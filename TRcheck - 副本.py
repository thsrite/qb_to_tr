import json
import time

import requests
import transmission_rpc


qb_url = "192.168.31.3:8999"
qb_username = ""
qb_password = ""
tr_url = "192.168.31.3"
tr_username = ""
tr_password = ""

print("开始执行\r")
a = time.time()
print("获取QB数据\r")
qb_cookis = requests.get(url="http://"+qb_url+"/api/v2/auth/login", params="username="+qb_username+"&password=" + qb_password, headers={'Referer': 'http://' + qb_url})
qb_tors = requests.get(url="http://"+qb_url+"/api/v2/torrents/info", cookies=qb_cookis.cookies)
qb_hashs = json.loads(qb_tors.text)
print("用时：" + str(int(time.time() - a)) + "\r")
print("获取TR数据\r")
tr_client = transmission_rpc.Client(host=tr_url, port=9091, username=tr_username, password=tr_password)
arge = {"id", "name", "hashString"}
tr_tors = tr_client.get_torrents(arguments=arge)
print("用时：" + str(int(time.time() - a)) + "\r")
print("获数据获取完毕\r")
for qbh in qb_hashs:
    for tr_tor in tr_tors:
        if tr_tor.hashString == qbh["hash"]:
            qb_trak = requests.get(url="http://"+qb_url+"/api/v2/torrents/trackers?hash=" + tr_tor.hashString, cookies=qb_cookis.cookies)
            msgs = json.loads(qb_trak.text)
            for msg in msgs:
                if msg['url'] != '** [LSD] **' and msg['url'] != '** [PeX] **' and msg['url'] != '** [DHT] **':
                    print(qbh["tracker"])
                    try:
                        tr_client.change_torrent(ids=tr_tor.id, trackerAdd=[msg['url']])
                    except Exception as e:
                        print(e)

            break
print("用时：" + str(int(time.time() - a)) + "\r")
print("执行结束\r")
