#!/opt/homebrew/bin/python3
import sys, argparse, pickle, os
sys.dont_write_bytecode = True
from http import client
from box import do_Box_OAuth
from boxsdk import Client
from boxsdk.exception import BoxAPIException

FILE_LIST_PATH = 'filelist.pkl'
FILE_NAME_PATH= 'filenames.pkl'
PROCESSED_FILE_PATH = 'processedfiles.pkl'
RANSOMWARE_KEY= '.deadbolt'
# get folders
# 126264334150, 115714809494, 116874274727,107948712218,107946739327,135025921277, 109911126297, 118344302378
folder_ids =[135025921277, 109911126297, 118344302378]
file_ids = []
file_names= {}
processed_file_ids = []

def file_setup():
    """get all the files in the specified folders"""
    global file_ids, file_names, processed_file_ids
    if (os.path.exists(FILE_LIST_PATH)): 
        with open(FILE_LIST_PATH, 'rb') as f:
            file_ids = pickle.load(f)
    else:
        for folder_id in folder_ids:
            items = client.folder(folder_id=folder_id).get_items()
            for item in items:
                #print(f'{item.type} {item.id} is named "{item.name}"')
                print('.', end='', flush=True)
                if item.type == 'folder':
                    folder_ids.append(item.id)
                else:
                    # work only on the ransomeware infected files
                    if (item.name.endswith(RANSOMWARE_KEY)):
                        file_names[item.id]=item.name
                        file_ids.append(item.id)
        with open(FILE_LIST_PATH,'wb') as f:
            pickle.dump(file_ids, f)
        with open(FILE_NAME_PATH, 'wb') as f:
            pickle.dump(file_names, f)

    if (os.path.exists(FILE_NAME_PATH)):
        with open(FILE_NAME_PATH, 'rb') as f:
            file_names = pickle.load(f)

    if (os.path.exists(PROCESSED_FILE_PATH)):
        with open(PROCESSED_FILE_PATH,'rb') as f:
            processed_file_ids = pickle.load(f)
            for file_id in processed_file_ids:
                file_ids.remove(file_id)
    else:
        processed_file_ids = []

def recover():
    """recover the files with specific heuristics"""
    global file_ids, file_names, processed_file_ids
    try:
        for file_id in file_ids:
            file_name = file_names[file_id]
            #file_info = client.file(file_id).get()
            # work only on the ransomware infected files
            if (file_name.endswith(RANSOMWARE_KEY)):
                #print (f'Working on File: {file_name}')
                file_versions = client.file(file_id).get_previous_versions()
                version = next((x for x in file_versions), None)
                if (version != None):
                    new_file_name = file_name.replace(RANSOMWARE_KEY,'')
                    version_to_promote = client.file_version(version.id)
                    new_version = client.file(file_id).promote_version(version_to_promote)
                    try:
                        updated_file = client.file(file_id).update_info(data={'name': new_file_name})
                    except BoxAPIException as b:
                        if "same name" in b.message:
                            print(f"File {file_id} has duplicate issue")
                            updated_file = client.file(file_id).update_info(data={'name': "__" + new_file_name  })
                    print(f'Version promoted to {updated_file.id} and File renamed to {new_file_name}')
            else:
                print('.', end='')
            processed_file_ids.append(file_id)
    finally:
        with open(PROCESSED_FILE_PATH, 'wb') as f:
            pickle.dump(processed_file_ids, f)

def cleanup():
    if False:
        # we are done remove the intermediate files
        if os.path.exists(FILE_LIST_PATH):
            os.remove(FILE_LIST_PATH)
        if os.path.exists(PROCESSED_FILE_PATH):
            os.remove(PROCESSED_FILE_PATH)
        
def main(argv):
    global oauth, client, folder_ids, RANSOMWARE_KEY
    parser = argparse.ArgumentParser(description='recover files in folders hit with ransomware.')
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
    print(f'{RANSOMWARE_KEY}')
    oauth = do_Box_OAuth()
    client = Client(oauth)
    file_setup()
    recover()
    cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])
