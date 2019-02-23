# -*- coding: utf-8 -*-
# @Author: ZhaZhaHui
# @Date:   2019-01-09 19:32:31
# @Last Modified by:   ZhaZhaHui
# @Last Modified time: 2019-01-09 19:32:31

import argparse
import os
import numpy as np
import math
import itertools
import cv2 as cv
import time

import torchvision.transforms as transforms
from torchvision.utils import save_image
from torch.utils.data import dataloader
import torch.utils.data as Data
from torchvision import datasets
from torch.autograd import Variable
from sklearn.metrics.pairwise import cosine_similarity
import torch.nn as nn
import torch.nn.functional as F
import torch
from img_cut import img_cut

os.makedirs('images', exist_ok=True)

#参数
parser = argparse.ArgumentParser()
parser.add_argument('--n_epochs', type=int, default=2500, help='number of epochs of training')
parser.add_argument('--batch_size', type=int, default=64, help='size of the batches')
parser.add_argument('--lr', type=float, default=0.0002, help='adam: learning rate')
parser.add_argument('--b1', type=float, default=0.5, help='adam: decay of first order momentum of gradient')
parser.add_argument('--b2', type=float, default=0.999, help='adam: decay of first order momentum of gradient')
parser.add_argument('--n_cpu', type=int, default=8, help='number of cpu threads to use during batch generation')
parser.add_argument('--latent_dim', type=int, default=100, help='dimensionality of the latent code')
parser.add_argument('--img_size', type=int, default=60, help='size of each image dimension')
parser.add_argument('--channels', type=int, default=3, help='number of image channels')
parser.add_argument('--sample_interval', type=int, default=400, help='interval between image sampling')
opt = parser.parse_args()
print(opt)

#数据集中的图像形状
img_shape = (opt.channels, opt.img_size, opt.img_size)

cuda = True if torch.cuda.is_available() else False

#再参数化
def reparameterization(mu, logvar):
    std = torch.exp(logvar / 2)
    sampled_z = Variable(Tensor(np.random.normal(0, 1, (mu.size(0), opt.latent_dim))))
    z = sampled_z * std + mu
    return z

#编码器——生成器
class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(int(np.prod(img_shape)), 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.LeakyReLU(0.2, inplace=True)
        )

        self.mu = nn.Linear(512, opt.latent_dim)
        self.logvar = nn.Linear(512, opt.latent_dim)

    def forward(self, img):
        img_flat = img.view(img.shape[0], -1)
        x = self.model(img_flat)
        mu = self.mu(x)
        logvar = self.logvar(x)
        z = reparameterization(mu, logvar)
        return z

#解码器
class Decoder(nn.Module):
    def __init__(self):
        super(Decoder, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(opt.latent_dim, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, int(np.prod(img_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        img_flat = self.model(z)
        img = img_flat.view(img_flat.shape[0], *img_shape)
        return img

#判别器
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(opt.latent_dim, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, z):
        validity = self.model(z)
        return validity

# Use binary cross-entropy loss
#分别为自编码器和对抗网络设置损失函数
adversarial_loss = torch.nn.BCELoss()
pixelwise_loss = torch.nn.L1Loss()

# Initialize generator and discriminator
#实例化
encoder = Encoder()
decoder = Decoder()
discriminator = Discriminator()

# encoder = torch.load('models/encoder.pkl')
# encoder.eval()
# decoder = torch.load('models/decoder.pkl')
# decoder.eval()
# discriminator = torch.load('models/discriminator.pkl')
# discriminator.eval()


if cuda:
    encoder.cuda()
    decoder.cuda()
    discriminator.cuda()
    adversarial_loss.cuda()
    pixelwise_loss.cuda()

# Configure data loader
#加载数据集
root = ".\\tmp"  # 这里是自己的图片的位置
train_data = datasets.ImageFolder(
    root = root,
    transform=transforms.ToTensor()
)
data_loader = Data.DataLoader(dataset=train_data, batch_size=opt.batch_size, shuffle=True)

# Optimizers
#分别为编码器和对抗网络定义优化器
optimizer_G = torch.optim.Adam( itertools.chain(encoder.parameters(), decoder.parameters()),
                                lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

#定义Pytorch张量
Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

#每训练一次使用解码器生成图像结果
def sample_image(n_row, batches_done):
    """Saves a grid of generated digits"""
    # Sample noise
    #随机产生z输入解码器
    z = Variable(Tensor(np.random.normal(0, 1, (n_row**2, opt.latent_dim))))
    gen_imgs = decoder(z)
    save_image(gen_imgs.data, 'images/%d.png' % batches_done, nrow=n_row, normalize=True)
# ----------
#  Training
# ----------
#进行训练
for epoch in range(opt.n_epochs):
    for i, (imgs, b_label) in enumerate(data_loader):
        # Adversarial ground truths
        #定义real_deature和fake_feature
        valid = Variable(Tensor(imgs.shape[0], 1).fill_(1.0), requires_grad=False)
        fake = Variable(Tensor(imgs.shape[0], 1).fill_(0.0), requires_grad=False)
        # Configure input
        #real_imgs是读入的数据集中的真实图像
        real_imgs = Variable(imgs.type(Tensor))
        # -----------------
        #  Train Generator
        # -----------------
        #训练生成器
        optimizer_G.zero_grad()
        encoded_imgs = encoder(real_imgs)
        decoded_imgs = decoder(encoded_imgs)
        # Loss measures generator's ability to fool the discriminator
        #计算生成器的损失率
        g_loss =    0.001 * adversarial_loss(discriminator(encoded_imgs), valid) + \
                    0.999 * pixelwise_loss(decoded_imgs, real_imgs)
        #损失率反向传播
        g_loss.backward()
        #反向传播之后优化生成器
        optimizer_G.step()

        # ---------------------
        #  Train Discriminator
        # ---------------------
        #训练判别器
        optimizer_D.zero_grad()
        # Sample noise as discriminator ground truth
        #z是以我们期望的分布生成的一维特征向量
        z = Variable(Tensor(np.random.normal(0, 1, (imgs.shape[0], opt.latent_dim))))
        # Measure discriminator's ability to classify real from generated samples
        #分别计算真实损失率和虚假损失率
        real_loss = adversarial_loss(discriminator(z), valid)
        fake_loss = adversarial_loss(discriminator(encoded_imgs.detach()), fake)
        #计算判别器损失率
        d_loss = 0.5 * (real_loss + fake_loss)
        #反向传播
        d_loss.backward()
        #优化判别器
        optimizer_D.step()
        print ("[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]" % (epoch, opt.n_epochs, i, len(data_loader),
                                                            d_loss.item(), g_loss.item()))
        batches_done = epoch * len(data_loader) + i
        #保存结果图像以及模型
        if batches_done % opt.sample_interval == 0:
            sample_image(n_row=10, batches_done=batches_done)
            #只保存模型参数
            # torch.save(encoder.state_dict(), 'models/encoder_dict.pkl')
            # torch.save(decoder.state_dict(), 'models/decoder_dict.pkl')
            # torch.save(discriminator.state_dict(), 'models/discriminator_dict.pkl')
            # #保存整个模型
            # torch.save(encoder, 'models/encoder.pkl')
            # torch.save(decoder, 'models/decoder.pkl')
            # torch.save(discriminator, 'models/discriminator.pkl')

##加载以训练好的模型进行验证， 还没写好
# for epoch in range(opt.n_epochs):
#     for i, (imgs, b_label) in enumerate(data_loader):
#         real_imgs = Variable(imgs.type(Tensor))
# #         with open('2.txt', 'w') as f:
# #             f.write(str(real_imgs))
#         encoded_imgs = encoder(real_imgs)
#         decoded_imgs = decoder(encoded_imgs)
#         decoded_imgs = decoded_imgs.detach().numpy()
#         real_imgs = real_imgs.detach().numpy()
#         decoded_imgs = decoded_imgs*300
#         decoded_imgs = decoded_imgs.astype(np.int32)
#         for d in decoded_imgs:
#             for s in d:
#                 with open('1.txt', 'w') as f:
#                     f.write(str(s))
#                 cv.imwrite('cut.jpg', s)
#                 # cv.imshow('cut', s)
#                 # cv.waitKey()
#                 time.sleep(20)
#                 # cv.destroyAllWindows()
