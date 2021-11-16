#!/usr/bin/python
import os
import glob
import shutil
import getpass
import subprocess
from sys import argv


src_volume = None
dst_volume = None
app = None
package_start_stop = "/var/packages/{0}/scripts/start-stop-status"

app_link_mapping = {
    "@appstore": "target",
    "@appconf": "etc",
    "@appdata": "var",
    "@apphome": "home",
    "@apptemp": "tmp",
}


def help():
    print("")
    print("app_mvr help:")
    print("app_mvr must be run as root/sudo.")
    print("Usage: sudo app_mvr.py --app TextEditor --from /volume1 --to /volume2")
    print("\t--dry-run\tRun a test without actually moving anything.")
    print("\t--app\t<APP>\tThe apps name found in the @appstore directory.")
    print("\t--all\t\tAlternative to --app. Moves all applications on the source volume.")
    print("\t--from\t<VOL>\tThe volume the app is currently installed on.")
    print("\t--to\t<VOL>\tThe destination volume you want the app installed on.")
    print("")
    exit(0)


def switch(item):
    index = argv.index(item) + 1
    return argv[index]


def termy(cmd):
    task = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return task.communicate()


def move_app(app, source, destination):

    if "--dry-run" in argv:
        print("Moving {}".format(app))
        print("Stopping", [package_start_stop.format(app), "stop"])
    else:
        # stop the app
        termy([package_start_stop.format(app), "stop"])

    for dir_name, target in app_link_mapping.items():
        src = os.path.join(source, dir_name, app)
        dst = os.path.join(destination, dir_name, app)
        target_path = "/var/packages/{app}/{target}".format(app=app, target=target)

        relink_app(app, dir_name, target_path, src, dst)

    if "--dry-run" in argv:
        print("Starting", [package_start_stop.format(app), "start"])
    else:
        # start the app
        termy([package_start_stop.format(app), "start"])

    print("------Done moving {}-----".format(app))


def relink_app(app, dir_name, target_path, src, dst):
    print(app, dir_name)
    if not os.path.exists(src):
        print(src, "does not exists. Skipping.")
        return

    # create new dir_name (@appstore and such) dir if it doesn't exist
    dst_store = os.path.join(dst, dir_name)
    if not os.path.isdir(dst_store):
        print("Creating {}".format(dst_store))
        os.makedirs(dst_store)

    if "--dry-run" in argv:
        print("moving from {} to {}".format(src, dst))
        print("Unlink {}".format(target_path))
        print("Create new symlink", "/bin/ln -s {} {}".format(dst, target_path))
    else:
        # move the app
        shutil.move(src, dst)
        # remove the app target
        os.unlink(target_path)
        # create a new symlink
        termy(["/bin/ln", "-s", dst, target_path])


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
    print("Improper syntax, exiting...")  # sub with help()
    exit(1)

# get the source volume
if "--from" in argv:
    src_volume = switch('--from')
else:
    print("Improper syntax, exiting...")  # sub with help()
    exit(1)

# get the destination volume
if "--to" in argv:
    dst_volume = switch('--to')
else:
    print("Improper syntax, exiting...")  # sub with help()
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
