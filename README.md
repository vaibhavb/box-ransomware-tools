These set of tools help you with recovering ransomeware effects files from Box. 
These tools implement suggestions from [Box article](https://support.box.com/hc/en-us/articles/360043694054-Ransomware)


Pre-requisites
1. Install Box python SDK
2. Create a Box OAuth application


Tools
- box-get-enc-files.py
```sh
% python3 box-get-enc-files.py -h
usage: box-get-enc-files.py [-h] [-t] [-d FOLDER_ID [FOLDER_ID ...]] [-r RANSOMEWARE_EXT]

Get details on files in folders hit with ransomeware.

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            tests the oauth connection to Box servers
  -d FOLDER_ID [FOLDER_ID ...], --folder_id FOLDER_ID [FOLDER_ID ...]
                        folder ID(s) to work on
  -r RANSOMEWARE_EXT, --ransomeware_ext RANSOMEWARE_EXT
                        ransomeware file extension, default is deadbolt
```

- box-ransomeware-recovery.py
```sh
% python3 box-ransomeware-recovery.py -h
usage: box-ransomeware-recovery.py [-h] [-t] [-d FOLDER_ID [FOLDER_ID ...]]
                                   [-r RANSOMEWARE_EXT]

recover files in folders hit with ransomeware.

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            tests the oauth connection to Box servers
  -d FOLDER_ID [FOLDER_ID ...], --folder_id FOLDER_ID [FOLDER_ID ...]
                        folder ID(s) to work on
  -r RANSOMEWARE_EXT, --ransomeware_ext RANSOMEWARE_EXT
                        ransomeware file extension, default is deadbolt
```

- box-rename-file.py
```sh
% python3 box-rename-file.py -h         
usage: box-rename-file.py [-h] [-t] -f FILE_ID -r RENAME

Get details on files in folders hit with ransomeware.

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            tests the oauth connection to Box servers
  -f FILE_ID, --file-id FILE_ID
                        file id to rename
  -r RENAME, --rename RENAME
                        file name to rename to
```