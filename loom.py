import sys
import os

if len(sys.argv) > 1:
    if sys.argv[1] == "init":
        try:
            os.makedirs('.loom/objects')
            os.makedirs('.loom/refs/heads')  
        except FileExistsError as e:
            print("loom already got initialised")
            sys.exit(0)
        new_file_path = '.loom/HEAD.txt'
        content_to_write = 'ref: refs/heads/main\n'
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(content_to_write)
