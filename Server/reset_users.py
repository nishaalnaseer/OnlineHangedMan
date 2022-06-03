import json, os

if os.name == "nt":
    slash = '\\'
else:
    slash = '/'

path = f"{os.getcwd()}{slash}user_files{slash}"  # linux format

with open("hi-scos.json", 'r') as f:
    scos = json.load(f)

for k, v in scos.items():
    file_path = f"{path}{k}.json"
    try:
        os.remove(file_path)
    except FileNotFoundError e:
        print(e)

with open("hi-scos.json", 'w') as f:
    scos = json.dump({}, f)

with open("users.json", 'w') as f:
    json.dump({}, f)