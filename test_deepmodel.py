import os
import argparse
import cv2
import numpy as np

import torch
from torchvision import datasets, models, transforms
import torchvision
from skimage.metrics import structural_similarity as compare_ssim

from detect_corner import get_avatar
# from detect_person import Person_Detection

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--avatar', type=str, default='hero/hero_avatar.txt')
    parser.add_argument('--size', type=int, default=128)
    parser.add_argument('--device', type=str, default='cuda:0')
    parser.add_argument('--input', type=str, default='test_data/test_images')
    parser.add_argument('--output', type=str, default='output.txt')
    parser.add_argument('--visualize', type=str, default='visualize')
    args = parser.parse_args()

    # person_model = Person_Detection(args.device)
    data_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(224),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    model_ft = models.resnet18(pretrained=True)
    model_ft.eval()

    if not os.path.exists(args.visualize):
        os.makedirs(args.visualize)

    # Read Storage
    with open(args.avatar) as f:
        hero_list = [line.strip().split() for line in f]
    hero_storage = {}
    for hero in hero_list:
        image = cv2.imread(hero[0])
        image = data_transforms(image)
        image.unsqueeze_(dim=0)
        with torch.no_grad():
            hero_storage[hero[1]] = model_ft(image)[0]
    
    # Read Test
    hero_test_paths = [os.path.join(args.input, i) for i in os.listdir(args.input)]
    hero_test_paths.sort()
    with open(args.output, 'w') as f:
        for hero_path in hero_test_paths:
            print(os.path.basename(hero_path))
            avatar = get_avatar(hero_path)
            cv2.imwrite(os.path.join(args.visualize, os.path.basename(hero_path)), avatar)
            avatar = data_transforms(avatar)
            avatar.unsqueeze_(dim=0)
            with torch.no_grad():
                search_ft = model_ft(avatar)[0]
            score_dict = {}
            for name, hero_ft in hero_storage.items():
                dist  = np.linalg.norm(search_ft - hero_ft)
                score_dict[name] = dist
            # predicted = max(score_dict, key=score_dict.get)
            predicted = sorted(score_dict.items(), key=lambda x:x[1])
            predicted = ' '.join(str(item) for innerlist in predicted[:5] for item in innerlist)
            # print(hero_path, predicted)
            f.write(os.path.basename(hero_path) + '\t' + predicted + '\n')
            

