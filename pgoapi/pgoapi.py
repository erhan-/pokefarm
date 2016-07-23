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

from __future__ import absolute_import

import logging
import re
import requests
import json

import pickle
import random


from .utilities import f2i, h2f
from pgoapi.rpc_api import RpcApi
from pgoapi.auth_ptc import AuthPtc
from pgoapi.auth_google import AuthGoogle
from pgoapi.exceptions import AuthException, NotLoggedInException, ServerBusyOrOfflineException


from location import *
from time import sleep
from collections import defaultdict
import os.path


from . import protos
from POGOProtos.Networking.Requests.RequestType_pb2 import RequestType

logger = logging.getLogger(__name__)


# Global variables

CP_CUTOFF = 0 # release anything under this if we don't have it already
#BAD_ITEM_IDS = [101,102,701,702,703] #Potion, Super Potion, RazzBerry, BlukBerry Add 201 to get rid of revive
BAD_ITEM_IDS = [101,102,103,104,201,202,701,702,703,704,705] #Potion, Super Potion, RazzBerry, BlukBerry Add 201 to get rid of revive

inventory_balls = [0, 0, 0]
NO_BALLS = True


class PGoApi:

    API_ENTRY = 'https://pgorelease.nianticlabs.com/plfe/rpc'

    def __init__(self):

        self.log = logging.getLogger(__name__)

        self._auth_provider = None
        self._api_endpoint = None

        self._position_lat = 0
        self._position_lng = 0
        self._position_alt = 0
        self._posf = (0,0,0) # this is floats

        self._req_method_list = []

    def call(self):
        if not self._req_method_list:
            return False

        if self._auth_provider is None or not self._auth_provider.is_login():
            self.log.info('Not logged in')
            return False

        player_position = self.get_position()

        request = RpcApi(self._auth_provider)

        if self._api_endpoint:
            api_endpoint = self._api_endpoint
        else:
            api_endpoint = self.API_ENTRY

        self.log.info('Execution of RPC')
        response = None
        try:
            response = request.request(api_endpoint, self._req_method_list, player_position)
        except ServerBusyOrOfflineException as e:
            self.log.info('Server seems to be busy or offline - try again!')

        # cleanup after call execution
        self.log.info('Cleanup of request!')
        self._req_method_list = []

        return response

    def list_curr_methods(self):
        for i in self._req_method_list:
            print("{} ({})".format(RequestType.Name(i),i))

    def set_logger(self, logger):
        self._ = logger or logging.getLogger(__name__)

    def get_position(self):
        return (self._position_lat, self._position_lng, self._position_alt)

    def set_position(self, lat, lng, alt):
        self.log.debug('Set Position - Lat: %s Long: %s Alt: %s', lat, lng, alt)
        self._posf = (lat,lng,alt)
        self._position_lat = lat
        self._position_lng = lng
        self._position_alt = alt

    def __getattr__(self, func):
        def function(**kwargs):

            if not self._req_method_list:
                self.log.info('Create new request...')

            name = func.upper()
            if kwargs:
                self._req_method_list.append( { RequestType.Value(name): kwargs } )
                self.log.info("Adding '%s' to RPC request including arguments", name)
                self.log.debug("Arguments of '%s': \n\r%s", name, kwargs)
            else:
                self._req_method_list.append( RequestType.Value(name) )
                self.log.info("Adding '%s' to RPC request", name)

            return self

        if func.upper() in RequestType.keys():
            return function
        else:
            raise AttributeError


    def heartbeat(self):
        global inventory_balls
        global NO_BALLS
        # making a standard call, like it is also done by the client
        self.get_player()
        self.get_hatched_eggs()
        self.get_inventory()
        self.check_awarded_badges()
        # self.download_settings(hash="4a2e9bc330dae60e7b74fc85b98868ab4700802e")
        res = self.call()
        #print('Response dictionary: \n\r{}'.format(json.dumps(res, indent=2)))
        if res and ('GET_INVENTORY' in res['responses']):
            NO_BALLS = True
            self.cleanup_inventory(res['responses']['GET_INVENTORY']['inventory_delta']['inventory_items'])
            #print('Response dictionary: \n\r{}'.format(json.dumps(res['responses']['GET_INVENTORY']['inventory_delta']['inventory_items'], indent=2)))
            for item in res['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']:
                if 'player_stats' in item['inventory_item_data']:
                    stats = item['inventory_item_data']['player_stats']
                    self.log.info("Level: %d, Experience: %d, KM walked: %f, Pokedex: %d", stats.get('level', 0), stats.get('experience', 0), stats.get('km_walked', 0), stats.get('unique_pokedex_entries',0))
                if 'item' in item['inventory_item_data']:
                    if ('count' in item['inventory_item_data']['item']) and ('item_id' in item['inventory_item_data']['item']):
                        id = item['inventory_item_data']['item']['item_id']
                        # 1 Pokeball, 2 Superball, 3 Ultraball
                        if id < 4 and id > 0 :
                            inventory_balls[id-1] = item['inventory_item_data']['item'].get('count', 0)
                            if item['inventory_item_data']['item'].get('count', 0) > 0:
                                NO_BALLS = False
            if NO_BALLS:
                self.log.error("No Balls left! Searching forts ...")
        return res






    def walk_to(self,loc): #location in floats of course...
        steps = get_route(self._posf, loc)
        for step in steps:
            for i,next_point in enumerate(get_increments(self._posf,step)):
                self.set_position(*next_point)
                self.heartbeat()
                self.log.info("sleeping before next heartbeat")
                sleep(1)
                while self.catch_near_pokemon():
                    sleep(1)

    def spin_near_fort(self):
        global NO_BALLS
        try:
            map_cells = self.nearby_map_objects()['responses']['GET_MAP_OBJECTS']['map_cells']
            forts = sum([cell.get('forts',[]) for cell in map_cells],[]) #supper ghetto lol
        except:
            return False
        destinations = filtered_forts(self._posf,forts)
        if destinations:
            fort = destinations[0]
            self.log.info("Walking to fort: %s", fort)
            self.walk_to((fort['latitude'], fort['longitude']))
            position = self._posf # FIXME ?
            res = self.fort_search(fort_id = fort['id'], fort_latitude=fort['latitude'],fort_longitude=fort['longitude'],player_latitude=position[0],player_longitude=position[1]).call()['responses']['FORT_SEARCH']
            self.log.info("Fort spinned: %s", res)
            if 'lure_info' in fort and not NO_BALLS:
                self.disk_encounter_pokemon(fort['lure_info'])
            return True
        else:
            self.log.info("No fort to walk to in near distance!")
            return False


    def disk_encounter_pokemon(self, lureinfo):
        if 'encounter_id' in lureinfo:
            encounter_id = lureinfo['encounter_id']
            fort_id = lureinfo['fort_id']
            position = self._posf
            resp = self.disk_encounter(encounter_id=encounter_id, fort_id=fort_id, player_latitude=position[0], player_longitude=position[1]).call()['responses']['DISK_ENCOUNTER']
        else:
            self.log.error("encounter_id not in lure_info: %s", lureinfo)
            return False
        if resp['result'] == 1:
            self.log.info("Started Disk Encounter, Pokemon ID: %s", resp['pokemon_data']['pokemon_id'])
            capture_status = -1
            cp = resp['pokemon_data'].get('cp', CP_CUTOFF)
            id = resp['pokemon_data'].get('pokemon_id', 0)
            iva = resp['pokemon_data'].get('individual_attack', 0)
            ivd = resp['pokemon_data'].get('individual_defense', 0)
            ivs = resp['pokemon_data'].get('individual_stamina', 0)
            cap_prob = resp.get('capture_probability').get('capture_probability')
            iv = ((iva+ivd+ivs)/45.0)*100
            self.log.info("Started Encounter with %d (CP: %d) IV: %f (IVA: %d // IVD: %d // IVS: %d) || capture probability: %s", id, cp, iv, iva, ivd, ivs, cap_prob)
            # while capture_status != RpcEnum.CATCH_ERROR and capture_status != RpcEnum.CATCH_FLEE:
            while capture_status != 0 and capture_status != 3:
                catch_attempt = self.attempt_catch(encounter_id, fort_id, cp,iv, cap_prob)
                capture_status = catch_attempt['status']
                # if status == RpcEnum.CATCH_SUCCESS:
                if capture_status == 1:
                    self.log.info("Caught Pokemon: : %s", catch_attempt)
                    sleep(2)

                    return catch_attempt
                elif capture_status != 2:
                    self.log.info("Failed Catch: : %s", catch_attempt)
                    return False
                sleep(2)
        else:
            self.log.error("Received Disk Encounter result: %s", resp['result'])
            return False

    def catch_near_pokemon(self):
        try:
            map_cells = self.nearby_map_objects()['responses']['GET_MAP_OBJECTS']['map_cells']
            pokemons = sum([cell.get('catchable_pokemons',[]) for cell in map_cells],[]) #supper ghetto lol
        except:
            return False

        # catch first pokemon:
        origin = (self._posf[0],self._posf[1])
        pokemon_distances = [(pokemon, distance_in_meters(origin,(pokemon['latitude'], pokemon['longitude']))) for pokemon in pokemons]
        #self.log.info("Nearby pokemon: : %s", pokemon_distances)
        if pokemons:
            target = pokemon_distances[0]
            self.log.info("Catching pokemon: : %s, distance: %f meters", target[0], target[1])
            return self.encounter_pokemon(target[0])
        return False

    def nearby_map_objects(self):
        position = self.get_position()
        neighbors = getNeighbors(self._posf)
        return self.get_map_objects(latitude=position[0], longitude=position[1], since_timestamp_ms=[0]*len(neighbors), cell_id=neighbors).call()

    def attempt_catch(self, encounter_id, spawn_point_id, cp, iv, cap_prob):
        # Catch depending on ball amount, cp, iv and cap_prob
        global CP_CUTOFF
        pokeball = 1


        # Throw normal ball if we don't care but also check if we even have one, get the worst ball
        for ball_nr, ball_amount in enumerate(inventory_balls, start=1):
            if ball_amount > 0:
                pokeball = ball_nr
                break

        # If it is a good pokemon then we reaaally want it!
        if ((cp > CP_CUTOFF) or (iv > 80)) and inventory_balls[2] > 0:
            pokeball = 3
        else:
            for ball_nr, ball_amount in enumerate(inventory_balls, start=1):
                # Check if we have enough balls and if the probability is acceptable
                if ball_amount > 0 and cap_prob[ball_nr-1] > 0.5:
                    pokeball = ball_nr
                    break

        inventory_balls[pokeball-1] = inventory_balls[pokeball-1]-1
        # CATCH_SUCCESS = 1; CATCH_ESCAPE = 2;
        status = 2
        self.log.info("Will use Ball %d for CP: %d, IV: %f and Probability: %f", pokeball, cp, iv, cap_prob[pokeball-1])

        # Try again if the Pokemon escapes from the Pokeball
        while(status == 2):
            resp = self.catch_pokemon(
                normalized_reticle_size= 1.950,
                pokeball = pokeball,
                spin_modifier= 0.850,
                hit_pokemon=True,
                normalized_hit_position=1,
                encounter_id=encounter_id,
                spawn_point_guid=spawn_point_id,
                ).call()['responses']['CATCH_POKEMON']
            if "status" in resp:
                # Check if the catch was successful
                if resp['status'] == 1:
                    return resp
                else:
                    # Else set the status so that it goes on when 2 or quits if something else
                    status = resp['status']
            else:
                self.log.error("No status in Catch response. Poke inventory full? Increasing CP_CUTOFF: %s:", resp)
                CP_CUTOFF = CP_CUTOFF + 100
                return resp
            self.log.info("Pokemon escaped from ball. Retrying throw ...")
            sleep(1)
        return resp



    def cleanup_inventory(self, inventory_items=None):
        # This function removes duplicate pokemons and items that we don't need.

        if not inventory_items:
            inventory_items = self.get_inventory().call()['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

        caught_pokemon = defaultdict(list)
        for inventory_item in inventory_items:
            if "pokemon_data" in inventory_item['inventory_item_data']:
                # is a pokemon:
                pokemon = inventory_item['inventory_item_data']['pokemon_data']
                if 'cp' in pokemon:
                    caught_pokemon[pokemon["pokemon_id"]].append(pokemon)
            # Remove Items
            elif "item" in  inventory_item['inventory_item_data']:
                item = inventory_item['inventory_item_data']['item']
                if item['item_id'] in BAD_ITEM_IDS and "count" in item:
                    self.recycle_inventory_item(item_id=item['item_id'],count=item['count'])

        # Remove duplicate Pokemons
        for pokemons in caught_pokemon.values():
            # Check if we have more than one of this Pokemon
            if len(pokemons) > 1:
                pokemons = sorted(pokemons, lambda x,y: cmp(x['cp'],y['cp']),reverse=True)

                # Keep the Pokemon with the highest CP or CP >= CP_CUTOFF
                for pokemon in pokemons[1:]:
                    # calculate IV value
                    iva = pokemon.get('individual_attack', 0)
                    ivd = pokemon.get('individual_defense', 0)
                    ivs = pokemon.get('individual_stamina', 0)
                    iv = ((iva+ivd+ivs)/45.0)*100
                    if 'cp' in pokemon and pokemon['cp'] < CP_CUTOFF and iv < 80:
                        self.log.info("Releasing Pokemon %d with CP: %d and IV: %f", pokemon["pokemon_id"], pokemon["cp"], iv)
                        self.release_pokemon(pokemon_id = pokemon["id"])

        return self.call()


    def encounter_pokemon(self, pokemon): #take in a MapPokemon from MapCell.catchable_pokemons
        encounter_id = pokemon['encounter_id']
        spawn_point_id = pokemon['spawn_point_id']
        # begin encounter_id
        position = self._posf # FIXME ?
        resp = self.encounter(encounter_id=encounter_id,spawn_point_id=spawn_point_id,player_latitude=position[0],player_longitude=position[1]).call()['responses']['ENCOUNTER']

        if resp['status'] == 1:
            capture_status = -1
            cp = resp['wild_pokemon']['pokemon_data'].get('cp', CP_CUTOFF)
            id = resp['wild_pokemon']['pokemon_data'].get('pokemon_id', 0)
            iva = resp['wild_pokemon']['pokemon_data'].get('individual_attack', 0)
            ivd = resp['wild_pokemon']['pokemon_data'].get('individual_defense', 0)
            ivs = resp['wild_pokemon']['pokemon_data'].get('individual_stamina', 0)
            cap_prob = resp.get('capture_probability').get('capture_probability')
            iv = ((iva+ivd+ivs)/45.0)*100
            self.log.info("Started Encounter with %d (CP: %d) IV: %f (IVA: %d // IVD: %d // IVS: %d) || capture probability: %s", id, cp, iv, iva, ivd, ivs, cap_prob)
            #{'capture_probability': [0.41520917415618896, 0.5528010129928589, 0.6580196619033813], 'pokeball_type': [1, 2, 3]}}


            # while capture_status != RpcEnum.CATCH_ERROR and capture_status != RpcEnum.CATCH_FLEE:
            # check the cp of the pokemon and throw different ball or also berry
            while capture_status != 0 and capture_status != 3:
                catch_attempt = self.attempt_catch(encounter_id, spawn_point_id, cp, iv, cap_prob)
                status = catch_attempt['status']
                # if status == RpcEnum.CATCH_SUCCESS:
                if status == 1:
                    self.log.info("Caught Pokemon: : %s", catch_attempt)
                    sleep(2)
                    return catch_attempt
                elif status != 2:
                    self.log.info("Failed Catch: : %s", catch_attempt)
                    return False
                sleep(2)
        elif resp['status'] == 7:
            self.log.error("Your Poke Inventory is too full! Encounter response status: %s", resp['status'])
        else:
            self.log.error("Error received in Encounter response status: %s", resp['status'])
            return False


    def login(self, provider, username, password, cp, cached=False):
        global CP_CUTOFF
        CP_CUTOFF = cp
        if not isinstance(username, basestring) or not isinstance(password, basestring):
            raise AuthException("Username/password not correctly specified")

        if provider == 'ptc':
            self._auth_provider = AuthPtc()
        elif provider == 'google':
            self._auth_provider = AuthGoogle()
        else:
            raise AuthException("Invalid authentication provider - only ptc/google available.")

        self.log.debug('Auth provider: %s', provider)

        if not self._auth_provider.login(username, password):
            self.log.info('Login process failed')
            return False

        self.log.info('Starting RPC login sequence (app simulation)')

        fname = "auth_cache_%s" % username
        if os.path.isfile(fname) and cached:
            response = pickle.load(open(fname))
        else:
            response = self.heartbeat()
            f = open(fname,"w")
            pickle.dump(response, f)

        if not response:
            self.log.error('Login failed!')
            return False

        if 'api_url' in response:
            self._api_endpoint = ('https://{}/rpc'.format(response['api_url']))
            self.log.debug('Setting API endpoint to: %s', self._api_endpoint)
        else:
            self.log.error('Login failed - unexpected server response!')
            return False

        if 'auth_ticket' in response:
            self._auth_provider.set_ticket(response['auth_ticket'].values())

        self.log.info('Finished RPC login sequence (app simulation)')
        self.log.info('Login process completed')

        return True




    def main_loop(self):
        global NO_BALLS
        self.heartbeat() # always heartbeat to start...
        while True:
            try:
                self.heartbeat()
                sleep(1)
                self.spin_near_fort()
                if not NO_BALLS:
                    while self.catch_near_pokemon():
                        sleep(4)
            except Exception as e:
                self.log.error("Error in main loop: %s", e)
                sleep(60)
                pass
