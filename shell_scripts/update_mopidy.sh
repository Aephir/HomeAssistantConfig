#!/bin/bash

echo "Updating Mopidy OS"
ssh -p 145 -i /home/aephir/connection/privatekey_libreelec pi@192.168.0.145 "sudo apt-get update && sudo apt-get upgrade -y && sudo pip install --upgrade Mopidy-Iris"
