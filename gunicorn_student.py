# -*- encoding: utf-8 -*-
# @ModuleName: gunicorn_teacher
# @Function :
# @Author : ximo
# @Time : 2022/10/19 14:14
import multiprocessing
import yaml

# 并行工作进程数
workers = 2
# 指定每个工作者的线程数
# threads = 1
# 监听内网端口5000
f = open('config.yaml', 'r')
config_data = yaml.load(f, Loader=yaml.FullLoader)
bind = config_data['base_data']['student']['ip'] + ":" + config_data['base_data']['student']['port']
print(bind)
# bind = '10.66.10.234:5000'
# bind = '173.0.85.5:5000'
# bind = '10.160.195.50:50'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式同步
timeout = 600
worker_class = 'sync'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = './log/student_gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = './log/student_gunicorn_access.log'
errorlog = './log/student_gunicorn_error.log'
# 设置这个值为true 才会把打印信息记录到错误日志里
# capture_output = True
# 设置日志记录水平
loglevel = 'warning'
debug = False
# 启动 gunicorn -c gunicorn.conf api:app
# api是flask入口文件名
# 杀死 pstree -ap|grep gunicorn 找到主进程，kill -9
