#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from time import sleep
import logging


landing_page = 'https://club.pokemon.com/de/pokemon-trainer-club/anmelden/'
eltern_anmelden = 'https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden'
#proxy = {"https": "http://127.0.0.1:8080"} # burp
proxy = None
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}
ssl_verify = True

#logging.basicConfig(level=logging.DEBUG)

class PTCAccountCreator:

    def __init__(self, username, password, email, bday):
        self.username = username
        self.password = password
        self.email = email
        self.bday = bday
        self.req_session = requests.session()
        #self.ghost = Ghost()
        #self.session = self.ghost.start()
        # cookies and csrf_token will be set with init_session
        self.init_session()

    def init_session(self):
        for _ in range(5):
            if proxy != None:
                r = self.req_session.get(landing_page, headers=headers, proxies=proxy, verify=ssl_verify)
            else:
                r = self.req_session.get(landing_page, headers=headers, verify=ssl_verify)
            print "init_session resp: ", r.status_code
            if r.status_code == 200:
                self.csrf_token = self.req_session.cookies['csrftoken'] 
                break
            sleep(2)

    def post_birthday(self):
        data = "csrfmiddlewaretoken=%s&dob=%s&undefined=6&undefined=%s&country=DE&country=DE"%(
                self.csrf_token, self.bday, self.bday.split(".")[-1])
        #print self.req_session.cookies
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Referer'] = landing_page
        for _ in range(5):
            try:
                if proxy != None:
                    r = self.req_session.post(landing_page, data, headers=headers, proxies=proxy, verify=ssl_verify)
                else:
                    r = self.req_session.post(landing_page, data, headers=headers, verify=ssl_verify)
                print "post_birthday resp: ", r.status_code
                if r.status_code == 302 or r.status_code == 200:
                    break
                sleep(2)
            except:
                print "error in post_birthday"
                if proxy != None:
                    break
        print r.url

    def post_account(self):
        data = "csrfmiddlewaretoken=%s&username=%s&password=%s&confirm_password=%s&email=%s&confirm_email=%s&public_profile_opt_in=True&screen_name=%s&terms=on"%(
                self.csrf_token, self.username, self.password, self.password, self.email, self.email, self.username)
        for _ in range(5): 
            try:
                if proxy != None:
                    r = self.req_session.post(eltern_anmelden, data, headers=headers, proxies=proxy, verify=ssl_verify)
                else:
                    r = self.req_session.post(eltern_anmelden, data, headers=headers, verify=ssl_verify)
                print "post_account resp: ", r.status_code
                if r.status_code == 320 or r.status_code == 200:
                    break
                sleep(2)
            except:
                print "error in post_account"
                if proxy != None:
                    break
        print r.url


ptc_creator = PTCAccountCreator("m3ta009", "asdfasdfasdf", "m3ta009@gmx.de", "19.07.1977")
ptc_creator.post_birthday()
ptc_creator.post_account()



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
Cookie: django_language=de; s_ppvl=%5B%5BB%5D%5D; s_vnum=1500896475720%26vn%3D1; s_cc=true; _gat_UA-625471-2=1; s_sq=pcomprod%252Ctpciglobalprod%3D%2526pid%253DHomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fclub.pokemon.com%25252Fde%25252Fpokemon-trainer-club%25252Flogin%2526ot%253DA;
s_fid=0FA986871BB1A350-26BF472A739C3DCB;
eVar40=3; s_ppn=Homepage; 
s_invisit=true; 
s_nr=1469360506523-New; 
gpv_pn=Homepage; 
ebpdghrqhiowzrfafjht=637078005; 
s_ppv=Homepage%2C27%2C25%2C873%2C950%2C873%2C1920%2C1039%2C1%2CL;
_ga=GA1.2.775913039.1469360478


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
