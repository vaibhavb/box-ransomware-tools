#!/opt/homebrew/bin/python3
import sys, argparse, pickle, os
sys.dont_write_bytecode = True
from http import client
from box import do_Box_OAuth
from boxsdk import Client
from boxsdk.exception import BoxAPIException

folder_ids = []
RANSOMWARE_KEY= '.deadbolt'

def get_files():
    """get all the files in the specified folders"""
    global folder_ids
    for folder_id in folder_ids:
        items = client.folder(folder_id=folder_id).get_items()
        for item in items:
            if item.type == 'folder':
                folder_ids.append(item.id)
            else:
                # work only on the ransomware infected files
                if (item.name.endswith(RANSOMWARE_KEY)):
                    file_versions = client.file(item.id).get_previous_versions()
                    version_count = 0
                    for i in file_versions:
                        # incrementing counter
                        version_count = version_count + 1
                    print(f'{item.type} {item.id} is named "{item.name} with versions {version_count}"')

def cleanup():
    # we are done remove the intermediate files
    return

def main(argv):
    global oauth, client, folder_ids, RANSOMWARE_KEY
    parser = argparse.ArgumentParser(description='Get details on files in folders hit with ransomware.')
    parser.add_argument('-t', '--test', action='store_true', help="tests the oauth connection to Box servers")
    parser.add_argument("-d", "--folder_id", action='extend', nargs='+', help="folder ID(s) to work on")
    parser.add_argument("-r", "--ransomware_ext", action='store', help="ransomware file extension, default is deadbolt")
    args = parser.parse_args()
    if (args.test):
        oauth = do_Box_OAuth()
        client = Client(oauth)
        user = client.user().get()
        print(f'User ID is {user.id}')
        sys.exit()
    if (args.folder_id):
        folder_ids = args.folder_id
    if (args.ransomware_ext):
        RANSOMWARE_KEY = "." + args.ransomware_ext
    oauth = do_Box_OAuth()
    client = Client(oauth)
    get_files()
    print(f'{folder_ids}')
    cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])
