import cv2 as cv
import os
from img_cut import img_cut


# 批量改变图像大小或者裁剪图像，可自行更改

# # 裁剪imgs/taobao的图像
# imgDir = "imgs/taobao"
# imgList = os.listdir(imgDir)
# count = 0
# for im in imgList:
# 	try:
# 		imgPath = imgDir + '/' + im
# 		img = img_cut(imgPath)
# 		# img = cv.resize(img,(40,40))
# 		print('imgs/taobao_cut/' + im)
# 		cv.imwrite('imgs/taobao_cut/' + im, img)
# 		count+=1
# 	except:
# 		pass

# 批量改变imgs/yuan图像大小，imgDir自行更改
imgDir = "imgs/yuan"
imgDirList = os.listdir(imgDir)
count = 0
for dir in imgDirList:
	imgList = os.listdir(imgDir + '/' + dir)
	for imD in imgList:
		# if count > 15:
		# 	break
		try:
			imDList = os.listdir( imgDir + '/' + dir + '/' + imD)
			for im in imDList:
				imgPath = imgDir + '/' + dir + '/' + imD + '/' + im
				print(imgPath)
				# try:
				img = cv.imread(imgPath)
				img = cv.resize(img,(60,60))
				print('tmp/tmp/' + im)
				cv.imwrite('tmp/tmp/' + im, img)
				count+=1
				# except:
				# 	print("有一个异常")
				# 	pass
		except:
			pass