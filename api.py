#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: qiantu
#qq 261767353

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import web
import httplib
import redis
import urllib
import urllib2
import json

urls = (
    '/mail', 'mail',
    '/sms', 'sms'
)

class mail:
    def GET(self):
        i=web.input()
	toaddr=i.get('toaddr')
	header=i.get('header')
	content=i.get('content')

	print toaddr.split()
	def sendmail():
		def _format_addr(s):
		    name, addr = parseaddr(s)
		    return formataddr(( \
			Header(name, 'utf-8').encode(), \
			addr.encode('utf-8') if isinstance(addr, unicode) else addr))

		from_addr = "wangqiantu@zuozh.com"
		password = "******"
		to_addr = toaddr.split(",")
		print to_addr
		smtp_server = "smtp.zuozh.com"


		msg = MIMEText(content, 'html', 'utf-8')
		msg['From'] = _format_addr(u'邮件接口自动发送 <%s>' % from_addr)
		msg['To'] = _format_addr(u'运维 <%s>' % to_addr)
		msg['Subject'] = Header(header, 'utf-8').encode()

		server = smtplib.SMTP(smtp_server, 25)
		server.set_debuglevel(1)
		server.login(from_addr, password)
		server.sendmail(from_addr, to_addr, msg.as_string())
		server.quit()

	if len(i) <3:
		return	u'mail send fail,'.encode('GBK')+' please check the args, /mail?toaddr=wangqiantu@zuozh.com&content="content"&header="title"'
	else:
		sendmail()
		print "mail send Successful"
        return u'mail send Successful'.encode('GBK')

class sms:
    def POST(self):
        i=web.input()
        phone=i.get('phone')
        key_in=i.get('password')
        message=i.get('message')
	url='http://wt.3tong.net/json/sms/Submit'
	account="user"
	password="password"
        print phone
        mobile =phone
        text = message.encode('utf-8')
        print type(message)
        control=True
	sign="【牛板金】"
        key="*******"
        def send_sms(text, mobile):
    		"""
    		能用接口发短信
    		"""
    		values ={'account':account,'password':password,'phones':mobile,'content':text,'sign':sign}
    		print sign
    		jdata = json.dumps(values)
    		req = urllib2.Request(url, jdata)
    		response = urllib2.urlopen(req)
   		return response.read()
        if key_in !=key:
        	return  u'sms send fail,'.encode('GBK')+' password error'
        elif control==False:
                return  u'sms send fail,'.encode('GBK')+' control is off'
        else:
                send_sms(text, mobile)
                print "sms send Successful"
        return u'sms send Successful'.encode('GBK')



if __name__ == "__main__":
    app = web.application(urls, globals())
    web.httpserver.runsimple(app.wsgifunc(), ('0.0.0.0', 11111))
    app.run()
