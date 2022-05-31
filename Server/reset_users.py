import json, os

path = f"{os.getcwd()}/user_files/"  # linux format

with open("hi-scos.json", 'r') as f:
    scos = json.load(f)

for k, v in scos.items():
    file_path = f"{path}{k}.json"