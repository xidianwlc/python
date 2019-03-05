#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   package.py    
@Desc    :   
@Contact :   thefreer@outlook.com
@License :   (C)Copyright 2018-2019, TheFreer.NET
@WebSite :   www.thefreer.net
@Modify Time      @Author    @Version
------------      -------    --------
2019/3/5 13:37   thefreer      1.0         
'''
from PyInstaller.__main__ import run

if __name__ == '__main__':

    opts = ['ui_zhilian.py', '-w', '--onefile']
    #opts = ['calculator.py', '-F']
    #opts = ['calculator.py', '-F', '-w']
    #opts = ['calculator.py', '-F', '-w', '--icon=TargetOpinionMain.ico','--upx-dir','upx391w']
    run(opts)