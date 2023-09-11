import os
from flask import Flask, render_template, request, session

app = Flask(__name__, static_url_path='/static')

rooms = {
    "wake_up": {
        "title": "Wake Up",
        "description": "You are asleep, you need to wake up. We need you.",
        "options": {
            "awake": "Wake Up",
        },
    },

    "awake": {
        "title": "test",
        "description": "test",
        "options": {
            "": "",
        }

    },
}

current_room = "wake_up"

items = {
    1: {
        "name": "op mega sword",
        "description": "gives you the strength of an alcoholic father after a night out."
    },
    2: {
        "name": "Key",
        "description": "Opens a door."
    },
}

inventory = []

player_stats = {
  "health": 100,
  "strength": 10,
  "magika": 100,
  "defense": 0,
  "agility": 5,
}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def game():
    room = rooms[current_room]
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))