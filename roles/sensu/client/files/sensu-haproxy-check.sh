#!/bin/bash

CHECK_AUTH=$1
CHECK_HA_IP=$2
CHECK_SENSU_URI=$3

#Get the data from the haproxy
CURL_DATA=`curl -u $CHECK_AUTH "$CHECK_HA_IP/haproxy?stats;csv" 2>/dev/null`
CURL_RESULT=`echo $?`

#Check that the curl command had succeded
if [ "$CURL_RESULT" != "0" ]; then
   echo "Could not get the haproxy stats:::$CURL_RESULT"
   exit 2
fi


#Insert data by service
echo "$CURL_DATA" | awk -F, '{ {STATUS="3";STATUS_STR="UNKNOWN";}  switch($18) { case "UP":case "OPEN":{STATUS="0";STATUS_STR="OK";} break; case "DOWN": case "DOWN 1/2":{ STATUS="2"; STATUS_STR="ERROR";} break; default: {STATUS="2";STATUS_STR="ERROR";} break}; print "{\"source\":\""$1"\",\"name\":\""$2"\",\"output\":\""STATUS_STR" : "$18"\",\"status\":"STATUS"}"}' | xargs -r -0 -I R -d"\n"   curl -s -i -X POST -H 'Content-Type: application/json' -d "R" $CHECK_SENSU_URI/results > /dev/null
SERVICE_RESULT=`echo $?`

#Insert data by Node
echo "$CURL_DATA" | awk -F, '{ {STATUS="3";STATUS_STR="UNKNOWN";}  switch($18) { case "UP":case "OPEN":{STATUS="0";STATUS_STR="OK";} break; case "DOWN": case "DOWN 1/2":{ STATUS="2"; STATUS_STR="ERROR";} break; default: {STATUS="2";STATUS_STR="ERROR";} break}; print "{\"source\":\""$2"\",\"name\":\""$1"\",\"output\":\""STATUS_STR" : "$18"\",\"status\":"STATUS"}"}' | xargs -r -0 -I R -d"\n"   curl -s -i -X POST -H 'Content-Type: application/json' -d "R" $CHECK_SENSU_URI/results > /dev/null
NODE_RESULT=`echo $?`

#Review the result of inserting data into sensu
RESULT=0
OUT="OK"
if [ "$SERVICE_RESULT" != "0" ]; then
   RESULT=1
   OUT="Could not insert the service data into sensu"
fi

if [ "$NODE_RESULT" != "0" ]; then
   if [ "$SERVICE_RESULT" != "0" ]; then
      RESULT=2
      OUT="Could not insert any data into sensu"
   else
      OUT="Could not insert the node data into sensu"
   fi
fi

echo "$OUT"
exit $RESULT
