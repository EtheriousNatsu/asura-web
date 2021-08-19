# asura-web
本项目为阿修罗接口测试平台的后端代码，[前端代码传送门](https://github.com/EtheriousNatsu/asura-frontend)

# 功能简介
该测试平台是仿照[assertible]()实现的，已实现[assertible]()的大部分主要功能，感兴趣的可以参考assertible的[使用手册](https://assertible.com/docs)
进行体验，[体验地址](http://120.79.132.106)

# 技术栈
* Django
* Django rest_framework
* Django-configurations
* Celery
* Django_celery_beat
* rest_framework.authtoken
* Channels
* Requests
* dj-database-url
* jsonpath-rw&jsonpath-rw-ext

# 前置准备

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# 项目结构
```bash
── asura
│   ├── __init__.py
│   ├── asgi.py             ;channel配置文件
│   ├── assertions          ;assertion app
│   ├── celery.py           ;celery配置文件
│   ├── config              ;django配置文件
│   ├── core                ;核心框架
│   ├── environments        ;environment app
│   ├── hooks               ;hook app
│   ├── results             ;result app
│   ├── routing.py          ;channel全局路由
│   ├── schedules           ;schedule app
│   ├── services            ;service app
│   ├── steps               ;step app
│   ├── tasks.py            ;公用任务
│   ├── testcases           ;testcase app
│   ├── testsuites          ;testsuite app
│   ├── urls.py             ;django全局路由 
│   ├── users               ;user app
│   ├── utils
│   └── wsgi.py
├── compose                 ;Dockerfile
│   ├── local
│   └── production
├── local.yml               ;本地部署文件
├── manage.py
├── production.yml          ;生产部署文件
├── requirements            ;依赖库
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── setup.cfg
├── static                  ;静态资源
│   ├── css
│   └── images
├── templates               ;模板文件
│   └── email
└── wait_for_postgres.py
```
# 本地开发

启动服务:
```bash
docker-compose -f local.yml up
```

# 生产部署
1.首先创建文件 .envs/.production/.django，内容如下:

|   DJANGO_SECRET_KEY  | ${Django生产环境秘钥}  |
|  :-----  | :-----  |
| SERVICE_HOST  | ${项目服务器地址} |
| EMAIL_HOST  | ${邮箱服务器地址} |
| EMAIL_PORT  | ${邮箱服务器端口} |
| EMAIL_HOST_USER  |  ${邮箱账号}|
| EMAIL_HOST_PASSWORD  |  ${邮箱密码}|

2.使用命令启动服务: `docker-compose -f production.yml up -d`


# 数据库
开发环境你可以使用客户端程序连接数据库，数据库连接信息如下:

|   主机  | 127.0.0.1  |
|  :-----  | :-----  |
| 端口  | 5432 |
| 初始数据库  | postgres |
| 用户名  | postgres |
| 密码  |  |

PS:生产环境，数据库放在容器里面，容器一旦删除，数据就会丢失。如果需要查询直接登陆到容器内使用
`psql`查询