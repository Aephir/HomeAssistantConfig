#!/bin/bash

# OBS! For new HASS, remember to try connecting using the homeassistant user through terminal, so you can accept connections

ssh -i /home/aephir/connection/privatekey_libreelec root@192.168.0.155 "shutdown -h now"
