import sys
import os

import hashlib
import zlib

if len(sys.argv) > 1:
    if sys.argv[1] == "init":
        try:
            os.makedirs('.loom/objects')
            os.makedirs('.loom/refs/heads')  
        except FileExistsError as e:
            print("loom already got initialised")
            sys.exit(0)
        new_file_path = '.loom/HEAD'
        content_to_write = 'ref: refs/heads/main\n'
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(content_to_write)
    elif sys.argv[1] == "cat-file":
        path = '.loom/objects/' + sys.argv[2]
        with open(path, 'rb') as f:
            c = f.read()
            c1 = zlib.decompress(c)
            print(c1)
            c2 = c1.split(b'\x00', maxsplit=1)
            print(c2)
            pure = c2[1].decode('utf-8')
            print(pure)
    elif sys.argv[1] == "add":
        if len(sys.argv) < 3:
            print("Usage: python loom.py add <filename>")
            sys.exit(1)
        file_path = sys.argv[2]
        
        #1. Hash and Store (Reusing Hash-object logic)
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            sys.exit(1)

        header = f"blob {len(content)}\0".encode('utf-8')
        store = header + content

        sha1 = hashlib.sha1(store).hexdigest()
        zlibout = zlib.compress(store)

        object_path = '.loom/objects/' + sha1
        with open(object_path, 'wb') as f:
            f.write(zlibout)

        #2. The Ledger (.loom/index)
        index_path = '.loom/index'
        index_data = {}

        #Read the existing index if it already exists
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        #We split by the first space only: "<hash> <filepath>"
                        parts = line.strip().split(' ', 1)
                        if len(parts) == 2:
                            index_data[parts[1]] = parts[0]
        
        #Update the dictionary with the new hash for this file
        index_data[file_path] = sha1

        #3. Write the updated ledger back to the file
        with open(index_path, 'w', encoding='utf-8') as f:
            for path, obj_hash in index_data.items():
                f.write(f"{obj_hash} {path}\n")

        print(f"Staged {file_path}")
        

# with open('sample.py', 'rb') as file:
#     content = file.read() # read the file in binary mode

# header = f"blob {len(content)}\0".encode('utf-8') # create the loom blob header

# store = header + content # concatenate header and file content

# sha1 = hashlib.sha1(store).hexdigest() # compute the SHA-1 hash
# zlibout = zlib.compress(store)

# file_to_create = '.loom/objects/' + sha1
# with open(file_to_create, 'wb') as f:
#     f.write(zlibout)

# print(sha1)
