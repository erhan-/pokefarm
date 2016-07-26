#!/usr/bin/env python
"""
pgoapi - Pokemon Go API
Copyright (c) 2016 tjado <https://github.com/tejado>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

Author: tjado <https://github.com/tejado>
"""

import os
import re
import sys
import json
import time
import struct
import pprint
import logging
import requests
import argparse
import getpass



# add directory of this file to PATH, so that the package will be found
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# import Pokemon Go API lib
from pgoapi import pgoapi
from pgoapi import utilities as util

# other stuff
from google.protobuf.internal import encoder
from geopy.geocoders import GoogleV3
from s2sphere import Cell, CellId, LatLng
from time import sleep

log = logging.getLogger(__name__)

def get_pos_by_name(location_name):
    geolocator = GoogleV3()
    # add something to retry if it didn't work
    loc = geolocator.geocode(location_name)

    log.info('Your given location: %s', loc.address.encode('utf-8'))
    log.info('lat/long/alt: %s %s %s', loc.latitude, loc.longitude, loc.altitude)

    return (loc.latitude, loc.longitude, loc.altitude)

def get_cell_ids(lat, long, radius = 10):
    origin = CellId.from_lat_lng(LatLng.from_degrees(lat, long)).parent(15)
    walk = [origin.id()]
    right = origin.next()
    left = origin.prev()

    # Search around provided radius
    for i in range(radius):
        walk.append(right.id())
        walk.append(left.id())
        right = right.next()
        left = left.prev()

    # Return everything
    return sorted(walk)

def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return ''.join(output)

def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"

    # If config file exists, load variables from json
    load   = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))


    # Read passed in Arguments
    required = lambda x: not x in load['accounts'][0].keys()
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')", required=required("auth_service"))
    parser.add_argument("-i", "--config_index", help="config_index", type=int)#required=required("config_index"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password", required=required("password"))
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.add_argument("-c", "--cached", help="cached", action='store_true')
    parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
    parser.add_argument("-cp", "--cp", help="CP Cutoff", required=required("cp"))
    parser.add_argument("--token", help="token will be send to django and django will return the actual config", type=str)
    parser.add_argument("--master", help="master server example: http://10.8.0.1:8000", type=str)
    parser.add_argument("--rest", help="start rest api server", action='store_true')
    parser.set_defaults(DEBUG=False, TEST=False,CACHED=False)
    config = parser.parse_args()

    if config.config_index != None:
        load = load['accounts'][config.config_index]
    elif config.master != None and config.token != None:
        resp = requests.post("%s/get_config/"%(config.master), data={"token": config.token})
        #print resp.content
        try:
            load = json.JSONDecoder().decode(resp.content)
            config.__dict__["port"] = load["port"]
            config.__dict__["username"] = load["username"]
            config.__dict__["password"] = load["password"]
            config.__dict__["latitude"] = load["latitude"]
            config.__dict__["longitude"] = load["longitude"]
            config.__dict__["auth_service"] = load["auth_service"]
            config.__dict__["min_cp"] = load["min_cp"]

        except ValueError:
            log.error("Invalid server response, this does not looke like json")
            sys.exit()
    else:
        log.error("-i or --master, --token must be passed as argument")
        return None

    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = load[key]


    if config.auth_service not in ['ptc', 'google']:
        log.error("Invalid Auth service specified! ('ptc' or 'google')")
        return None
    return config


def main():

    config = init_config()
    if not config:
        return
    #print config
    # log settings
    # log format
    logging.basicConfig(filename="logs/"+str(config.port)+"-"+config.username+".log", level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')
    # log level for http request class
    logging.getLogger("requests").setLevel(logging.WARNING)
    # log level for main pgoapi class
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    # log level for internal pgoapi class
    logging.getLogger("rpc_api").setLevel(logging.INFO)


    if config.debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    #position = get_pos_by_name(config.location)
    position = (config.latitude, config.longitude ,0)
    if config.test:
        return

    # instantiate pgoapi
    api = pgoapi.PGoApi()

    # provide player position on the earth
    api.set_position(*position)

    logged_in = False
    while(logged_in == False):
        logged_in = api.login(config.auth_service, config.username, config.password, config.cp, config.cached)
        if not logged_in:
            log.error("Login failed. Servers down maybe? Retrying in 5 seconds ...")
            sleep(10)


    # chain subrequests (methods) into one RPC call

    # get player profile call
    # ----------------------
    api.get_player()

    # get inventory call
    # ----------------------
    api.get_inventory()

    # get map objects call
    # repeated fields (e.g. cell_id and since_timestamp_ms in get_map_objects) can be provided over a list
    # ----------------------
    #cell_ids = get_cell_ids(position[0], position[1])
    #timestamps = [0,] * len(cell_ids)
    #api.get_map_objects(latitude = util.f2i(position[0]), longitude = util.f2i(position[1]), since_timestamp_ms = timestamps, cell_id = cell_ids)

    # spin a fort
    # ----------------------
    #fortid = '<your fortid>'
    #lng = <your longitude>
    #lat = <your latitude>
    #api.fort_search(fort_id=fortid, fort_latitude=lat, fort_longitude=lng, player_latitude=f2i(position[0]), player_longitude=f2i(position[1]))

    # release/transfer a pokemon and get candy for it
    # ----------------------
    #api.release_pokemon(pokemon_id = <your pokemonid>)

    # get download settings call
    # ----------------------
    #api.download_settings(hash="05daf51635c82611d1aac95c0b051d3ec088a930")

    # execute the RPC call
    response_dict = api.call()
    #print('Response dictionary: \n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))

    if config.rest:
        # start rest server thread
        import rest_server as rest
        import thread
        rest.api = api
        if config.config_index != None:
            thread.start_new_thread(lambda: rest.app.run(port=5000+config.config_index), ())
        else:
            thread.start_new_thread(lambda: rest.app.run(port=config.port), ())
        log.info("REST Server has been started")

    while True:
        api.main_loop(config.auth_service, config.username, config.password, config.min_cp, config.cached)
     #alternative:
     #api.get_player().get_inventory().get_map_objects().download_settings(hash="05daf51635c82611d1aac95c0b051d3ec088a930").call()


if __name__ == '__main__':
    main()
