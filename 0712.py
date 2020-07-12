  #-*- coding:utf-8 -*-
import requests
import json
import time
import hashlib

def update():
	account_lib = {"18663187969":"shihao1992", "18663187965":"li121452",}
	url_spicit = "https://interface5.spicit.com.cn/api/v1.0/"
	
	url_auth = url_spicit + "sysUser/login?"
	url_save = url_spicit + "healthFill/save"
	url_getdata = url_spicit + "healthFill/findDataByOrgCodeOrUserName"
	
	time_today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	time_lastday = time.strftime('%Y-%m-%d',time.localtime(time.time() - 3600 * 24))
	sess = requests.session()

	headers_auth = {
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en,zh;q=0.9,zh-CN;q=0.8,lb;q=0.7',
	'Connection':'keep-alive',
	'Host':'interface5.spicit.com.cn',
	'Sec-Fetch-Mode':'cors',
	'Sec-Fetch-Site':'same-origin',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',
	}

	headers_save = headers_auth.copy()
	headers_save['Content-Length'] = '944'
	headers_save['Content-Type'] = 'application/json'

	for account in account_lib:
		#模拟登陆的同时获取token，更新headers_save
		md5_pwd = hashlib.md5()
		md5_pwd.update(account_lib[account])
		msg = sess.get(url_auth + "mobile=" + account + "&password=" + md5_pwd.hexdigest(), headers = headers_auth).json()["data"]
		headers_save['Authorization'] = account + ' ' + msg["token"]
		print(headers_save['Authorization'])

		get_data_lastday = {}
		get_data_lastday["fillUserid"] = msg["id"]
		get_data_lastday["fillDate"] = time_lastday
		
		data_lastday = sess.post(url_getdata, headers = headers_save, data = json.dumps(get_data_lastday)).json()["data"][0]
		
		#print(data_lastday)
		
		data_today = {"orgCode":"","fillUsername":"","fillUserid":"","fillAccount":"","isLeaveCompany":"否","destination":"","leaveTime":"","leaveWay":"","leaveTraffic":"","backTime":"","backWay":"","otherOverseas":"否","otherBackTime":"","backTraffic":"","isStay":"否","isOverseas":"否","isContact":"否","currentLocation":"","currentHealthState":"正常","isWorking":"是","workingWay":"自驾","otherWorkingWay":"","workingWayTaxiStartDate":"","workingWayTaxiEndDate":"","workingWayTaxiNum":"","workingWayBusStartDate":"","workingWayBusEndDate":"","workingWayBusNum":"","homeWay":"自驾","otherHomeWay":"","homeWayTaxiStartDate":"","homeWayTaxiEndDate":"","homeWayTaxiNum":"","homeWayBusStartDate":"","homeWayBusEndDate":"","homeWayBusNum":"","morningTemp":"35.9","takeTogetherDate":"","contactDetail":"","fillDate":"","nowPlace":""}
		for item in data_today:
			if(data_lastday[item]):
				data_today[item] = data_lastday[item]
		
		#data_today = data_lastday.copy()
		data_today["fillDate"] = time_today
		data_today["morningTemp"] = "35.5"
		print(json.dumps(data_today))

		result = sess.post(url_save, headers = headers_save, data = json.dumps(data_today))
		print(result)
		
		sess.close()
	
	return
	

update()
