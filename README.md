<h1 align="center">W01f-ssh-crack</h1>  
<div align="center">一款综合性的ssh爆破工具，支持任意IP，不需要电脑里面事先存有key</div>

# :sunny:声明

1. 本程序仅供学习交流，若用本程序行违法之事，后果自负。
2. 在此非常感谢[刘江的博客教程](https://www.liujiangblog.com/)，他的简洁易懂的文字让我快速了解了如何用paramiko实现Python内的ssh功能，具体文章地址：https://www.liujiangblog.com/blog/15/ 。
3. 在写程序的过程中，我也参考了官方的一些文档资料，在https://docs.paramiko.org/en/stable/api/client.html 中我了解了`set_missing_host_key_policy(paramiko.WarningPolicy())`这个方法，可以让我实现不需要本地有`key`就可以连接对方的`ssh`（只用账号密码登录的时候），这一点我写完之后看其他人的代码的时候并没有发现。

# :foggy:如何使用：

1. 先填写`data.conf`，参数说明：
  
  | 参数  | 说明  |
  | --- | --- |
  | `sender` | 发送人的QQ邮箱，例如`xxxxxx@qq.com` |
  | `pw` | 在`https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256`可以查看，注意填写的是授权码，不是QQ邮箱密码。 |
  | `receivers` | 接收人的QQ邮箱，例如`xxxxxxxx@qq.com` |
  

2. 本程序的`1.0`版本提供了三种选择，分别是`-C`、`-R`、`-T`：
  
  | 参数  | 说明  |
  | --- | --- |
  | `-C` | 采用`sshclient`+账号密码的方式登录（爆破账号密码） |
  | `-R` | 采用`sshclient`+公钥秘钥的方式登录（爆破密码） |
  | `-T` | 采用`sftp`上传、下载文件（爆破账号密码） |
  

3. 本程序提供两个参数：
  

        ①以上的三种选择三选一；

        ②IP地址。

        使用示例为：

```python
python W01f-ssh-crack.py -C 192.168.137.150
```

4. 须确保您的`data.conf`、`W01f-ssh-crack.py`、`username.txt`、`password.txt`在同一目录下。

5. 目前已写好的代码里面邮件发送功能只支持`QQ`邮箱，您也可以自行改成其他的，如`smtp.gmail.com`、端口`587`，详情请参考网上的教程。

6. 如果您在使用中遇到任何问题，您有两种途径可以反馈：
  
    ①mailto:[sharecat2022@gmail.com](mailto:sharecat2022@gmail.com)
  
    ②https://github.com/W01fh4cker/W01f-ssh-crack/issues
