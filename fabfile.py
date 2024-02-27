#!/usr/bin/env python3
# Using Fabric python library

from fabric.api import *

env.user = "ubuntu"
env.key_filename=['~/alxswe/ssh_key']
env.hosts = ['100.24.240.234']

def uptime():
    run("uptime")
    run("sudo apt-get update -y")
