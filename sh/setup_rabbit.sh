#!/bin/bash -x

apt-add-repository "deb http://www.rabbitmq.com/debian/ testing main"
wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
apt-key add rabbitmq-signing-key-public.asc
apt-get update
yes | apt-get install rabbitmq-server

rabbitmqctl stop
s3cmd get --force s3://silverline/.erlang.cookie /var/lib/rabbitmq/.erlang.cookie
rabbitmq-server -detached
