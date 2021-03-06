## 简要说明

> * 此文件夹中的代码为 <b>SRTP 项目 </b>全部流程代码，其中有关于深度学习的训练集这里无法提供。
>
> * 关于每个源文件的具体说明如下：
>   * img_cut.py —— 对输入图像进行预处理切割
>   * AAE.py —— 对抗生成网络与深度自编码器的结合品，即对抗自编码器，用来对图像特征提取
>   * tools.py —— 每个源代码里需要用到的工具函数
>   * cluter.py —— 在对图像特征匹配之前进行层次聚类过滤
> * 代码完成情况说明：
>   * 特征提取及预处理完成，最后的特征匹配未完成
>   * 各个模块之间的对接未完成

<hr><b>以下为关于此次 SRTP 的详细说明</b></hr>

## 建立板件库

> 利用python爬虫爬取了淘宝上一部分板件的信息，包括价格，发货地，销量，运费，板件的图片，型号等数据，建立了板件的估价的初步模型，估价的准确度达到90%以上，建立了板件数据库，数量达到8000种以上。

建立板件库完成情况：100%

残留问题/待改进：待建立板件估价模型

## 图像识别

### 图像预处理

> 对用户输入的图像进行预处理，包括去噪、灰度化、二值化、增强、形态学处理等一系列操作，最后的目的是力求完整地从输入图像中切割出目标板件，并且争取切割结果不对识别结果产生较大影响



- 图像预处理完成情况：90%，采取的是矩形切割办法，对于一般图像预处理结果没有大问题

- 残留问题/待改进：对切割算法进行进一步优化

### 图像特征提取

> 对经过预处理的图像降维，提取出其一系列代表特征。作为从库中匹配图像的依据。采取的方法是深度对抗自编码器。



- 特征提取完成情况：90%，深度学习算法没有什么问题，初步训练的结果不错

- 残留问题/待改进：对自编码器模型进行最后的大规模训练，将训练集图像的分辨率从 60*60 提升到 600*600，根据训练结果改进模型参数。

### 图像匹配，即图像识别

> \1. 先根据输入图像初步过滤掉板件库中 90% 以上的图像，采取的办法是长宽比划分以层次聚类的办法；

> \2. 再对输入图像进行特征提取，让此特征与板件库中剩余的图像进行进一步特征匹配；

> \3. 最后以相似度排名输出匹配结果

- 图像匹配完成情况：60%，初步过滤已经完成，特征匹配还在尝试各种方法中，目前已经尝试了 SIFT 和 SURF算法，下一步准备尝试一下 LOPQ算法

- 残留问题/待改进：SIFT 和 SURF 速度很慢，速度需要改进，想尝试一下 LOPQ 算法；

## 建立板件估价模型

> 待完成

