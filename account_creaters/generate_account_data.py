from faker import Faker
# install with: pip install faker
import string
import random
import json
import sys

def gen_password(length):
    # TODO: do this more secure
    return ''.join(random.choice("@${}()^&*%#!"+string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

if len(sys.argv) != 3:
    print "Usage: %s <num accounts> <output file>"%(sys.argv[0])

num_accounts = int(sys.argv[1])
output_file = sys.argv[2]

config = {"accounts": []}
f = Faker()

for _ in range(num_accounts):
    account = {
        "auth_service": "ptc",
        "username": f.username() + gen_password(5) ,
        "password": gen_password(15)+"!",
        "location": "40.766733, -73.977474",
        "cp": 0
        }
    config["accounts"].append(account)


with open(output_file, "w") as fd:
    fd.write(json.JSONEncoder().encode(config))
