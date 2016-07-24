#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import requests

####################
# install ghost.py:
####################
# pacman -S python2-pyside
# pip install ghost.py

from ghost import Ghost

landing_page = 'https://club.pokemon.com/de/pokemon-trainer-club/anmelden/'
proxy = {"https": "http://127.0.0.1:8080"} # burp
ssl_verify = False



class PTCAccountCreator:

    def __init__(self, username, password, email, bday):
        self.username = username
        self.password = password
        self.email = email
        self.bday = bday
        #self.req_session = requests.session()
        self.ghost = Ghost()
        self.session = self.ghost.start()
        # cookies and csrf_token will be set with init_session
        self.init_session()

    def init_session(self):
        r = self.session.open(landing_page, proxies=proxy, verify=ssl_verify)

        self.cookies = r.cookies
        # this token will also be set in a hidden field, think we can ignore that
        self.csrf_token = self.cookies['csrftoken'] 

    def post_birthday(self):
        #data = {
        #        "csrfmiddlewaretoken": self.csrf_token,
        #        "dob": self.bday,
        #        "undefined": 6,
        #        "undefined": self.bday.split(".")[-1],
        #        "country": "DE",
        #        "country": "DE"
        #        }
        data = "csrfmiddlewaretoken=%s&dob=%s&undefined=6&undefined=%s&country=DE&country=DE"%(
                self.csrf_token, self.bday, self.bday.split(".")[-1])
        r = self.req_session.post(landing_page, data, proxies=proxy, verify=ssl_verify)



ptc_creator = PTCAccountCreator("m3ta003", "asdfasdfasdf", "m3ta003@gmx.de", "19.07.1977")
ptc_creator.post_birthday()



#csrfmiddlewaretoken = ""
#day = "05"
#month = "11"
#year = "1984"
#undef1 = "10"
#undef2
#
#data = {
#    'csrfmiddlewaretoken':csrf_token,
#    'username': username,
#    'password': password,
#    'confirm_password': password,
#    'email': email,
#    'confirm_email': email,
#    'public_profile_opt_in': 'False',
#    'screen_name': '',
#    'terms': 'on',
#    }
#
#register = requests.post('https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden', data)
#
#csrfmiddlewaretoken=ghJ7Y4R221CvX8LzjTDxIBmRbP6aHOkl&dob=17.07.2004&undefined=6&undefined=2004&country=US&country=US
#
#csrfmiddlewaretoken=JkLFxVEGb5do6PFGJczPbyFWOeh6Nnb2&dob=05.11.1984&undefined=10&undefined=1984&country=US&country=US
#
#
##root = etree.fromstring(r.text.decode('utf8'))
#print(r.text)
##print(root.xpath("//input[@name='csrfmiddlewaretoken']/text()"))
## inputs = root.find("input")
## input_list = inputs.findall("input[@name='csrfmiddlewaretoken']/content")
## for a in input_list_list:
##     print a.text
#
## username = ""
## password = ""
## email = ""
##
##
## data = {
##     'csrfmiddlewaretoken':csrf_token,
##     'username': username,
##     'password': password,
##     'confirm_password': password,
##     'email': email,
##     'confirm_email': email,
##     'public_profile_opt_in': 'False',
##     'screen_name': '',
##     'terms': 'on',
##     }
##
## register = requests.post('https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden', data)

### Example ###
"""
GET /de/pokemon-trainer-club/anmelden/ HTTP/1.1
Host: club.pokemon.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://sso.pokemon.com/sso/login?locale=de&service=https://club.pokemon.com/de/pokemon-trainer-club/caslogin
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: en-US,en;q=0.8,de;q=0.6,fr;q=0.4
Cookie: django_language=de; s_ppvl=%5B%5BB%5D%5D; s_vnum=1500896475720%26vn%3D1; s_cc=true; _gat_UA-625471-2=1; s_sq=pcomprod%252Ctpciglobalprod%3D%2526pid%253DHomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fclub.pokemon.com%25252Fde%25252Fpokemon-trainer-club%25252Flogin%2526ot%253DA; s_fid=0FA986871BB1A350-26BF472A739C3DCB; eVar40=3; s_ppn=Homepage; s_invisit=true; s_nr=1469360506523-New; gpv_pn=Homepage; ebpdghrqhiowzrfafjht=637078005; s_ppv=Homepage%2C27%2C25%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; _ga=GA1.2.775913039.1469360478


HTTP/1.1 200 OK
Date: Sun, 24 Jul 2016 11:41:55 GMT
Server: PWS/8.1.38
X-Px: nc h0-s1001.p12-fra ( h0-s3016.p9-jfk), nc h0-s3016.p9-jfk ( origin>CONN)
Content-Type: text/html; charset=utf-8
Content-Language: de
Vary: Accept-Encoding
Px-Uncompress-Origin: -1
Access-Control-Allow-Origin: https://www.pokemon.com
Access-Control-Allow-Credentials: true
X-Frame-Options: SAMEORIGIN
Connection: keep-alive
Set-Cookie: csrftoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o; expires=Sun, 23-Jul-2017 11:41:55 GMT; Max-Age=31449600; Path=/
Set-Cookie: ptcs_session_id=7bt67u3gs0ecobd4vzhbfym5pdckczt9; httponly; Path=/; secure
Set-Cookie: ebpdghrqhiowzrfafjht=1015617753; expires=Sun, 24 Jul 2016 11:43:55 GMT; path=/
Content-Length: 56472






POST /de/pokemon-trainer-club/anmelden/ HTTP/1.1
Host: club.pokemon.com
Connection: keep-alive
Content-Length: 116
Cache-Control: max-age=0
Origin: https://club.pokemon.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://club.pokemon.com/de/pokemon-trainer-club/anmelden/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.8,de;q=0.6,fr;q=0.4
Cookie: s_vnum=1500896475720%26vn%3D1; s_cc=true; _gat_UA-625471-2=1; s_sq=pcomprod%252Ctpciglobalprod%3D%2526pid%253DHomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fclub.pokemon.com%25252Fde%25252Fpokemon-trainer-club%25252Flogin%2526ot%253DA; csrftoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o; ptcs_session_id=7bt67u3gs0ecobd4vzhbfym5pdckczt9; ebpdghrqhiowzrfafjht=1015617753; django_language=de; _sdsat_businessUnit=pcom; _sdsat_Internal/External=internal; _sdsat_Language=de; _ga=GA1.2.775913039.1469360478; _ga=GA1.3.775913039.1469360478; _sdsat_SignUpUserType=Child; s_ppvl=Homepage%2C27%2C25%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; s_ppv=https%253A%2F%2Fclub.pokemon.com%2Fde%2Fpokemon-trainer-club%2Fanmelden%2F%2C69%2C69%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; s_fid=0FA986871BB1A350-26BF472A739C3DCB; eVar40=10; s_ppn=no%20value; s_invisit=true; s_nr=1469360572880-New; gpv_pn=no%20value

csrfmiddlewaretoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o&dob=19.07.1977&undefined=6&undefined=1977&country=DE&country=DE


HTTP/1.1 302 Found
Date: Sun, 24 Jul 2016 11:42:51 GMT
Server: PWS/8.1.38
X-Px: nc h0-s1001.p12-fra ( h0-s3016.p9-jfk), nc h0-s3016.p9-jfk ( origin>CONN)
Content-Length: 0
Content-Type: text/html; charset=utf-8
Content-Language: de
Location: https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden
Access-Control-Allow-Origin: https://club.pokemon.com
Access-Control-Allow-Credentials: true
Vary: Accept-Language, Cookie
X-Frame-Options: SAMEORIGIN
Connection: keep-alive
Set-Cookie: dob=1977-07-19; expires=Sun, 24-Jul-2016 13:42:51 GMT; httponly; Max-Age=7200; Path=/; secure
Set-Cookie: ebpdghrqhiowzrfafjht=212191568; expires=Sun, 24 Jul 2016 11:44:51 GMT; path=/









GET /de/pokemon-trainer-club/eltern/anmelden HTTP/1.1
Host: club.pokemon.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://club.pokemon.com/de/pokemon-trainer-club/anmelden/
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: en-US,en;q=0.8,de;q=0.6,fr;q=0.4
Cookie: s_vnum=1500896475720%26vn%3D1; s_cc=true; _gat_UA-625471-2=1; s_sq=pcomprod%252Ctpciglobalprod%3D%2526pid%253DHomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fclub.pokemon.com%25252Fde%25252Fpokemon-trainer-club%25252Flogin%2526ot%253DA; csrftoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o; ptcs_session_id=7bt67u3gs0ecobd4vzhbfym5pdckczt9; django_language=de; _sdsat_businessUnit=pcom; _sdsat_Internal/External=internal; _sdsat_Language=de; _ga=GA1.2.775913039.1469360478; _ga=GA1.3.775913039.1469360478; _sdsat_SignUpUserType=Child; s_ppvl=Homepage%2C27%2C25%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; s_fid=0FA986871BB1A350-26BF472A739C3DCB; eVar40=10; s_ppn=no%20value; s_invisit=true; s_nr=1469360572880-New; gpv_pn=no%20value; s_ppv=https%253A%2F%2Fclub.pokemon.com%2Fde%2Fpokemon-trainer-club%2Fanmelden%2F%2C69%2C69%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; dob=1977-07-19; ebpdghrqhiowzrfafjht=212191568


HTTP/1.1 200 OK
Date: Sun, 24 Jul 2016 11:42:53 GMT
Server: PWS/8.1.38
X-Px: nc h0-s1001.p12-fra ( h0-s3016.p9-jfk), nc h0-s3016.p9-jfk ( origin>CONN)
Content-Type: text/html; charset=utf-8
Content-Language: de
Vary: Accept-Encoding
Px-Uncompress-Origin: -1
Access-Control-Allow-Origin: https://www.pokemon.com
Access-Control-Allow-Credentials: true
X-Frame-Options: SAMEORIGIN
Connection: keep-alive
Set-Cookie: csrftoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o; expires=Sun, 23-Jul-2017 11:42:53 GMT; Max-Age=31449600; Path=/
Set-Cookie: ebpdghrqhiowzrfafjht=1672910893; expires=Sun, 24 Jul 2016 11:44:53 GMT; path=/
Content-Length: 118279








POST /de/pokemon-trainer-club/eltern/anmelden HTTP/1.1
Host: club.pokemon.com
Connection: keep-alive
Content-Length: 231
Cache-Control: max-age=0
Origin: https://club.pokemon.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.8,de;q=0.6,fr;q=0.4
Cookie: s_vnum=1500896475720%26vn%3D1; _gat_UA-625471-2=1; s_sq=pcomprod%252Ctpciglobalprod%3D%2526pid%253DHomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fclub.pokemon.com%25252Fde%25252Fpokemon-trainer-club%25252Flogin%2526ot%253DA; ptcs_session_id=7bt67u3gs0ecobd4vzhbfym5pdckczt9; dob=1977-07-19; csrftoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o; django_language=de; _sdsat_businessUnit=pcom; _sdsat_Internal/External=internal; _sdsat_Language=de; _ga=GA1.2.775913039.1469360478; _ga=GA1.3.775913039.1469360478; s_ppvl=https%253A%2F%2Fclub.pokemon.com%2Fde%2Fpokemon-trainer-club%2Fanmelden%2F%2C69%2C69%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL; s_cc=true; ebpdghrqhiowzrfafjht=853671453; s_ppv=https%253A%2F%2Fclub.pokemon.com%2Fde%2Fpokemon-trainer-club%2Feltern%2Fanmelden%2C39%2C86%2C1986%2C950%2C873%2C1920%2C1039%2C1%2CL; eVar40=22; s_ppn=no%20value; s_invisit=true; s_nr=1469360653507-New; gpv_pn=no%20value; _sdsat_SignUpUserType=Parent; s_fid=0FA986871BB1A350-26BF472A739C3DCB

csrfmiddlewaretoken=7eSOIWh0VG5pMZrVYubaWvUR4MPxKj5o&username=m3ta002&password=asdfasdfasdf&confirm_password=asdfasdfasdf&email=m3ta002%40gmx.de&confirm_email=m3ta002%40gmx.de&public_profile_opt_in=True&screen_name=m3ta002&terms=on


HTTP/1.1 302 Found
Date: Sun, 24 Jul 2016 11:44:12 GMT
Server: PWS/8.1.38
X-Px: nc h0-s1001.p12-fra ( h0-s3016.p9-jfk), nc h0-s3016.p9-jfk ( origin>CONN)
Content-Length: 0
Content-Type: text/html; charset=utf-8
Content-Language: de
Location: https://club.pokemon.com/de/pokemon-trainer-club/eltern/e-mail
Access-Control-Allow-Origin: https://club.pokemon.com
Access-Control-Allow-Credentials: true
Vary: Accept-Language, Cookie
X-Frame-Options: SAMEORIGIN
Connection: keep-alive
Set-Cookie: ebpdghrqhiowzrfafjht=998098021; expires=Sun, 24 Jul 2016 11:46:12 GMT; path=/



"""












