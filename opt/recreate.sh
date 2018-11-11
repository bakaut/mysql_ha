#!/bin/bash
#set -x
systemctl stop mysqld
rm -rf /var/lib/mysql/*
> /var/log/mysqld.log
systemctl start mysqld
pass=`tail -10000 /var/log/mysqld.log | grep "temporary password" | awk '{print $13}'`
echo $pass

query="SET sql_log_bin=OFF;set global super_read_only=OFF;ALTER USER 'root'@'localhost' IDENTIFIED BY '7,Agf5Cupp0E,';update mysql.user set Host='%' where user='root';flush privileges;set global super_read_only=ON;SET sql_log_bin=ON"

echo "${query}"
mysql --connect-expired-password -p"${pass}" -e "${query}"
systemctl restart mysqld
