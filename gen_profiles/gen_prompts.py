import json

pts = []

with open('profiles.json', 'r') as f:
    data = json.load(f)['profiles']
    
for user in data:
    pts.append(f'Generate a profile picture for {user["name"]} {user["age"]} {user["sex"]} {user["religion"]}\n')

with open('prompts.txt', 'w+') as f:
    f.writelines(pts)