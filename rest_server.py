from flask import Flask, jsonify
app = Flask(__name__)
api = None

@app.route("/inventory")
def get_inventory():
    response = api.get_inventory().call()
    if response and ('GET_INVENTORY' in response['responses']):
        inventory_items = response['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']
        return jsonify(inventory_items)
    return 'Error in GET_INVENTORY reponse'


@app.route("/player")
def get_player():
    response = api.get_player().call()
    if response and response['responses']['GET_PLAYER']['success'] == True:
        player = response['responses']['GET_PLAYER']['player_data']
        return jsonify(player)
    return 'Error in GET_PLAYER reponse'



if __name__ == "__main__":
    app.run()
