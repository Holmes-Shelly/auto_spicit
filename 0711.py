  #-*- coding:utf-8 -*-
import requests
import json
import time

def update():
	url_auth = "https://interface5.spicit.com.cn/api/v1.0/sysUser/login?mobile=18663187969&password=48af1eaba8b08cfe28a2467b17d0cdd7"
	url_save = "https://interface5.spicit.com.cn/api/v1.0/healthFill/save"
	url_getdata = "https://interface5.spicit.com.cn/api/v1.0/healthFill/findDataByOrgCodeOrUserName"

	req = requests.session()

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
	
	#模拟登陆的同时获取token，更新headers_save
	token = req.get(url_auth, headers = headers_auth).json()["data"]["token"]
	headers_save['Authorization'] = '18663187969 ' + token
	print(headers_save['Authorization'])

	data_lastday = {"fillUserid":"4c33a327a506b9480764bc5dcd08f84c",}
	data_lastday["fillDate"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	
	data = req.post(url_getdata, headers = headers_save, data = json.dumps(data_lastday)).json()
	
	'''
	data = {"orgCode":"d24a0ea4f21e4cdabb693ea9d730c83d","fillUsername":"石昊","fillUserid":"4c33a327a506b9480764bc5dcd08f84c","fillAccount":"18663187969","isLeaveCompany":"否","destination":"","leaveTime":"","leaveWay":"","leaveTraffic":"","backTime":"","backWay":"","otherOverseas":"否","otherBackTime":"","backTraffic":"","isStay":"否","isOverseas":"否","isContact":"否","currentLocation":"国和一号生活区","currentHealthState":"正常","isWorking":"是","workingWay":"自驾","otherWorkingWay":"","workingWayTaxiStartDate":"","workingWayTaxiEndDate":"","workingWayTaxiNum":"","workingWayBusStartDate":"","workingWayBusEndDate":"","workingWayBusNum":"","homeWay":"自驾","otherHomeWay":"","homeWayTaxiStartDate":"","homeWayTaxiEndDate":"","homeWayTaxiNum":"","homeWayBusStartDate":"","homeWayBusEndDate":"","homeWayBusNum":"","morningTemp":"35.9","takeTogetherDate":"","contactDetail":"","fillDate":"2020-07-11","nowPlace":"中国大陆"}

	data["morningTemp"] = "36.0"

	result = req.post(url_save, headers = headers_save, data = json.dumps(data))
	print(result)
	'''
	
	return
	
def update_cycle():
	while(1):
		time_hour = int(time.strftime('%H',time.localtime(time.time())))

		time_delay = (31 - time_hour) * 3600
		
		try:
			print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			update()
		except requests.exceptions.ConnectionError as ErrorAlert:
			print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			print(ErrorAlert)
			update()
		time.sleep(time_delay)
	return

update_cycle()
