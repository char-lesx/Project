import os
from flask import Flask, render_template, request, session

app = Flask(__name__, static_url_path='/static')

rooms = {
    "wake_up": {
        "title": "Wake Up",
        "description": "You are asleep, you need to wake up. We need you.",
        "options": {
            "dark_room": "Wake Up",
        },
    },
    "dark_room": {
        "title": "Dark Room",
        "description": "You have woken up. The room is pitch black. You can see nothing apart from a dim light down a corridor. Even though is there no light you see a slight shimmer on the ground... It's a key.",
        "options": {
            "corridor": "Corridor",
        },
    },
    "corridor": {
        "title": "Corridor",
        "description": "You are in the long corridor. You can still see the dim light at the end. As you walk the the corridor you see mysterious paintings lining the walls.",
        "options": {
            "end_of_corridor": "End of Corridor",
            "back": "Dark Room" 
        },
    },
    "end_of_corridor": {
        "title": "End of the Corridor",
        "description": "As you come to the end of the corridor you are stopped by a big door. It is locked.",
        "options": {
            "corridor": "Corridor",
            "unlock": "Unlock"

        },
    },
    "unlock": {
        "title": "The Outside.",
        "description": "As you exit through the great big door, the sun blazing pierces your eyes. It's been a long time since you've seen the sun. There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "corridor": "Corridor",
            "unlock": "Unlock"

        },
    },
}
current_room = "wake_up"

items = {
    1: {
        "name": "op mega sword",
        "description": "gives you the strength of an alcoholic father after a night out..."
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def game():
    room = rooms[current_room]
    if current_room == "dark_room":
        if 2 not in inventory:  # Check if the key item is not in the inventory
            room["options"]["pick_up_key"] = "Pick Up Key"  # Add the "pick_up_key" option
        else:
            room["options"].pop("pick_up_key", None)  # Remove the "pick_up_key" option
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

@app.route('/pick_up_key')
def pick_up_key():
    global current_room

    if current_room == "dark_room":
        if 2 not in inventory:  # Check if the key item is not in the inventory
            inventory.append(2)  # Add the key item to the inventory
            rooms[current_room]["options"].pop("pick_up_key", None)  # Remove the "pick_up_key" option

    room = rooms[current_room]
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

@app.route('/move/<direction>')
def move(direction):
    global current_room

    if current_room == "wake_up" and direction == "dark_room":
        current_room = direction

    current_options = rooms[current_room]["options"]
    if direction in current_options:
        current_room = current_options[direction].lower().replace(" ", "_")

    room = rooms[current_room]
    if current_room == "dark_room":
        if 2 not in inventory:  # Check if the key item is not in the inventory
            room["options"]["pick_up_key"] = "Pick Up Key"  # Add the "pick_up_key" option
        else:
            room["options"].pop("pick_up_key", None)  # Remove the "pick_up_key" option

    if current_room == "end_of_corridor":
        if 2 not in inventory:  # Check if the key item is not in the inventory
            room["options"]["unlock"] = "Locked"  # Change the label of the "Unlock" option
        else:
            room["options"]["unlock"] = "Unlock"  # Set the label of the "Unlock" option to the original text

    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))