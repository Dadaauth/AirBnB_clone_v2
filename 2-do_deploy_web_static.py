#!/usr/bin/python3
# A fabric script to compress the contents of a folder
from fabric.api import *
import os


def do_pack():
    """A fabric function to conpress files"""
    local('if [ ! -d "versions" ];'
          'then\n\t\tmkdir "versions"\n\tfi', capture=True)

    dt = local("date '+%Y%m%d%H%M%S'", capture=True)
    comp_filename = f"versions/web_static_{dt}.tgz"
    command = f"tar -cvzf {comp_filename} web_static"
    local(command)
    result = local("echo $?", capture=True)
    if result != 0:
        return None
    else:
        return comp_filename


env.user = "ubuntu"
env.hosts = ["100.25.38.3", "100.24.240.234"]
env.key_filename = ["~/alxswe/ssh_key"]


def do_deploy(archive_path):
    """ Deploy an archive to some web servers """
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False
    archive_name_ext = archive_path[9:]
    archive_name = archive_path[9:-4]
    try:
        put(local_path=archive_path, remote_path='/tmp/', use_sudo=True, mirror_local_mode=True)
    except Exception as e:
        return False
    extract_folder = f"/data/web_static/releases/{archive_name}"
    try:
        run(f"mkdir -p {extract_folder}")
        run(f"tar -xzf /tmp/{archive_name_ext} -C {extract_folder}/")
        run(f"rm /tmp/{archive_name_ext}")
        run(f"mv {extract_folder}/web_static/* {extract_folder}")
        run(f"rm -rf {extract_folder}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {extract_folder} /data/web_static/current")
    except Exception as e:
        return False
    return True
