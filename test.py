import os
import argparse
import cv2

from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import mean_squared_error as mse

from detect_corner import get_avatar
# from detect_person import Person_Detection

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--avatar', type=str, default='hero/hero_avatar.txt')
    parser.add_argument('--size', type=int, default=14)
    parser.add_argument('--device', type=str, default='cuda:0')
    parser.add_argument('--input', type=str, default='test_data/test_images')
    parser.add_argument('--output', type=str, default='output.txt')
    parser.add_argument('--visualize', type=str, default='visualize')
    args = parser.parse_args()

    # person_model = Person_Detection(args.device)

    if not os.path.exists(args.visualize):
        os.makedirs(args.visualize)

    # Read Storage
    with open(args.avatar) as f:
        hero_list = [line.strip().split() for line in f]
    hero_storage = {}
    for hero in hero_list:
        image = cv2.imread(hero[0])
        image = cv2.resize(image, (args.size,args.size), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hero_storage[hero[1]] = gray
    
    # Read Test
    hero_test_paths = [os.path.join(args.input, i) for i in os.listdir(args.input)]
    hero_test_paths.sort()
    with open(args.output, 'w') as f:
        for hero_path in hero_test_paths:
            print(os.path.basename(hero_path))
            avatar = get_avatar(hero_path)
            cv2.imwrite(os.path.join(args.visualize, os.path.basename(hero_path)), avatar)

            avatar = cv2.resize(avatar, (args.size,args.size), interpolation = cv2.INTER_AREA)
            avatar = cv2.cvtColor(avatar, cv2.COLOR_BGR2GRAY)
            score_dict = {}
            for name, hero in hero_storage.items():
                (score, diff) = compare_ssim(avatar, hero, full=True)
                diff = (diff * 255).astype("uint8")
                score_dict[name] = score
            # predicted = max(score_dict, key=score_dict.get)
            predicted = sorted(score_dict.items(), key=lambda x:x[1], reverse=True)
            predicted = ' '.join(str(item) for innerlist in predicted[:5] for item in innerlist)
            # print(hero_path, predicted)
            f.write(os.path.basename(hero_path) + '\t' + predicted + '\n')
            

