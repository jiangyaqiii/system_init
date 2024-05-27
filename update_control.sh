#!/bin/bash
cd ~/system_init
git checkout -- control.py
git checkout -- init.sh
git pull

##杀死此服务
# 检查用户是否输入端口号
port=80 ##程序版本
# 查看当前端口是否有服务占用
# 显示第二行到最后一行($代表最后一行)并去重
allPid=$(echo `lsof -i:$port|awk '{print $2}'|sed -n '2,$p'|sort -u`)
echo "Service pid: " $allPid
# 显示所有行数,去除字符串中空格并将字符串转为int
lines=$(echo $allPid | wc -l | sed 's/[[:space:]]//g' | awk '{print int($0)}')
# 循环杀死服务下所有PID
isSuccess=0
for (( i=1; i <= $lines; i++ ))
do
    kill -9 $(echo $allPid | sed -n $i'p')
    # 判断上条命令执行是否成功
    if [[ $? == 0 ]]
    then
        let isSuccess+=1
    fi
done

##启动脚本
sh init.sh
# 删除此脚本
cd ~
rm -f update_control.sh
