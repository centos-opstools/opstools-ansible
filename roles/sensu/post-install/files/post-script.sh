#!/bin/bash

CIRROS_URL='http://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img'
CIRROS_NAME='cirros'
CIRROS_FILE='cirros-0.3.0-x86_64-disk.img'
FLAVOR_NAME='m1.tiny'
NETWORK_CIDR='192.168.7.0/24'

source /home/stack/overcloudrc

if [ -f $CIRROS_NAME ];then
 rm -rf $CIRROS_NAME
fi

curl --silent -L -O $CIRROS_URL

TEST_IMG=`glance image-list  | grep $CIRROS_NAME | wc -l`

if ! [ 1 -eq $TEST_IMG ]; then
  # upload and create the cirros image
  glance image-create --name $CIRROS_NAME --min-disk 1 --visibility public --os-distro cirros --owner admin --min-ram 512 --disk-format raw --file $CIRROS_FILE --container-format bare
fi

TEST_FLAVOR=`nova flavor-list | grep $FLAVOR_NAME | wc -l `

if ! [ 1 -eq $TEST_FLAVOR ]; then
  # Create the m1.tiny flavor
  nova flavor-create  $FLAVOR_NAME auto 512 1 1
fi

TEST_NET=`neutron net-list | grep public | wc -l`

if ! [ 1 -eq $TEST_NET ]; then
 # Create the public network
 neutron net-create public --shared --router:external True
fi

TEST_SUBNET=`neutron subnet-list | grep public-subnet | wc -l`

if ! [ 1 -eq $TEST_SUBNET ]; then
 # Create the public subnet
 neutron subnet-create --name public-subnet --enable-dhcp  public $NETWORK_CIDR
fi
