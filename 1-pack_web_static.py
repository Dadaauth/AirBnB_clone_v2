#!/usr/bin/python3
# A fabric script to compress the contents of a folder
from fabric.api import *


def do_pack():
    """A fabric function to conpress files"""
    local('if [ ! -d "versions" ]; then\n\t\tmkdir "versions"\n\tfi', capture=True)

    dt = local("date '+%Y%m%d%H%M%S'", capture=True)
    comp_filename = f"versions/web_static_{dt}.tgz"
    command = f"tar -cvzf {comp_filename} web_static"
    local(command)
    result = local("echo $?", capture=True)
    if result != 0:
        return None
    else:
        return comp_filename
