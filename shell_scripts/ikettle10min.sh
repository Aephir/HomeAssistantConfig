#!/bin/bash

echo -e "HELLOKETTLE\nset sys output 0x8010\n" | nc  192.168.0.20 2000
