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
2019/3/5 13:25   thefreer      1.0         
'''
from PyInstaller.__main__ import run

if __name__ == '__main__':

    opts = ['ui_58.py', '-w', '--onefile']
    run(opts)