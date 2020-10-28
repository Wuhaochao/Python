import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt

'''绘制表格'''
def pltFig(datingDataMat, datingLabels):
	# 创建画表
	# plt.figure()中有个参数figsize = (2,2)，用来设置表格的大小
	fig = plt.figure(figsize=(10, 10))
	# 
	ax1 = fig.add_subplot(311)
	ax2 = fig.add_subplot(312)
	ax3 = fig.add_subplot(313)
	# 导入数据
	ax1.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * np.array(datingLabels), 15.0 * np.array(datingLabels))
	ax2.scatter(datingDataMat[:, 0], datingDataMat[:, 2], 15.0 * np.array(datingLabels), 15.0 * np.array(datingLabels))
	ax3.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0 * np.array(datingLabels), 15.0 * np.array(datingLabels))
	ax1.set(ylabel='玩视频游戏所耗时间', xlabel='每年获得飞行常客里程数')
	ax2.set(ylabel='每周消费冰淇淋公升数', xlabel='每年获得飞行常客里程数')
	ax3.set(ylabel='每周消费冰淇淋公升数', xlabel='玩视频游戏所耗时间')
	plt.show()


#创造矩阵
def createDataSet():
	# 生成矩阵
	group = np.array([1., 1.1], [1., 1.], [0, 0], [0, 0.1])
	# 标记特征值
	labels = ['a', 'a', 'b', 'b']
	return group, labels

'''inX为样本，dataSet为训练集，labels为标签向量，k为聚类个数'''
def classIfY0(inX, dataSet, labels, k):
	# 返回dataSet训练集的行数;*shape[0]为行数、shape[1]为列数
	dataSetSize = dataSet.shape[0]
	# np.tile为拷贝，将 inX 拷贝行dataSetSize次，列1次
	# 拷贝完的 inX' 减去dataSet矩阵 
	# 其实python具有广播机制也是可以的    
	# diffMat = inX - dataSet
	diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
	# 做完减法后得平方
	sqDiffMat = diffMat ** 2
	# sqDiffMat矩阵按行相加,得到dataSetSize列矩阵；*axis=1按行相加、axis=0按列相加
	sqDistances = sqDiffMat.sum(axis=1)
	# 对sqDistances矩阵开方
	distances = sqDistances**0.5
	# 从小到大排列，提取其对应的index(索引)
	sortedDistIndicies = distances.argsort()
	# 创建空字典，用来记录K个邻居点的特征值名称（键）-数量（值）
	classCount = {}
	for i in range(k):
		# 找到[0, k)区间较小的值所对应的特征值
		# sortedDistIndicies[i]返回数值较小的索引号
		voteIlabel = labels[sortedDistIndicies[i]]
		# 在字典中查找voteIlabel键的特征值个数
		# 若找到则返回voteIlabel键下对应的值并加1；
		# 若找不出，则新建voteIlabel（键）- 0（值）并加1
		classCount[voteIlabel] = classCount.setdefault(voteIlabel, 0) + 1 #**
	# classCount.items()返回键值对迭代器，字典形式：{'a':1,'b':3}-》列表形式[('a',1),('b',3)]
	# key=operator.itemgetter(1)使用元素第二维的数据进行排序
	# reverse=True决定了排序方式，从大到小
	sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True) #**
	return sortedClassCount[0][0]

'''读取训练文件'''
def file2matrix(fileName):
	# 读取文件
	with open(fileName) as fr:
		# 按行读取
		arrayOlinges = fr.readlines()
		# 获得长度
		numberOfLines = len(arrayOlinges)
		# 生成N * 3的矩阵
		returnMat = np.zeros((numberOfLines, 3))
		classLabelVector = []
		index = 0
		for line in arrayOlinges:
			line = line.strip()
			# 将行数据写入列表中
			listFromLine = line.split('\t')
			# 将文件的前三列写入矩阵中
			returnMat[index, :] = listFromLine[0: 3]
			# 记录第四列内容
			classLabelVector.append(int(listFromLine[-1]))
			# 行+1
			index += 1
			#print(line)
		'''返回前三列的数据矩阵和一列特征矩阵'''
		return returnMat, classLabelVector


'''归一化特征值'''
def autoNorm(dataSet):
	# 得到最大、最小值和差值
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)
	ranges = maxVals - minVals
	# 得到和训练集的同型矩阵
	normDataSet = np.zeros(np.shape(dataSet))
	# 得到行数
	dataSetRowNum = dataSet.shape[0]
	# 做矩阵数的减法和除法，实现归一化
	normDataSet = dataSet - np.tile(minVals, (dataSetRowNum, 1))
	normDataSet = normDataSet / np.tile(ranges, (dataSetRowNum, 1))
	return normDataSet, ranges, minVals, dataSetRowNum

'''分类器测试'''
def datingClassTest(datingDataMat, datingLabels):
	hoRatio = 0.1
	# 归一化，得到归一矩阵、差值矩阵、最小值矩阵和行数
	normMat, ranges, minVals, dataSetRowNum = autoNorm(datingDataMat)
	# 取百分之10作为测试数据
	numTestVecs = int(dataSetRowNum * hoRatio)
	# 错误统计
	errorCount = 0.0
	
	for i in range(numTestVecs):
		# 测试矩阵（0->numTestVecs-1）, 训练矩阵（numTestVecs->dataSetRowNum）,特征矩阵， K聚类的个数
		classIfierResult = classIfY0(normMat[i, :], \
			normMat[numTestVecs: dataSetRowNum, :], \
				datingLabels[numTestVecs: dataSetRowNum], \
					3)
		print(f'the classifier came back with : {classIfierResult}, the real answer is : {datingLabels[i]}')
		if classIfierResult != datingLabels[i]:
			errorCount += 1
	print(f'the total error rate is : {errorCount/float(numTestVecs)}')
	pltFig(datingDataMat, datingLabels)

'''分类器个人'''
def datingClassPerson(datingDataMat, datingLabels):
	resultList = ['不喜欢', '魅力一般', '极具魅力']
	ffMiles = float(input('每年获得飞行常客里程数:'))
	percentTats = float(input('玩视频游戏所耗时间:'))
	iceCream = float(input('每周消费冰淇淋公升数:'))
	# 创建单个小矩阵
	inArr = np.array([ffMiles, percentTats, iceCream])
	# 调用np.row_stack函数，将小矩阵并入大矩阵中
	datingDataMat = np.row_stack((datingDataMat, inArr))
	# 归一化，得到归一矩阵、差值矩阵、最小值矩阵和行数
	normMat, ranges, minVals, dataSetRowNum = autoNorm(datingDataMat)
	# 进入预测
	classIfierResult = classIfY0(normMat[-1, :], normMat[:-1, :], datingLabels, 3)
	print(resultList[int(classIfierResult) - 1])
	

if __name__ == '__main__':
	num = input('1：测试KNN的正确性\n2：自行输入数据，预测约会网站的匹配结果\n')
	# 读取文件
	datingDataMat, datingLabels = file2matrix(r'G:\WuDownload\CodeVsCode\CodePython\机器学习实战\机器学习实战资料\Ch02\datingTestSet2.txt')

	if num == '1':
		datingClassTest(datingDataMat, datingLabels)
	else:
		datingClassPerson(datingDataMat, datingLabels)
