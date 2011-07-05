#!/bin/bash -x

export HOME="/root"

IS_MASTER=%IS_MASTER%

apt-add-repository "deb http://www.rabbitmq.com/debian/ testing main"
wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
apt-key add rabbitmq-signing-key-public.asc
apt-get update
yes | apt-get install rabbitmq-server

rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl stop
s3cmd get --force s3://silverline/.erlang.cookie /var/lib/rabbitmq/.erlang.cookie

if [ $IS_MASTER -ne 1 ]; then
  cat << EOF > /etc/rabbitmq/rabbitmq.config
[{rabbit, [{cluster_nodes, ['%RABBIT_MASTER%']}]}].
EOF
fi


sleep 10
rabbitmq-server -detached
