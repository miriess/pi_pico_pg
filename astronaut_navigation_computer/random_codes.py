from random import randrange
import json

codelist = []

for i in range(49):
    code = '*'
    for i in range(4):
        code += str(randrange(0,10,1))
    code += '#'
    codelist.append(code)

code_json = {'codes': codelist}

# with open('codelist.json', 'w') as outputfile:
#     outputfile.write(json.dumps(code_json, indent=2))
