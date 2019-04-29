#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import json
import time
import re
import base64
from bs4 import BeautifulSoup
from threading import Thread
import datetime
from django.conf import settings

def handler():
    data_respone=[]
    try:
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        data = {
            "password": settings.ZABBIX_PASSWORD,
            "name": settings.ZABBIX_USER,
            "enter": "Sign in",
            "autologin": 1
        }
        login_url = "{0}index.php".format(settings.ZABBIX_URL)
        respone = s.post(url=login_url, data=data, headers=headers)
        cookies = s.cookies.get_dict()
        sid = cookies['zbx_sessionid'][-16:]
        auth = cookies['zbx_sessionid']
        headers = {
            'Content-type': 'application/json-rpc',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': '{0}zabbix.php?action=dashboard.view'.format(settings.ZABBIX_URL),
            'Origin': '{0}'.format(settings.ZABBIX_URL),
            'X-Prototype-Version': '1.6.1',
        }
        # data = {"jsonrpc": "2.0", "method": "message.settings", "params": {}, "auth": auth, "id": 1}
        # respone = s.post(url='http://172.16.7.145/zabbix/jsrpc.php?output=json-rpc', data=json.dumps(data), headers=headers)
        # upd_counter = json.loads(respone.text).get('id', None)  # 获取id
        upd_counter = 0
        data = {
            'widgetRefresh': 'lastiss',
            '_:': '',
        }
        #
        #baseurl = "http://172.16.7.145/zabbix/zabbix.php?action=widget.system.view&sid={0}&upd_counter={1}&pmasterid=dashboard".format(sid, upd_counter)
        baseurl = "{url}zabbix.php?action=widget.issues.view&sid={0}&upd_counter={1}&pmasterid=dashboard".format(sid, upd_counter,url=settings.ZABBIX_URL)
        respone = s.post(url=baseurl, data=data, headers=headers)
        html = json.loads(respone.text).get('body', None)
        soup = BeautifulSoup(html, features="html.parser")
        tages = soup.select("span[data-menu-popup]")
        data_list = []
        data_list_tmp=[]
        for line in tages:
            hostid=json.loads(line.get('data-menu-popup')).get('hostid', None)
            hostname=line.text
            item_keyt = ''
            numt=''
            try:
                alarm_msg = re.search(r'"max-width: 500px"\);\'>(.*)<span style="display: none;">',str(line.parent.next_sibling.select('.link-action')[0])).groups()
                alarm_msg=alarm_msg[0].strip()
                alarm_time=line.parent.next_sibling.next_sibling.text.strip()
                if re.match(r'^(Free|Total)', alarm_msg) and "Physical Memory" not in alarm_msg:
                    numt,item_keyt= re.search('than(.*)on\s+volume(.*)', alarm_msg).groups()
                    numt = 'less {0}'.format(numt.strip())
            except Exception:
                continue
            if item_keyt and numt:
                pass
            else:
                continue
            data_list_tmp.append([hostname, hostid, numt, item_keyt, alarm_time,sid])
        def get_graphid(hostname, hostid, numt, item_keyt, alarm_time,sid):
            url = '{url}charts.php?hostid={0}&sid={1}'.format(hostid, sid,url=settings.ZABBIX_URL)
            respone = s.get(url=url, headers=headers)
            result = BeautifulSoup(respone.text, features="html.parser")
            tages = result.select('#graphid option')
            for tage in tages:
                rest = tage.text
                tmp='{0} strip'.format(item_keyt.strip())
                if  tmp in rest and 'boot' not in rest and 'shm' not in rest and "OracleLinux" not in rest and "ICBC" not in rest:
                    graphid = tage.attrs['value']
                    data_list.append([hostname, hostid, graphid, numt, item_keyt, alarm_time])
                    # print(hostname,hostid, alarm_time, alarm_msg, numt, item_keyt, graphid)
        res_1 = []
        for hostname, hostid, numt, item_keyt, alarm_time,sid in data_list_tmp:
            t1 = Thread(target=get_graphid, args=(hostname, hostid, numt, item_keyt, alarm_time,sid))
            res_1.append(t1)
            t1.start()
        for t1 in res_1:
            t1.join()

        graphid_url_list = []
        stime=(datetime.datetime.now() + datetime.timedelta(-7)).strftime("%Y%m%d%H%M%S")
        period=7*24*60*60
        def get_page(host, hostid, graphid, numt, key, times, url):
            respone = s.get(url, headers=headers)
            if respone.status_code == 200:
                html = respone.text
                graphid_url = re.search(r'\"src\":\'(.*)\',\"objDims', html).groups()[0]
                if 'stime' in graphid_url and 'period' in graphid_url:
                    graphid_url=re.sub('stime=\d+','stime={0}'.format(stime),graphid_url)
                    graphid_url=re.sub('period=\d+','period={0}'.format(period),graphid_url)
                graphid_url_list.append((host, hostid, graphid, numt, key, times, graphid_url))

        res_1 = []
        for host, hostid, graphid, numt, key, times in data_list:
            url = "{url}charts.php?fullscreen=0&groupid=0&hostid={0}&graphid={1}".format(hostid,graphid,url=settings.ZABBIX_URL)
            t1 = Thread(target=get_page, args=(host, hostid, graphid, numt, key, times, url))
            res_1.append(t1)
            t1.start()
        for t1 in res_1:
            t1.join()
        def work(host, hostid, graphid, numt, key, times, graphid_url):
            url = '{url}'.format(url=settings.ZABBIX_URL) + graphid_url
            respone = s.get(url=url, headers=headers)
            # print(host,numt, key,times,url,respone.content)
            # path = 'tmp/' + str(hostid) + '.jpg'
            # with open(path, 'wb') as f:
            #     f.write(respone.content)

            data_respone.append((host, hostid, graphid, numt, key, times,base64.b64encode(respone.content)))

        res_l = []
        for host, hostid, graphid, numt, key, times, graphid_url in graphid_url_list:
            t1 = Thread(target=work, args=(host, hostid, graphid, numt, key, times, graphid_url,))
            res_l.append(t1)
            t1.start()
        for t in res_l:
            t.join()
        data_respone=sorted(data_respone, key=lambda data_respone: time.mktime(time.strptime(data_respone[5], '%Y-%m-%d %X')),reverse=True)
        return data_respone
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    rest=handler()
    print(rest)
