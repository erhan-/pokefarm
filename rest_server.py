from flask import Flask, jsonify, request
app = Flask(__name__)
api = None








from functools import wraps
from flask import request, Response



def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    # Get username from config file or so

    if username == 'admin' and password == 'secret':
        return True
    else:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/inventory", methods=["GET"])
@requires_auth
def get_inventory():
    inventory_items = api.get_inventory().call()['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
    return jsonify(inventory_items)


@app.route("/evolve", methods=["POST"])
def evolve():
    try:
        poke_id = request.form.get('pokeid', type=int)
        response = api.evolve_pokemon(pokemon_id=poke_id).call()
        return jsonify({"status": response.get('responses').get('EVOLVE_POKEMON')})
    except Exception as e:
        print(e)
        return jsonify({"status": "error"})


@app.route("/release", methods=["POST"])
def release():
    try:
        poke_id = request.form.get('pokeid', type=int)
        response = api.release_pokemon(pokemon_id=poke_id).call()
        return jsonify({"status": response.get('responses').get('RELEASE_POKEMON')})
    except Exception as e:
        print(e)
        return jsonify({"status": "error"})



@app.route("/position", methods=["GET"])
def get_position():
    lat, lng, alt = api.get_position()
    pos = {"lat": lat, "lng": lng, "alt": alt}
    return jsonify(pos)

@app.route("/position", methods=["POST"])
def set_position():
    # data=lat=0.0&lng=0.0&alt=0.0
    try:
        lat = request.form.get('lat', type=float)
        lng = request.form.get('lng', type=float)
        alt = request.form.get('alt', type=float)
        api.set_position(lat, lng, alt)
        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "error"})

@app.route("/pokemon_count", methods=["GET"])
def get_pokemon_count():
    inventory_items = api.get_inventory().call()['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
    count = 0
    for item in inventory_items:
        if item.has_key("inventory_item_data") and item["inventory_item_data"].has_key("pokemon_data"):
            count += 1
    return jsonify({"count": count})

@app.route("/ball_count", methods=["GET"])
def get_ball_count():
    pass


@app.route("/login_account", methods=["POST"])
def login_account():
    # data=auth_service=ptc&username=lalal&password=sicher&cp=100&cached=True
    try:
        auth_service = request.form.get("auth_service", type=str)
        username = request.form.get("username", type=str)
        password = request.form.get("password", type=str)
        cp = request.form.get("cp", type=int)
        cached = request.form.get("cached", type=bool)
        print auth_service, username, password, cp, cached, type(cached)
        if api.login(auth_service, username, password, cp, cached):
            state = "ok"
        else:
            state = "fail"

    except:
        state = "error"
    return jsonify({"status": state})


#@app.route("/cleanup_inventory", methods=["GET"])
#def cleanup_inventory():
#    try:
#        api.cleanup_inventory()
#        return jsonify({"status": "ok"})
#    except:
#        return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run()
