#!/usr/bin/python3
# A fabric script to compress the contents of a folder
from fabric.api import *
import os


@runs_once
def do_pack():
    """A fabric function to conpress files"""
    local('if [ ! -d "versions" ];'
          'then\n\t\tmkdir "versions"\n\tfi', capture=True)

    dt = local("date '+%Y%m%d%H%M%S'", capture=True)
    comp_filename = f"versions/web_static_{dt}.tgz"
    command = f"tar -cvzf {comp_filename} web_static"
    local(command)
    result = local("echo $?", capture=True)
    if result.stdout != '0':
        return None
    return comp_filename


def do_deploy(archive_path):
    """ Deploy an archive to some web servers """
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False
    archive_name_ext = archive_path[9:]
    archive_name = archive_path[9:-4]
    try:
        put(local_path=archive_path, remote_path='/tmp/',
            use_sudo=True, mirror_local_mode=True)
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


# You can also pass these variables via the
# Command line i.e -u ubuntu -i ssh_key
# env.user = "ubuntu"
env.hosts = ["100.25.38.3", "100.24.240.234"]
# env.key_filename = ["~/alxswe/ssh_key"]


def deploy():
    """Does the archiving and deployment tasks """
    created_archive = do_pack()
    if created_archive is None:
        return False
    return do_deploy(created_archive)


def extract_files_to_remove(directory, number, env):
    """ Extracts the filenames that is needed to be removed
    """
    if env == 'remote':
        filenames = run(f'find {directory} -mindepth'
                        f'1 -maxdepth 1 -type d -exec basename {{}} \\;')
        filenames = filenames.stdout.strip().split('\n')
        for index, filename in enumerate(filenames):
            filenames[index] = filename.strip('\r')
    else:
        filenames = os.listdir(directory)
    filenames.sort(reverse=True)

    if number > len(filenames) - 1:
        print(f'number more than expected range'
              f'[0-{len(filenames) - 1}] got [{number}]')
        print('continuing ....')
        return None
    elif number == 0 or number == 1:
        filenames = filenames[1:]
    else:
        filenames = filenames[number:]
    return filenames


@runs_once
def remove_local(number=0):
    """Remove the non-needed files from the local machine"""
    filenames = extract_files_to_remove('versions', number, 'local')
    if filenames == None:
        return None
    # Loop through the remaining list of filenames
    # and delete them all from the filesystem
    for filename in filenames:
        # Delete them all
        os.remove(f'versions/{filename}')
        print(f"Deleted: versions/{filename} from local")
    return filenames


def do_clean(number=0):
    """Cleans both the local storage and the remote storage"""
    number = int(number)
    remove_local(number)
    directory = '/data/web_static/releases'
    filenames = extract_files_to_remove(directory, number, 'remote')
    if filenames == None:
        return None
    for filename in filenames:
        if filename[:11] == "web_static_":
            run(f"rm -rf {directory}/{filename}")
            print(f"Deleted: {directory}/{filename} from remote")
