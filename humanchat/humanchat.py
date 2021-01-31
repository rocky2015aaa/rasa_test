from flask import Flask
from flask import jsonify
from flask import request
import time

app = Flask(__name__)

sender_store = {"123": {"paused": True, "replies": []},
                "456": {"paused": True, "replies": []}}

@app.route('/handoff/<sender_id>', methods=["GET","POST"])
def handoff(sender_id):
    if request.method == "POST":
        print(request.get_json()["message"])
        if sender_id in sender_store:
            sender_store[sender_id]["replies"].append(request.get_json()["message"])
            return jsonify(sender_store[sender_id])
        else:
            return jsonify({"error": "sender_id not found"})
    else:
        if sender_id not in sender_store:
            sender_store[sender_id] = {"paused": True, "replies": []}
        
        while len(sender_store[sender_id]["replies"]) == 0:
            time.sleep(1)

        message = sender_store[sender_id]["replies"].pop(0)
        return jsonify({"message": message})


if __name__ == '__main__':
    app.run()
