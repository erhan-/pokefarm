from flask import Flask, jsonify, request
app = Flask(__name__)
api = None

@app.route("/inventory", methods=["GET"])
def get_inventory():
    inventory_items = api.get_inventory().call()['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
    return jsonify(inventory_items)

@app.route("/position", methods=["GET"])
def get_position():
    lat, lng, alt = api.get_position()
    pos = {"lat": lat, "lng": lng, "alt": alt}
    return jsonify(pos)

@app.route("/position", methods=["POST"])
def set_position():
    try:
        lat = request.form.get('lat', type=float)
        lng = request.form.get('lng', type=float)
        alt = request.form.get('alt', type=float)
        api.set_position(lat, lng, alt)
        return jsonify({"status": "ok"})
    except:
        return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run()
