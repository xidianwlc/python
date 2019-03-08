

## 介绍

> 这个项目是我花了整整一个月的时间，写的一个网页聊天应用，主要功能如下：
>
> > * 注册、登录、修改密码、个人资料等
> > * 响应式设计，同时兼容各种大小的页面
> > * 社交功能：包括添加、关注、取消关注、删除好友等等
> > * 聊天功能：包括新建聊天室、群组聊天、私人聊天
> > * 特色功能：私人聊天可以查看在线状态，更多功能请自行探索。
>
> 部分功能预览可以查看截图
> (由于 Channels 需要 redis 数据库支持，我的 Windows 未安装 Redis，所以关于聊天室部分我没有进行演示，只演示了私人聊天部分及部分应用功能)
>
> 开发框架：Python-Django
>
> 核心技术：Channels-WebSocket、Redis
>
> 编程语言：Html、Ptrgon、JavaScript、CSS

## 打开终端输入以下命令:

### Linux 用户：

> git clone https://github.com/thefreer98/python.git
>
> cd python/webchat
>
> virtualenv Dj  --no-site-packages
>
> source ./Dj/bin/activate
>
> pip install -r requirements.txt
>
> python manage.py migrate
>
> python manage.py run_chat_server

### Windows 用户：

> git clone https://github.com/thefreer98/python.git
>
> cd python/webchat
>
> virtualenv Dj  --no-site-packages
>
> source ./Dj/Scripts/activate
>
> pip install -r requirements.txt
>
> pip install pypiwin32
>
> python manage.py migrate
>
> python manage.py run_chat_server

## 打开新的终端，接着输入，前一个终端不要关

> cd python/webchat
>
> source ./Dj/Scripts/activate
>
> python manage.py runserver

## 打开浏览器，访问:127.0.0.1:8000