#!/bin/bash
echo -e "HELLOKETTLE\nset sys output 0x4\nset sys output $1\n" | nc  192.168.0.20 2000
