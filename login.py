#!/usr/bin/env python
#coding:utf8
###Power by Hc1m1
#######

import sys
import re
import os
import time
import threading
import json
from md5 import md5
from Queue import Queue
import requests as requ

reload(sys)   
sys.setdefaultencoding('utf8')

cookieQu = Queue()
scheQu = Queue()
writQu = Queue()
endcookie = 0
endsche = 0
endstor = 0
endwrit = 0
#url2 = 'http://i.hdu.edu.cn/dcp/forward.action?path=/portal/portal&p=wkHomePage'
#url4 = 'http://i.hdu.edu.cn/dcp/forward.action?path=dcp/apps/sso/jsp/ssoDcpSelf&appid=1142'
#url5 = 'http://i.hdu.edu.cn'

class writeLog(threading.Thread):
	def __init__(self,username):
		threading.Thread.__init__(self)
		self.username = username
	def run(self):
		self.cookie_log()
		self.sche_log()
	def cookie_log(self):
		global cookieQu
		global endcookie
		global endstor
		
		file_path = './'+ self.username + '/cookie.txt'
		f = open(file_path,'w')
		while True:
			if cookieQu.empty() and endcookie:
				break	
			try:
				cont = cookieQu.get(block=False)
			except:
				continue
			f.write(cont)
			f.write('\n')
			print '[+] store cookie success!'
		f.close()
		endstor = 1
		print '[+] finish store!'
	def sche_log(self):
		global scheQu
		global endsche
		
		file_path = './'+ self.username + '/sche.html'
		f = open(file_path,'w')
		while True:
			if scheQu.empty() and endsche:
				break
			try:
				cont = scheQu.get(block=False)
			except:
				continue
			f.write(cont)
			f.write('\n')
		f.close()
		
		print '[+] Store schedule succeed!'
			
class get_Cook():
	def __init__(self,*arg):
		self.username = arg[0]
		self.password = arg[1]
		self.url1 = 'http://cas.hdu.edu.cn/cas/login'
		self.url7 = 'http://i.hdu.edu.cn/dcp/index.jsp?'
	
	def run(self):
		global cookieQu
		global endcookie
		
		cookie1 = self.get_cookie1()
		self.cookies1 = {cookie1[0]:cookie1[1],cookie1[2]:cookie1[3],cookie1[4]:cookie1[5]}
		quue1 = json.dumps(self.cookies1)
		cookieQu.put(quue1)
		print '[+] Get cas.hdu... cookie!'
		cookie2 = self.get_cookie2()
		self.cookies2 = {cookie2[0]:cookie2[1],cookie2[2]:cookie2[3]}
		quue2 = json.dumps(self.cookies2)
		cookieQu.put(quue2)
		print '[+] Get i.hdu... cookie!'
		endcookie = 1

	def get_cookie1(self):
		lt1 = requ.get(self.url1)
		lt_con = lt1.text
		lt2 = re.findall(r'lt.+(value=")(.+?)"',lt_con)[0][1].encode()
		
		post1 = dict(encodedService='http%3a%2f%2fi.hdu.edu.cn%2fdcp%2findex.jsp',service='http://i.hdu.edu.cn/dcp/index.jsp',serviceName='null',loginErrCnt=0,username=self.username,password=self.password,lt=lt2)
	
		da1 = requ.post(self.url1,data=post1)
		tick = da1.text
		try:
			tick2 = re.findall(r'(ticket=.+)">',tick)[0].encode()
		except:
			print '[-] Login fail!'
			os._exit(0)
		self.url7 += tick2
		cookie1 = da1.headers['set-cookie']
		return re.match(r'(key_dcp_cas)=(\w+\W+\w+).+(CASTGC)=(.+);.+(route)=(\w+)',cookie1).groups()

	def get_cookie2(self):
		index2 = requ.get(self.url7,allow_redirects=False)
		cookie2 = index2.headers['set-cookie']
		return re.match(r'(\w+).(\w+\W+?\w+).+(route).(\w+)',cookie2).groups()
class login_sch():
	def __init__(self,*arg):
		self.username = arg[0]
		self.password = arg[1]
		self.url3 = 'http://jxgl.hdu.edu.cn/index.aspx'
		self.url6 = 'http://jxgl.hdu.edu.cn/xs_main.aspx?xh=' + self.username
		self.url8 = 'http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/index.aspx'
		self.url9 = 'http://jxgl.hdu.edu.cn/'
		self.openlog()
	def openlog(self):
		global endstor
		
		while not endstor:
			pass
		try:
			file_path = './'+ self.username + '/cookie.txt'
			f = open(file_path)
		except:
			print '[-] Open file fail!'
			os._exit(0)
		cooki = f.read()
		if len(cooki) == 0:
			print '[-] Read cookie fail!'
			os._exit(0)
		cooki = cooki.split('\n')
		self.cookies1 = json.loads(cooki[0])
		self.cookies2 = json.loads(cooki[1])
		print '[+] Get cookie log succeed!'
		
	def run(self):
		cookie3 = self.get_cookie3()
		self.cookies3 = {cookie3[0]:cookie3[1],cookie3[2]:cookie3[3]}
		sche_url = self.login1()
		self.url9 += sche_url
		#print '[+] Schedual url is ' + self.url9
		self.login6()
		
	def get_cookie3(self):
		index3 = requ.get(self.url3,cookies=self.cookies2,allow_redirects=False)
		coo4 = index3.headers['set-cookie']
		print '[+] Get schedule cookie!'
		return	re.match(r'(ASP.NET_SessionId).(\w+).+(route).(\w+)',coo4).groups()

	def login1(self):
		url7 = 'http://jxgl.hdu.edu.cn/index.aspx?ticket='
		xs = requ.get(self.url8,cookies=self.cookies1,allow_redirects=False)
		url7 += xs.headers['cas-ticket']
		xs2 = requ.get(url7,cookies=self.cookies3)
		xs3 = requ.get(self.url6,cookies=self.cookies3)
		return re.findall(r'.+(xskbcx.aspx\?.+?)"',xs3.text)[0]

	def login6(self):
		global endsche
		global scheQu
		
		headers = {'Referer':self.url6}
		kb = requ.get(self.url9,headers=headers,cookies=self.cookies3)
		schedu = kb.text.split('\n')
		for x in schedu:
			scheQu.put(x)
		endsche = 1

class writeThread(threading.Thread):
	def __init__(self,username):
		threading.Thread.__init__(self)
		self.username = username
	def run(self):
		global writQu
		global endwrit
		
		file_path = './'+ self.username + '/sche.txt'
		f = open(file_path,'w')
		while True:
			if writQu.empty() and endwrit:
				break	
			try:
				cont = writQu.get(block=False)
			except:
				continue
			f.write(cont)
			f.write('\n')
		f.close()
		print '[+] write schedule succeed!'

class write_sche():
	def __init__(self,sche,username):
		self.sche = sche
		self.username = username
		
	def regular(self):
		global writQu
		global endwrit
		a = self.sche
		
		writ = writeThread(self.username)
		writ.start()
		
		stuid = re.findall(ur'Label5">([\u4e00-\u9fa5]+).+?(\d+)',a)
		stuid = stuid[0][0] + ':' + stuid[0][1]
		writQu.put(stuid)
		name = re.findall(ur'Label6">([\u4e00-\u9fa5]+).+?([\u4e00-\u9fa5]+)',a)
		name = name[0][0] + ':' + name[0][1]
		writQu.put(name)
		college = re.findall(ur'Label7">([\u4e00-\u9fa5]+).+?([\u4e00-\u9fa5]+)',a)
		college = college[0][0] + ':' + college[0][1]
		writQu.put(college)
		profe = re.findall(ur'Label8">([\u4e00-\u9fa5]+).+?([\u4e00-\u9fa5]+)',a)
		profe = profe[0][0] + ':' + profe[0][1]
		writQu.put(profe)
		grade = re.findall(ur'Label9">([\u4e00-\u9fa5]+).+?(\d+)',a)
		grade = grade[0][0] + ':' + grade[0][1]
		writQu.put(grade)
		writQu.put('-----------------------------')
		schedule = re.findall(ur'(<tr>[\s\S]+?</tr>)+?',a)
		for x in [2,4,7,9,11]:
			xx = re.findall(ur'<td.*?>(.+?)</td>',schedule[x])
			del xx[0]
			if x in [2,7,11]:
				del xx[0]
			for y in xx:
				writQu.put(y)
		#writQu.put(schedule[2])
		#writQu.put(schedule[4])
		#writQu.put(schedule[7])
		#writQu.put(schedule[9])
		#writQu.put(schedule[11])
		
		endwrit = 1
		writ.join()
		self.run()
		
	def run(self):
		file_path = './'+ self.username + '/sche.txt'
		try:
			f = open(file_path)
		except:
			print '[-] Open sche file fail!'
			self.regular()
			return
		cont = f.read()
		if len(cont) == 0:
			self.regular()
			return
		else:
			self.cont = cont.split('\n')
			for x in range(6):
				print self.cont[x]
			try:
				self.week = sys.argv[2]
				self.input_sche()
			except:
				self.ra_in()
			self.ra_in()
			
	def ra_in(self):
		#
		self.week = raw_input('请输入要查询的星期(1-7):\nPS:如输入0则表示输出所有(输入q则是退出~)\n')
		self.input_sche()
		self.ra_in()
		
	def input_sche(self):
		week = {'1':['|周一',6],'2':['|周二',7],'3':['|周三',8],'4':['|周四',9],'5':['|周五',10],'6':['|周六',11],'7':['|周日',12]}
		i = 0
		
		days = {0:'|#上午	|',2:'|#下午	|',4:'|#晚上	|'}
		if self.week in week:
			o = 0
			print '==========================='
			print week[self.week][0] + '###课程表'
			print '================================='
			for x in xrange(week[self.week][1],41,7):
				if '&nbsp;' in self.cont[x]:
					o += 1
					if o == 5:
						print '|恭喜你～～今天没有课！≡(▔﹏▔)≡'
					continue
				if i != 0:
					print '|================================'
				self.cont[x] = self.cont[x].replace('<br>','\n|')
				if i in days:
					print days[i]
					print '|======================'
				
				print '|' + self.cont[x]
				i += 1
			print '================================='
		elif self.week == '0':
			for x in range(1,8):
				self.week = str(x)
				self.input_sche()
		elif self.week == 'q':
			sys.exit()
		else:
			print '输入错误，请重新输入！\n======================='
		
	
def read_sche(username):
	file_path = './'+ username + '/sche.html'
	f = open(file_path)
	sche = f.read()
	sche = sche.decode()
	wri_sch = write_sche(sche,username)
	wri_sch.run()
	
def run_sche(username):
	print '新学号！'
	password = raw_input('请输入密码：')
	password = md5(password).hexdigest()
	
	log_thread = writeLog(username)
	log_thread.start()
	cook_thread = get_Cook(username,password)
	cook_thread.run()
	login = login_sch(username,password)
	login.run()
	log_thread.join()
	print '[+] Done!'
	read_sche(username)

def run_sche2(username):
	if time.time() - os.stat(username).st_mtime > 2592000:
		run_sche(username)
	else:
		try:
			file_path = './'+ username + '/sche.html'
			f = open(file_path)
		except:
			print '[-] Open file fail!'
			run_sche(username)
		html = f.read()
		f.close()
		if len(html) == 0:
			run_sche(username)
		else:
			read_sche(username)

if __name__ == '__main__':
	print \
r'''
  ____         _      ____  ____         _  ____
 / ___|  ____ | |___ / __ \|  _ \ _   _ | |/ __ \
 \___ \ / ___||  _  |  ___/| | | | | | || |  ___/
  ___) | (___ | | | | |___ | |_| | |_| || | |___
 |__._/ \____||_| |_|\_,__||_,__/\__,__||.|\_,__|
 
 Power By Hc1m1
'''
	try:
		username = sys.argv[1]
	except:
		username = raw_input('请输入学号：')
	if not os.path.isdir(username):
		os.makedirs(username)
		run_sche(username)
	else:
		run_sche2(username)
