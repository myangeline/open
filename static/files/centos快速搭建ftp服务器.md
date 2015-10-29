# centos快速搭建ftp服务器

## 安装vsftpd
	
	$ yum -y install vsftpd
	
## 编辑vsftpd配置文件

	$ vim /etc/vsftpd/vsftpd.conf
	
加入以下配置：
	
	listen=YES
	background=YES
	anonymous_enable=NO
	local_enable=YES
	write_enable=YES
	local_umask=022
	anon_upload_enable=NO
	anon_mkdir_write_enable=NO
	dirmessage_enable=YES
	xferlog_enable=YES
	connect_from_port_20=YES
	chown_uploads=NO
	xferlog_file=/var/log/vsftpd.log
	xferlog_std_format=YES
	async_abor_enable=YES
	ascii_upload_enable=YES
	ascii_download_enable=YES
	ftpd_banner=Welcome to hao32 FTP servers
	pam_service_name=vsftpd
	chroot_local_user=NO
	chroot_list_enable=YES
	chroot_list_file=/etc/vsftpd/vsftpd.chroot_list
	
## 启动vsftpd
	
	$ touch /etc/vsftpd/vsftpd.chroot_list
	$ service vsftpd start
	
如果出现	Starting vsftpd for vsftpd:                                [  OK  ] 则表示成功

如果不行则使用下面的命令：
	
	$ /etc/rc.d/init.d/xinetd restart
	
	
## 创建独立用户登录ftp

	$ useradd sun -d /home/sun -s /sbin/nologin

此用户指向目录 /home/sun ，权限是nologin，就是没给shell权限，不影响ftp的使用

## 设置目录及其文件的属组
	
	$ # chown -R sun.sun /home/sun

就是将 /home/sun 目录及其下的文件设置为sun所属

## 设置用户密码

	$ passwd sun

之后根据提示输入密码即可

## 把用户sun加到/etc/vsftpd/vsftpd.chroot_list里

	$ echo 'sun' >> /etc/vsftpd/vsftpd.chroot_list

这样用户就可以正常登陆并且不能跳出自己的目录

## 重启vsftpd服务
	$ service vsftpd restart
	
## 开启ftp_home_dir
如果在登录过程出现 “响应:	500 OOPS: cannot change directory:/home/ssftp” 错误，执行：
	
	$ setsebool ftp_home_dir on

使用下面命令:
	
	$ sestatus -b| grep ftp
	
可以查看关于ftp的一些权限状态，默认的都是off，所以需要执行上面的命令进行开启