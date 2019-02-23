

## 介绍

> 这个项目是我花了整整一个月的时间，写的一个网页聊天应用，主要功能如下：
>
> > * 注册、登录、修改密码、个人资料等
> > * 社交功能：包括添加、关注、取消关注、删除好友等等
> > * 聊天功能：包括新建聊天室、群组聊天、私人聊天
> > * 特色功能：私人聊天可以查看在线状态，更多功能请自行探索。
>
> 开发框架：Python-Django
>
> 核心技术：Channels-WebSocket、Redis
>
> 编程语言：Html、Ptrgon、JavaScript、CSS

## 打开终端输入以下命令:

 - git clone https://github.com/MTxZz/webchat
 - virtualenv Dj  --no-site-packages
 - source ./Dj/bin/activate
 - pip install -r requirements.txt
 - python manage.py migrate
 - python manage.py createsuperuser
 - python manage.py run_chat_server

## 打开新的终端，接着输入，前一个终端不要关

 - python manage.py runserver

## 打开浏览器，访问:127.0.0.1:8000