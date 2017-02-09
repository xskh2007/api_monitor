#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import os
import time
#短信联系人
#phone1="15158887113,18268695533"
phone1="15158887113"
phone2="18268695533"
#报警邮件联系人
#mails="wangqiantu@zuozh.com,261767353@qq.com,zhouhuajun@zuozh.com,wangpanpan.zuozh.com"
mails="wangqiantu@zuozh.com,261767353@qq.com"
#检测时间间隔
interval=60
while 1:
	html="<html><head></head><body>"
	htmlend="</body></html>"
	errurl=""
	num=0
	ISOTIMEFORMAT='%Y-%m-%d %X'
	date_now=time.strftime( ISOTIMEFORMAT, time.localtime() )
	for line in open("/root/script/post.url"):
		error_num=0
		for x in range(0,3):
			try:
				status=urllib.urlopen(line).code
				surl="code:"+str(status)+"____"+"api:"+line.strip('\n')+"<br>"
				if status !=200:
					#errurl=errurl+surl
					error_num=error_num+1
					print '第'+str(x)+'次',surl
			except:
				print 'time out',error_num
				error_num = error_num + 1
				surl="code:"+"time out"+"____"+"api:"+line.strip('\n')+"<br>"

		if error_num==3:
			num=num+1
			errurl=errurl+surl
			#防止垃圾短信过滤，特意去掉http://,替换.号
			errurl_sms=errurl.replace('http://','').replace('.','点')
		print date_now+"|"+line.strip('\n')+"|"+'错误次数:'+str(error_num)
	content=html+errurl+htmlend
	if num >0 and num<=3 and not os.path.exists("/tmp/check_api.lock"):
	    cmd_mail="curl -d \"toaddr="+mails+"&content="+content+"&header=接口报警" +"\" http://192.168.2.168:11111/mail"
	    cmd_sms1="curl -d \"phone="+phone1+"&password=zzjr123456&message="+errurl_sms+"\" 192.168.2.168:11111/sms"
	    #邮箱接口调用
	    print content
	    os.system(cmd_mail)
	    #短信接口调用
	    os.system(cmd_sms1)
	    os.system("touch /tmp/check_api.lock")
	if num >4 and not os.path.exists("/tmp/check_api.lock"):
            cmd_mail="curl -d \"toaddr="+mails+"&content="+content+"&header=接口报警" +"\" http://192.168.2.168:11111/mail"
            cmd_sms1="curl -d \"phone="+phone1+"&password=zzjr123456&message="+"有大于3个接口告警,具体请查收邮件告警"+"\" 192.168.2.168:11111/sms"
            #邮箱接口调用
            print content
            os.system(cmd_mail)
            #短信接口调用
            os.system(cmd_sms1)
            os.system("touch /tmp/check_api.lock")
	elif num!=0 and os.path.exists("/tmp/check_api.lock"):
	    print "有接口报警，但告警锁已打开，不在发送告警信息"
	elif num==0 and os.path.exists("/tmp/check_api.lock"):
	    #删除报警锁,有此文件不会报警
	    os.system("rm -f /tmp/check_api.lock")
	    #邮箱接口调用
	    #os.system("curl \"http://192.168.2.168:11111/mail?toaddr="+mails+"&content=所有接口正常"+"&header=接口报警\"")
	    os.system("curl -d \"toaddr="+mails+"&content=所有接口正常"+"&header=接口报警"+"\" http://192.168.2.168:11111/mail")
	    #短信接口调用
	    os.system("curl -d \"phone="+phone1+"&password=zzjr123456&message="+"所有接口正常"+date_now+"\" 192.168.2.168:11111/sms")
	elif num==0 and not os.path.exists("/tmp/check_api.lock"):
	    print "所有接口检测ok"
	num=0
	time.sleep(interval)

