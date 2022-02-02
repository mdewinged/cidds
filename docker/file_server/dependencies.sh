#!/bin/bash

# Update
until apt-get -y --error-on=any update 2> /tmp/apt-get-update-error
do
  echo "Error on apt-get update"
done
apt upgrade -y

# Download basic packages 
#declare -a versionsAptGet=("=2.0.6" "" "=1.3-20190808-1" "=3.0pl1-136ubuntu1" "=0.99.9.8" "=0.8.12-1ubuntu4" "=1:8.2p1-4ubuntu0.3" "" "" "" "" "")
declare -a packagesAptGet=("apt-utils" "sudo" "dialog"  "cron" "software-properties-common" "aptitude"       "ssh"                "nano" "iptables" "net-tools" "iproute2" "iputils-ping")
count=${#packagesAptGet[@]}
for i in `seq 1 $count` 
do
  until dpkg -s ${packagesAptGet[$i-1]} | grep -q Status;
  do
    #RUNLEVEL=1 apt install -y --no-install-recommends ${packagesAptGet[$i-1]}${versionsAptGet[$i-1]}
    RUNLEVEL=1 apt install -y --no-install-recommends ${packagesAptGet[$i-1]}
  done
  echo "${packagesAptGet[$i-1]} found."
done

# Solve problems on installing cups:
## 1.1 Policy-rc.d not permit start process on reboot
printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d
## 1.2 Failed to create symbolic link em /etc/resolv.conf https://stackoverflow.com/questions/40877643/apt-get-install-in-ubuntu-16-04-docker-image-etc-resolv-conf-device-or-reso
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
echo "resolvconf resolvconf/linkify-resolvconf boolean false" | debconf-set-selections
until dpkg -s resolvconf | grep -q Status;
do
  RUNLEVEL=1 apt install -y --no-install-recommends resolvconf=1.82
done
apt-get update

# Define the packets to install with apt-get 
until dpkg -s samba | grep -q Status;
do
#RUNLEVEL=1 apt install -y --no-install-recommends samba=2:4.13.14+dfsg-0ubuntu0.20.04.2
RUNLEVEL=1 apt install -y --no-install-recommends samba
done
