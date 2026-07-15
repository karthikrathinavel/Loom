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
    if sys.argv[1] == "cat-file":
        path = '.loom/objects/2dd1620a2f2c2d98732ffe6b899cee5a3f85998c'
        with open(path, 'rb') as f:
            c = f.read()
            c1 = zlib.decompress(c)
            print(c1)
            c2 = c1.split(b'\x00', maxsplit=1)
            print(c2)
            pure = c2[1].decode('utf-8')
            print(pure)

with open('sample.py', 'rb') as file:
    content = file.read() # read the file in binary mode

header = f"blob {len(content)}\0".encode('utf-8') # create the loom blob header

store = header + content # concatenate header and file content

sha1 = hashlib.sha1(store).hexdigest() # compute the SHA-1 hash
zlibout = zlib.compress(store)

file_to_create = '.loom/objects/' + sha1
with open(file_to_create, 'wb') as f:
    f.write(zlibout)

print(sha1)
