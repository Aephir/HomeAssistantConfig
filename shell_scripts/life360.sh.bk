#!/bin/bash

#Set variables
username360="waldenb@gmail.com"
password360="weby270683"
mosquitto_pub="/usr/bin/mosquitto_pub"
mqtt_host="127.0.0.1"
mqtt_port="1883"
mqtt_user="homeassistant"
mqtt_pass="homeassistantMQTTmos"
timeout=180


function bearer {
echo "$(date +%s) INFO: requesting access token"
bearer_id=$(curl -s -X POST -H "Authorization: Basic cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg==" -F "grant_type=password" -F "username=$username360" -F "password=$password360" https://api.life360.com/v3/oauth2/token.json | grep -Po '(?<="access_token":")\w*')
}

function circles () {
echo "$(date +%s) INFO: requesting circles."
read -a circles_id <<<$(curl -s -X GET -H "Authorization: Bearer $1" https://api.life360.com/v3/circles.json | grep -Po '(?<="id":")[\w-]*')
}

function members () {
echo "$(date +%s) INFO: requesting members"
members=$(curl -s -X GET -H "Authorization: Bearer $1" https://api.life360.com/v3/circles/$2)
}

bearer
circles $bearer_id

#Main Loop
while :
do

#Check if circle id is valid. If not request new token.
if [ -z "$circles_id" ]; then
bearer
circles $bearer_id
fi

#Loop through circle ids
for i in "${circles_id[@]}"
do

#request member list
members $bearer_id $i

#Check if member array is valid. If not request new token
if [ -z "$members" ]; then
bearer
circles $bearer_id
members $bearer_id $i
fi

members_count=$(echo $members | jq '.members | (length)')
count=0
while [ $count -lt $members_count ]
do
    id=$(echo $members | jq .members[$count].id)
    firstName=$(echo $members | jq .members[$count].firstName)
    lastName=$(echo $members | jq .members[$count].lastName)
    latitude=$(echo $members | jq .members[$count].location.latitude)
    longitude=$(echo $members | jq .members[$count].location.longitude)
    accuracy=$(echo $members | jq .members[$count].location.accuracy)
    battery=$(echo $members | jq .members[$count].location.battery)
    avatar=$(echo $members | jq .members[$count].avatar)
    echo $firstName
    #echo "$(date +%s) INFO: owntracks/${firstName//\"/}/${id//\"/}" -m "{\"t\":\"p\",\"tst\":$(date +%s),\"acc\":${accuracy//\"/},\"_type\":\"location\",\"alt\":0,\"lon\":${longitude//\"/},\"lat\":${latitude//\"/},\"batt\": ${battery//\"/}}"
    $mosquitto_pub -h $mqtt_host -p $mqtt_port -u $mqtt_user -P $mqtt_pass -t "owntracks/${firstName//\"/}/${id//\"/}" -m "{\"t\":\"p\",\"tst\":$(date +%s),\"acc\":${accuracy//\"/},\"_type\":\"location\",\"alt\":0,\"lon\":${longitude//\"/},\"lat\":${latitude//\"/},\"batt\": ${battery//\"/}}"
    count=$(($count+1))
done
done
sleep $timeout
done
