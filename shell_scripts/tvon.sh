#!/bin/bash

ssh -i /home/aephir/connection/privatekey_libreelec root@192.168.0.155 "echo 'on 0' | cec-client -s"
