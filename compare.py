from skimage.metrics import structural_similarity as compare_ssim
import cv2
import os

# load the two input images
imageA = cv2.imread("/storage/cv_hcm/huyvt/inteview/hero/hero_avatar/Ahri.jpg")
imageA = cv2.resize(imageA, (24,24), interpolation = cv2.INTER_AREA)
imageB = cv2.imread("/storage/cv_hcm/huyvt/inteview/Hero_Name_Recognition/avatar.jpg")
imageB = cv2.resize(imageB, (24,24), interpolation = cv2.INTER_AREA)
# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

folder = '/storage/cv_hcm/huyvt/inteview/hero/hero_avatar'
scores = []
for i in os.listdir(folder):
    print(i)
    imageA = cv2.imread(os.path.join(folder, i))
    imageA = cv2.resize(imageA, (24,24), interpolation = cv2.INTER_AREA)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    scores.append(float(score))
    print("SSIM {}: {}".format(i, score, diff))
scores.sort()
print(scores)
