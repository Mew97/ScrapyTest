echo 'nameserver 202.103.24.68' >> /etc/resolv.conf
echo 'nameserver 202.103.0.117' >> /etc/resolv.conf
systemctl restart network

hostnamectl set-hostname --static cdh5
echo  "192.168.2.31 cdh1" >> /etc/hosts
echo  "192.168.2.32 cdh2" >> /etc/hosts
echo  "192.168.2.33 cdh3" >> /etc/hosts
echo  "192.168.2.34 cdh4" >> /etc/hosts
echo  "192.168.2.35 cdh5" >> /etc/hosts


echo '安装工具中...'
yum install -y tmux ntp psmisc perl expect vim

timedatectl set-timezone "Asia/Shanghai"
ntpdate us.pool.ntp.org
clock -w
systemctl restart ntpd
systemctl enable ntpd
date

setenforce 0
sed -i 's/^SELINUX=.*/SELINUX=disabled/g'   /etc/selinux/config
sed -i 's/^SELINUX=.*/SELINUX=disabled/g'   /etc/sysconfig/selinux

reboot

########### ssh ############
# startautoSSH.sh
# autoSSH.sh
# 拷贝jdk cloudera.tar
########### ssh ############

mkdir -p /usr/java
echo '解压中...'
tar -zxf /home/jdk-8u25-linux-x64.tar.gz -C /usr/java/
echo 'export JAVA_HOME=/usr/java/jdk1.8.0_25' >> /etc/profile
echo 'export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar' >> /etc/profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile
source /etc/profile
java -version

### 主节点
yum -y install  mariadb-server   mariadb
systemctl start mariadb.service
systemctl enable mariadb.service
mysql -uroot -p

use mysql;
update user  set  password=password('123456') where user= 'root';
grant all privileges on *.* to root@'%' identified by '123456';
grant all privileges on *.* to root@'cdh1' identified by '123456';
grant all privileges on *.* to root@'localhost' identified by '123456';
FLUSH PRIVILEGES;
exit;

cp /etc/my.cnf /etc/my.cnf.bak
vim  /etc/my.cnf

character_set_server = utf8

systemctl restart mariadb.service
mysql -uroot -p

create database hive DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
create database amon DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
create database hue DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
create database monitor DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
create database oozie DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
create database reports DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

CREATE USER 'hive'@'localhost' IDENTIFIED BY 'hive';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'localhost';
CREATE USER 'hive'@'%' IDENTIFIED BY 'hive';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%';
CREATE USER 'hive'@'cdh1'IDENTIFIED BY 'hive';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'cdh1';

CREATE USER 'oozie'@'localhost' IDENTIFIED BY 'oozie';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'localhost';
CREATE USER 'oozie'@'%' IDENTIFIED BY 'oozie';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'%';
CREATE USER 'oozie'@'cdh1'IDENTIFIED BY 'oozie';
GRANT ALL PRIVILEGES ON oozie.* TO 'oozie'@'cdh1';

CREATE USER 'monitor'@'localhost' IDENTIFIED BY 'monitor';
GRANT ALL PRIVILEGES ON monitor.* TO 'monitor'@'localhost';
CREATE USER 'monitor'@'%' IDENTIFIED BY 'monitor';
GRANT ALL PRIVILEGES ON monitor.* TO 'monitor'@'%';
CREATE USER 'monitor'@'cdh1'IDENTIFIED BY 'monitor';
GRANT ALL PRIVILEGES ON monitor.* TO 'monitor'@'cdh1';

CREATE USER 'reports'@'localhost' IDENTIFIED BY 'reports';
GRANT ALL PRIVILEGES ON reports.* TO 'reports'@'localhost';
CREATE USER 'reports'@'%' IDENTIFIED BY 'reports';
GRANT ALL PRIVILEGES ON reports.* TO 'reports'@'%';
CREATE USER 'reports'@'cdh1'IDENTIFIED BY 'reports';
GRANT ALL PRIVILEGES ON reports.* TO 'reports'@'cdh1';
FLUSH PRIVILEGES;
exit;

######

yum -y install mysql-connector-java

tar -zxf /home/cloudera-manager-centos7-cm5.7.2_x86_64.tar.gz -C /opt/
useradd --system --home=/opt/cm-5.7.2/run/cloudera-scm-server --no-create-home --shell=/bin/false --comment "Cloudera SCM User" cloudera-scm
usermod -aG wheel cloudera-scm
sed -i "s/^server_host=.*/server_host=cdh1/g" /opt/cm-5.7.2/etc/cloudera-scm-agent/config.ini
cat  /opt/cm-5.7.2/etc/cloudera-scm-agent/config.ini|grep  server_host
ln -s  /usr/share/java/mysql-connector-java.jar /opt/cm-5.7.2/share/cmf/lib/mysql-connector-java.jar
mkdir -p /opt/cloudera/parcels
chown cloudera-scm:cloudera-scm /opt/*

##### 主节点
mkdir /var/cloudera-scm-server
chown -R cloudera-scm:cloudera-scm /var/cloudera-scm-server
chown -R cloudera-scm:cloudera-scm /opt/cloudera*

#### 拷贝cdh资源

#### 修改py文件 # if len(line.rstrip().split(" "))<=4:
vim /opt/cm-5.7.2/lib64/cmf/agent/build/env/lib/python2.7/site-packages/cmf-5.7.2-py2.7.egg/cmf/client_configs.py

scp /opt/cm-5.7.2/lib64/cmf/agent/build/env/lib/python2.7/site-packages/cmf-5.7.2-py2.7.egg/cmf/client_configs.py root@cdh5:/opt/cm-5.7.2/lib64/cmf/agent/build/env/lib/python2.7/site-packages/cmf-5.7.2-py2.7.egg/cmf/

####
/opt/cm-5.7.2/share/cmf/schema/scm_prepare_database.sh mysql -hcdh1 -uroot -p123456 --scm-host cdh1 scmdbn scmdbu scmdbp

/opt/cm-5.7.2/etc/init.d/cloudera-scm-server start
/opt/cm-5.7.2/etc/init.d/cloudera-scm-agent start

echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo "vm.swappiness=0" >> /etc/sysctl.conf
sysctl -p
cat /proc/sys/vm/swappiness

######################

startautoSSH.sh
#!/bin/bash

## 配置 SSH 免密登录的服务器列表，可写死，也可通过传参或者读配置文件的方式读取
#BASE_HOST_LIST="node001 node002 node003"
BASE_HOST_LIST="cdh2 cdh3 cdh4 cdh5"

## 脚本的放置目录（传送之前，和传送之后都是这个目录）
SCRIPT_PATH="/root/autoSSH.sh"

## 第一步：先让自己先跑 startautoSSH.sh 脚本，为了能顺利发送脚本到集群各节点
sh ${SCRIPT_PATH} ${BASE_HOST_LIST}

## 第二步：把脚本发送给其他服务器，让其他服务器也执行该脚本
for SSH_HOST in $BASE_HOST_LIST
do
    ## first : send install script
    ## 注意这行，用户名写死为root，如果是其他用户，记得在这里修改
    scp -r $SCRIPT_PATH root@${SSH_HOST}:$SCRIPT_PATH
    ## send command and generate ssh and auto ssh
    ssh ${SSH_HOST} sh ${SCRIPT_PATH} ${BASE_HOST_LIST}
done
