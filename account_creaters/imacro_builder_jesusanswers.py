from faker import Faker
# install with: pip install faker
import string
import random
import json
import sys

HEADER = "VERSION BUILD=8970419 RECORDER=FX\nTAB CLOSEALLOTHERS\n"

def gen_password(length):
    # TODO: do this more secure
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


def get_account_macro(username, password, question, answer, first_name, last_name, street, city, zipcode, bday):
    macro_template = """
URL GOTO=http://mail.jesusanswers.com/email/scripts/loginuser.pl
TAG POS=1 TYPE=B ATTR=TXT:Sign<SP>Up<SP>Now!
TAG POS=1 TYPE=B ATTR=TXT:SIGN<SP>UP<SP>NOW
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:loginName CONTENT=%s
SET !ENCRYPTION NO
TAG POS=1 TYPE=INPUT:PASSWORD FORM=NAME:myForm ATTR=NAME:password CONTENT=%s
TAG POS=1 TYPE=INPUT:PASSWORD FORM=NAME:myForm ATTR=NAME:passwordConfirm CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:passwordQuestion CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:passwordAnswer CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:firstName CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:lastName CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:streetAddress CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:city CONTENT=%s
TAG POS=1 TYPE=INPUT:TEXT FORM=NAME:myForm ATTR=NAME:postalCode CONTENT=%s
"""%(username, password, password, question, answer, first_name, last_name, street, city, zipcode)
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:birthMonth CONTENT=%"+bday.split(".")[1]+"\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:birthDay CONTENT=%"+bday.split(".")[0]+"\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:birthYear CONTENT=%"+bday.split(".")[2]+"\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:householdIncome CONTENT=%9\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:occupation CONTENT=%15\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:industry CONTENT=%13\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:primaryLang CONTENT=%1\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:gender CONTENT=%m\n"
    macro_template += "TAG POS=1 TYPE=SELECT FORM=NAME:myForm ATTR=NAME:state CONTENT=%AZ\n"
    macro_template += "TAG POS=8 TYPE=INPUT:CHECKBOX FORM=NAME:myForm ATTR=NAME:interests CONTENT=YES\n"
    return macro_template


def create_macro(account_macros):
    ret = [HEADER]
    count = 2
    for account_macro in account_macros:
        ret.append("\nTAB OPEN\nTAB T=%d\n"%(count))
        ret.append(account_macro)
        count += 1

    return "".join(ret)


if len(sys.argv) != 3:
    print "Usage: %s <account file> <output file>"%(sys.argv[0])
    sys.exit(1)

account_file = sys.argv[1]
output_file = sys.argv[2]

f = Faker()
config = None
macros = []
with open(account_file, "r") as fd:
    config = json.JSONDecoder().decode(fd.read())

for account in config["accounts"]:
    first_name, last_name = f.name().split(" ")[:2]
    username = account["username"]
    password = account["password"]
    question = gen_password(10)
    answer = gen_password(10)
    macros.append(get_account_macro(username, password, question, answer, first_name, last_name, "ErrorStreet", "Phoenix", "85002", "20.4.1980"))


with open(output_file, "w") as fd:
    fd.write(create_macro(macros))
