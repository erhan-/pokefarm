#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from lxml import etree


# get csrf token



csrf_token = ""

r = requests.get('https://club.pokemon.com/de/pokemon-trainer-club/anmelden/')
cookies = r.cookies

csrfmiddlewaretoken = ""
day = "05"
month = "11"
year = "1984"
undef1 = "10"
undef2

data = {
    'csrfmiddlewaretoken':csrf_token,
    'username': username,
    'password': password,
    'confirm_password': password,
    'email': email,
    'confirm_email': email,
    'public_profile_opt_in': 'False',
    'screen_name': '',
    'terms': 'on',
    }

register = requests.post('https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden', data)

csrfmiddlewaretoken=ghJ7Y4R221CvX8LzjTDxIBmRbP6aHOkl&dob=17.07.2004&undefined=6&undefined=2004&country=US&country=US

csrfmiddlewaretoken=JkLFxVEGb5do6PFGJczPbyFWOeh6Nnb2&dob=05.11.1984&undefined=10&undefined=1984&country=US&country=US


#root = etree.fromstring(r.text.decode('utf8'))
print(r.text)
#print(root.xpath("//input[@name='csrfmiddlewaretoken']/text()"))
# inputs = root.find("input")
# input_list = inputs.findall("input[@name='csrfmiddlewaretoken']/content")
# for a in input_list_list:
#     print a.text

# username = ""
# password = ""
# email = ""
#
#
# data = {
#     'csrfmiddlewaretoken':csrf_token,
#     'username': username,
#     'password': password,
#     'confirm_password': password,
#     'email': email,
#     'confirm_email': email,
#     'public_profile_opt_in': 'False',
#     'screen_name': '',
#     'terms': 'on',
#     }
#
# register = requests.post('https://club.pokemon.com/de/pokemon-trainer-club/eltern/anmelden', data)
