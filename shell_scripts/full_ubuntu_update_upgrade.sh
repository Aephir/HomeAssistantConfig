#!/bin/bash

echo "Updating and upgrading Raspbian"
sudo apt-get update && sudo apt-get upgrade -y

echo "Updating Home Assistant"
bash /home/homeassistant/.homeassistant/shell_scripts/updatehass.sh

echo "Update Custom UI files"
bash /home/homeassistant/.homeassistant/update_custom_ui.sh

echo "Upgrading AppDaemon"
sudo pip3 install --upgrade appdaemon

echo "updating Let's Encrypt certificates"
bash  /home/homeassistant/.homeassistant/shell_scripts/certbot_update.sh 

echo "Updated and upgraded" 
