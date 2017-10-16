#!/usr/bin/python
import os
import glob
import shutil
import getpass
import subprocess
from sys import argv


def help():
    print("")
    print("app_mvr help:")
    print("app_mvr must be run as root/sudo.")
    print("Usage: sudo app_mvr.py --app TextEditor --from /volume1 --to /volume2")
    print("\t--app\t<APP>\tThe apps name found in the @appstore directory.")
    print("\t--all\t\tAlternative to --app. Moves all applications on the source volume.")
    print("\t--from\t<VOL>\tThe volume the app is currently installed on.")
    print("\t--to\t<VOL>\tThe destination volume you want the app installed on.")
    print("")
    exit(0)

def switch(item):
    index = argv.index(item) + 1
    return(argv[index])

def termy(cmd):
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return(task.communicate())

def move_app(app, src_volume, dst_volume):
    src = os.path.join(src_volume, "@appstore", app)
    dst = os.path.join(dst_volume, "@appstore", app)
    
    # create new @appstore dir if it doesn't exist
    dst_store = os.path.join(dst_volume, "@appstore")
    if not os.path.isdir(dst_store):
        os.makedirs(dst_store)
    
    # stop the app
    termy(["/var/packages/{0}/scripts/start-stop-status".format(app), "stop"])
    # move the app
    shutil.move(src, dst)
    # remove the app target
    os.unlink("/var/packages/{0}/target".format(app))
    # create a new symlink
    termy(["/bin/ln", "-s", dst, "/var/packages/{0}/target".format(app)])
    # start the app
    termy(["/var/packages/{0}/scripts/start-stop-status".format(app), "start"])


# verify sudo/root is used
if getpass.getuser() != "root":
    print("Please run as root, exiting...")
    help()


if "--help" in argv or "-h" in argv:
    help()

# get the app name
if "--app" in argv:
    app = switch('--app')
# continue if --all is an argument or fail
elif "--all" in argv:
    pass
else:
    print("Improper syntax, exiting...") # sub with help()
    exit(1)

# get the source volume
if "--from" in argv:
    src_volume = switch('--from')
else:
    print("Improper syntax, exiting...") # sub with help()
    exit(1)

# get the destination volume
if "--to" in argv:
    dst_volume = switch('--to')
else:
    print("Improper syntax, exiting...") # sub with help()
    exit(1)

# move all apps from a volume
if "--all" in argv:
    app_src = os.path.join(src_volume, "@appstore", "*")
    apps = glob.glob(app_src)
    for app in apps:
        move_app(os.path.basename(app), src_volume, dst_volume)
# move a single app from a volume
else:
    move_app(app, src_volume, dst_volume)
