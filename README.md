## api_monitor
接口监控，url监控，

##需要启动2个进程
 1.api.py 是用web.py框架写的2个用来发送短信，和邮件的接口
 2.check_api2.py 是一个监控url的脚本
  2.1脚本循环读取post.url文件，
  2.2定时请求url如果返回的http状态码不是200就调用短信和邮件接口发送告警。
  2.3为避免短信浪费和邮件轰炸，加了锁功能调用告警接口前会判断下lock文件存不存在，存在就不再发送告警，如果所有url监控ok就删除lock文件。
  2.4用supervisord来守护上面2个进程

##supervisord配置文件  
[root@autoyunwei api_monitor]# cat /etc/supervisord/check_api2.conf 
[program:check_api2]
command=nohup python  /root/script/check_api2.py &
stdout_logfile=/var/log/check_api2_stdout.log
autostart=true
autorestart=true
startsecs=5
priority=1
stopasgroup=true
killasgroup=true



[root@autoyunwei api_monitor]# cat /etc/supervisord/api.conf 
[program:api]
command=nohup python  /root/script/api.py &
stdout_logfile=/var/log/api_stdout.log
autostart=true
autorestart=true
startsecs=5
priority=1
stopasgroup=true
killasgroup=true

