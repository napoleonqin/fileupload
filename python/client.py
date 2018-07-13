# -*- coding: utf-8 -*
import socket
import os
import json
import sys

def load():
    sk = socket.socket()
    sk.connect(('10.80.25.143', 30089))
    print ('连接服务器成功')
    file_name = input('请输入需要上传文件的文件名：').strip()
    file_size = os.stat(file_name).st_size
    file_point = 0
    print (file_name)
    print (file_size)
    # 文件信息
    send_data = dict(status=0, name=file_name, length=file_size)
    send_json = json.dumps(send_data)
    print (send_json)
    # 发送需上传文件信息
    sk.send((send_json + '\n').encode())
    # 接收服务器返回信息
    recv_data = sk.recv(1024).decode()
    print (recv_data)
    recv_json = json.loads(recv_data)
    print (recv_json)
    # 判断是否断点续传
    if recv_json['status'] == 0:
        print ('文件初次传输！')
        file_point = 0
    elif recv_json['status'] == 1:
        print ('文件已存在，继续传输！')
        file_point = recv_json['length']
    else:
        print ('状态码无效！')
    # 打开文件并传输
    f = open(file_name, 'rb')
    f.seek(file_point)
    while file_point < file_size:
        data = f.read(1024)
        sk.sendall(data)
        file_point += len(data)
        # print ('已发送Byte：' + str(file_point) + '\t' + '文件总Byte：' + str(file_size))
        percent = int(100*(file_point/file_size))
        print ('已发送文件比例：' + str(percent) + '%')
    f.close()
    print ('发送成功！')

while True:
    load()

