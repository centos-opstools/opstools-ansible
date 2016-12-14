#!/bin/bash

#Help info
if [ "-h" == $1 ]; then
  echo
  echo
  echo "The command will generate the ~/.opstools.inventory "
  echo "Once the ~/.opstools.inventory is created, a copy of the "
  echo "inventory file is copied and a hosts file is created."
  echo "Then the ansible-playbook will be deployed."
  echo "The inventory directory can be modified setting a"
  echo "OPSTOOLSINVPATH environment variable."
  echo
  echo "By default everything will be installed on localhost."
  echo "It can also be run like $0 REMOTE_IP to install there."
  echo "You can edit manually the ~/.opstools.inventory/hosts file"
  echo "to install the tools on different servers."
  echo
  echo
  echo "* To install everything on localhost:"
  echo "   $0"
  echo
  echo "* To install everything on 192.168.122.125:"
  echo "   $0 192.168.122.125"
  echo
  echo "* To install on differents servers :"
  echo "   export OPSTOOLS_PM_HOST=\"192.168.122.200\"  # Performance  monitoring"
  echo "   export OPSTOOLS_AM_HOST=\"192.168.122.201\"  # Availability monitoring"
  echo "   export OPSTOOLS_LOG_HOST=\"192.168.122.200\" # Centralized  Logging"
  echo "   $0"
  echo
  echo
  exit 0
fi

#Create the local inventory directory for ansible
if ! [ -v OPSTOOLSINVPATH ]; then
 OPSTOOLSINVPATH=$HOME/.opstools.inventory
  if ! [ -d $OPSTOOLSINVPATH ]; then
   echo "Create dir"
   mkdir -p $OPSTOOLSINVPATH
  fi
fi
#Check write access
if ! [ -w $OPSTOOLSINVPATH ]; then
  echo "You do not have permission to write on $OPSTOOLSINVPATH"
  exit 2
fi
OPSTOOLSPATH=`dirname $(readlink -f $0)`

#Copy the needed files
if [ -d $OPSTOOLSINVPATH ]; then
 cp -a $OPSTOOLSPATH/inventory/* $OPSTOOLSINVPATH
 OPSTOOLSINVFILE=$OPSTOOLSINVPATH/hosts
else
 echo "Could not created the $OPSTOOLSINVPATH directory"
 exit 2
fi

#Parse Arguments
if [ "x$1" != "x" ]; then
  HOST=$1
else
  HOST="localhost"
fi

if ! [ -v OPSTOOLS_PM_HOST ]; then
 OPSTOOLS_PM_HOST=$HOST
fi

if ! [ -v OPSTOOLS_AM_HOST ]; then
 OPSTOOLS_AM_HOST=$HOST
fi
if ! [ -v OPSTOOLS_LOG_HOST ]; then
 OPSTOOLS_LOG_HOST=$HOST
fi

CONNECTION=""
for host in $(echo "$OPSTOOLS_PM_HOST $OPSTOOLS_AM_HOST $OPSTOOLS_LOG_HOST"| xargs -n1 | sort -u ) ; do
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
$OPSTOOLS_LOG_HOST

[am_hosts]
$OPSTOOLS_AM_HOST

[pm_hosts]
$OPSTOOLS_PM_HOST

[targets]
$CONNECTION
EOF

echo "File $OPSTOOLSINVFILE created"
fi

#Executes the playbook to install the opstools
ansible-playbook -i $OPSTOOLSINVPATH $OPSTOOLSPATH/playbook.yml

