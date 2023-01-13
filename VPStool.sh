#VPStool.sh
#一些快速搭建服务器的脚本

echo "1. warp - 为IPv6 only VPS添加IPv4网络接口（新机首步）「必」"
echo "2. x-ui - 支持多用户协议的xray面板（梯子）"

echo "3. 查找python，查看所有安装的版本"
echo "4. 安装pip3"

echo "5. 安装nb-cli"
echo "6. 安装gocq插件"
echo "7. 不挂断地运行bot"

echo "请输入[1-7]："

read cmd

if [ $cmd == 1 ]
then
wget -N https://raw.githubusercontent.com/fscarmen/warp/main/menu.sh && bash menu.sh 
elif [ $cmd == 2 ]
then
bash <(curl -Ls https://raw.githubusercontent.com/vaxilu/x-ui/master/install.sh)
elif [ $cmd == 3 ]
then
whereis python
elif [ $cmd == 4 ]
then
sudo apt update
sudo apt install python3-pip
pip3 --version
elif [ $cmd == 5 ]
then
pip3 install nb-cli
elif [ $cmd == 6 ]
then
nb plugin install nonebot-plugin-gocqhttp
elif [ $cmd == 7 ]
then
cd ~/bot
nohup python3 bot.py >/dev/null 2>&1 &
else
echo "认真输入了吗？"
fi 
