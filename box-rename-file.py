#!/opt/homebrew/bin/python3
import sys, argparse, pickle, os
sys.dont_write_bytecode = True
from http import client
from box import do_Box_OAuth
from boxsdk import Client
from boxsdk.exception import BoxAPIException

def rename():
    """recover the files with specific heuristics"""
    global file_id, file_new_name
    try:
        updated_file = client.file(file_id).update_info(data={'name': file_new_name})
        print(f'Version promoted to {updated_file.id} and File renamed to {file_new_name}')
    except BoxAPIException as b:
        if "same name" in b.message:
            print(f"File {file_id} has duplicate issue")
            updated_file = client.file(file_id).update_info(data={'name': "__" + file_new_name  })
            print(f'Version promoted to {updated_file.id} and File renamed to {"__" + file_new_name}')
        else:
            print(b.message)

def cleanup():
    return
            
def main(argv):
    global oauth, client, file_id, file_new_name
    parser = argparse.ArgumentParser(description='rename a specific file-id to a desired name, as box does not allow clean UI re-naming.')
    parser.add_argument('-t', '--test', action='store_true', help="tests the oauth connection to Box servers")
    parser.add_argument('-f', "--file-id", required=True, help='file id to rename')
    parser.add_argument('-r', "--rename", required=True, help='file name to rename to')
    args = parser.parse_args()
    if (args.test):
        oauth = do_Box_OAuth()
        client = Client(oauth)
        user = client.user().get()
        print(f'User ID is {user.id}')
        sys.exit()
    file_id = args.file_id
    file_new_name = args.rename
    oauth = do_Box_OAuth()
    #client = Client(oauth)
    #rename()
    cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])