from flask import Flask, jsonify
app = Flask(__name__)
api = None

@app.route("/inventory")
def get_inventory():
    inventory_items = api.get_inventory().call()['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
    return jsonify(inventory_items)


if __name__ == "__main__":
    app.run()
