#!/bin/bash

# start mqnamesrv service
nohup $ROCKETMQ_HOME/bin/mqnamesrv > /dev/null 2>&1 &
echo "启动：mqnamesrv"

# start mqbroker service
nohup $ROCKETMQ_HOME/bin/mqbroker -n localhost:9876 > /dev/null 2>&1 &
echo "启动：mqbroker"

# start console service
cd $CONSOLE_HOME
nohup  java -jar rocketmq-console.jar > /dev/null 2>&1 &
echo "启动：console"
echo ""
echo "Console帐号以及密码"
echo "帐号：admin   密码：admin"
echo "帐号：normalt 密码：normal"

echo ''
echo ' _____            _        _     __  __  ____  '
echo '|  __ \          | |      | |   |  \/  |/ __ \ '
echo '| |__) |___   ___| | _____| |_  | \  / | |  | |'
echo '|  _  // _ \ / __| |/ / _ \ __| | |\/| | |  | |'
echo '| | \ \ (_) | (__|   <  __/ |_  | |  | | |__| |'
echo '|_|  \_\___/ \___|_|\_\___|\__| |_|  |_|\___\_\'
echo ''
echo "🚀版本：$ROCKETMQ_VERSION"
echo "🦄作者：徐承恩"
echo "📧邮箱：xuchengen@gmail.com"
echo "🐵github：https://github.com/Xuchengen/rocketmq-docker-build"
echo ""

# foreground process
tail -f /dev/null