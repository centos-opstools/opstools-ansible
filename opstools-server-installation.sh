#!/bin/bash

#Help info
if [ "-h" == $1 ]; then
  echo 
  echo
  echo "The command will generate the ~/.opstools.hosts file"
  echo "Once the ~/.opstools.hosts file is created, the"
  echo "ansible-playbook will be deployed"
  echo
  echo "By default everything will be installed on localhost"
  echo "It can also be run like $0 REMOTE_IP to install there"
  echo "You can edit manually the ~/.opstools.hosts file to install the tools on different servers"
  echo 
  echo 
  echo "* To install everything on localhost:"
  echo "   $0"
  echo 
  echo "* To install everything on 192.168.122.125:"
  echo "   $0 192.168.122.125"
  echo 
  exit 0
fi
 
OPSTOOLSINVFILE="$HOME/.opstools.hosts"
OPSTOOLSPATH=`dirname $(readlink -f $0)`

if [ "x$1" != "x" ]; then
  HOST=$1
else
  HOST="localhost"
fi

if ! [ -v PM_HOST ]; then
 PM_HOST=$HOST
fi

if ! [ -v AM_HOST ]; then
 AM_HOST=$HOST
fi
if ! [ -v LOG_HOST ]; then
 LOG_HOST=$HOST
fi

CONNECTION=""
for host in $(echo "$PM_HOST $AM_HOST $LOG_HOST"| xargs -n1 | sort -u ) ; do
 if [ "localhost" == $host ]; then
  CONNECTION=$CONNECTION"localhost ansible_connection=local
"
 else
   CONNECTION=$CONNECTION"$host ansible_connection=ssh ansible_user=root
"
 fi
done


if [ ! -f $OPSTOOLSINVFILE ]; then
cat <<EOF > $OPSTOOLSINVFILE
[logging_hosts]
$LOG_HOST
[am_hosts]
$AM_HOST
[pm_hosts]
$PM_HOST

[targets]
$CONNECTION
EOF

echo "File $OPSTOOLSINVFILE created"
fi

#Executes the playbook to install the opstools
ansible-playbook -i $OPSTOOLSPATH/inventory -i $OPSTOOLSINVFILE $OPSTOOLSPATH/playbook.yml

