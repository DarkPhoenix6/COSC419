#!/usr/bin/env bash

if [[ "$(cat /proc/version)" =~ .*"Red Hat".* ]]; then
	#centos7
    sudo yum install python-pip
    sudo pip install --upgrade pip
    sudo pip install flask
    if [[ ! -f /etc/yum.repos.d/passenger.repo ]]; then
        sudo curl --fail -sSLo /etc/yum.repos.d/passenger.repo https://oss-binaries.phusionpassenger.com/yum/definitions/el-passenger.repo
    fi
    sudo yum install -y mod_passenger || sudo yum-config-manager --enable cr && sudo yum install -y mod_passenger
    sudo service httpd restart
    sudo mkdir /var/www/lab8
    yes | sudo \cp -r ./ /var/www/lab8
    sudo mv /var/www/lab8/MyApp.conf /etc/httpd/conf.d/
    sudo chown -R root:root /var/www/lab8
    sudo chcon -v --type=httpd_sys_content_t /var/www/lab8
    sudo chcon -v --type=httpd_sys_content_t /var/www/lab8/*
    sudo chcon -v --type=httpd_sys_content_t /var/www/lab8/*/*
    sudo service httpd restart
fi
exit