#!/bin/bash

ssh -i /home/aephir/connection/privatekey_libreelec root@192.168.0.155 "echo 'standby 0' | cec-client -s"
