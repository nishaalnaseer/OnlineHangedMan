import json


class wot:
    def __init__(self, name):
        self.name = name

c = wot("okay")

print(c.name)
c.name = "no"
print(c.name)
c.name = "i cant od dis"
print(c.name)

c.__dict__.update({"name": 1})

print(c.name)

with open("test.json", 'r') as f:
    stuff = json.load(f)

print(stuff)

with open("test.json", 'w') as f:
    json.dump(c.__dict__, f)