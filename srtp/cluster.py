# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2019-01-09 19:28:41
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-09 19:31:11

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import re
import os
from sklearn import cluster
from sklearn.metrics.pairwise import cosine_similarity
from img_cut import img_cut



def getSim(t, k):
	c = cosine_similarity([t, k])
	c = c[0] / 2 + c[1] / 2
	c = c[0] / 2 + c[1] / 2
	return c


def getCluster(featureDict, n):
	featureList = [featureDict[f][0] for f in featureDict]
	# categoryDict = featureDict
	categoryDict = {}
	sk = cluster.AgglomerativeClustering(n)  #
	sk.fit(np.asarray(featureList).reshape(-1, 3))
	for i in range(sk.n_clusters):
		categoryDict[i] = []
	j = 0
	for key in featureDict:
		categoryDict[sk.labels_[j]].append([key, featureDict[key][0], featureDict[key][1]])
		j += 1
	return categoryDict


# def LWdivision(imgList, d):
# 	# print(imgList)
# 	"""
# 	长宽比划分
# 	:param List:图像列表
# 	:param d:划分的个数
# 	:return: 划分好的列表
# 	"""
# 	List = [img.shape[1] / img.shape[0] for img in imgList]
# 	# print(List)
# 	L = sorted(List)
# 	# print(L)
# 	num = int(len(List) / d) + 1
# 	# print(num)
# 	sortList = []
# 	for i in range(num + 1):
# 		if L[i * num:i * num + num] != []:
# 			sortList.append(L[i * num:i * num + num])
#
# 	return sortList


class imageFeature(object):
	"""
    这个类用来描述图像的一系列特征,
    将特征与图像映射起来
	"""

	def __init__(self):
		super(imageFeature, self).__init__()
		self.path = ''  # 图像路径
		# self.category = 0#分类序号
		self.LW = 0.000000  # 长宽比
		self.feature = 0  # 特征
		self.target = 0  # 标签序号——这个暂时没有
		self.targetNames = ''  # 标签名字——这个暂时没有
		self.featureName = ''  # 分类名字
		self.Dict = {}

	def img(self, path):
		# print(path)
		self.path = path
		img = cv.imread(path)
		self.LW = img.shape[1] / img.shape[0]
		self.feature = self.getHistFeature(img)
		self.Dict[self.path] = [self.feature, self.LW]
		return img

	def getHistFeature(self, img):
		'''
		获取图像的直方图统计特征
		:param imgList: 图像
		:return feather： 三个通道的均值/方差/标准差
		'''
		Hist = [cv.calcHist([img], [i], None, [256], [0.0, 255.0]) for i in range(img.shape[2])]
		'''
		hist = cv2.calcHist([image], [0], None, [256], [0.0,255.0])
		第一个参数[image]，必须带[]， 是读入后的图像

		第二个参数[0]，必须带[]，指定通道,若为灰度图则为[0]，若彩色图，则[0]、[1]、[2]分别对应于B、G、R通道

		第三个参数是掩膜Mask，指定ROI区域，若对整张图像取特征，则置为None

		第四个参数是bins的个数，必须带[]

		第五个参数是像素值范围
		'''

		# print(len(Hist))
		feature = []
		for H in Hist:
			# 求均值
			hist_mean = np.mean(H)
			hist_var = np.var(H)
			# 求标准差
			hist_std = np.std(H, ddof=1)
			# 求变异系数代替标准差和均值
			hist_cv = hist_std / hist_mean
			feature += [hist_cv]
		# print(feather)
		# featureList.append(feature)
		return feature

imageFeature = imageFeature()

if __name__ == '__main__':
	# 先对所有带匹配图片特征提取存入featureDict
	imgDir = 'imgs/taobao_cut'
	imgFiles = os.listdir(imgDir)
	imgList = [imageFeature.img(imgDir + '/' + i) for i in imgFiles]
	imgLWList = sorted([img.shape[1] / img.shape[0] for img in imgList])
	# print(imgLWList)
	# 目标图像
	testName = '10_1.jpg'
	testPath = 'imgs/taobao/' + testName
	testImg = img_cut(testPath)
	testFeature = imageFeature.getHistFeature(testImg)
	LW = testImg.shape[1] / testImg.shape[0]
	# firstList = []
	# 长宽比过滤, 以指定大小范围
	LWScope = (LW - 0.2, LW + 0.2)
	firstList = []
	for lw in imgLWList:
		if lw >= LWScope[0] and lw <= LWScope[1]:
			firstList.append(lw)
		else:
			pass
	# print(firstList)
	featureDict = imageFeature.Dict
	feaDict = {}
	for path in featureDict:
		if featureDict[path][1] in firstList:
			feaDict[path] = featureDict[path]
	categoryDict = getCluster(feaDict, int(len(firstList) / 5) + 1)
	cList = []
	cDict = {}
	i = 0
	# 在聚类中匹配目标图像
	for cate in categoryDict:
		# if i % 3 == 0:
		s = categoryDict[cate][int(len(categoryDict[cate]) / 2)][1]
		s = getSim(s, testFeature)
			# tmp = []
			# s = 0
			# for feaList in categoryDict[cate]:
			# 	c = getSim(testFeature, feaList[1])
			# 	tmp.append(c)
			# s = np.var(tmp)
		cList.append(s)
			# print(s)
		cDict[s] = categoryDict[i]
		i += 1
	# print(categoryDict)
	cList = sorted(cList, reverse=True)[0:2]
	finaList = []
	for ca in cDict:
		if ca in cList:
			finaList.append(cDict[ca])
pathList = []
for l in finaList:
	for i in l:
		pathList.append(i[0])
print(pathList)
for s in pathList:
	r = re.findall(testName, s)
	if r != []:
		print("找到啦: %s !!!" % s)
		break
	else:
		pass