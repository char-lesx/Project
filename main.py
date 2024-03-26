import os
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'whoopsiedaisies!'

def load_user_credentials():
    credentials = {}
    with open('user_credentials.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                username, password = parts
                credentials[username] = password
            else:
                print(f"Skipping invalid line: {line}")
    return credentials

valid_credentials = load_user_credentials()

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
            "left_path": "Left Path",
            "middle_path": "Middle Path",
            "right_path": "Right Path"

        },
    },
    "back": {
        "title": "The Outside.",
        "description": "There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "left_path": "Left Path",
            "middle_path": "Middle Path",
            "right_path": "Right Path"

        },
    },
    "leave": {
        "title": "The Outside.",
        "description": "There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "middle_path": "Middle Path",
            "right_path": "Right Path"

        },
    },
    "go_back": {
        "title": "The Outside.",
        "description": "There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "middle_path": "Middle Path",

        },
    },
    "left_path": {
        "title": "A Mysterious Tree.",
        "description": "Before you stands a tall old tree. Something is off about this particular tree.",
        "options": {
            "back": "Back",
            "punch": "Punch"

        },
    },
    "punch": {
        "title": "Battle.",
        "description": "You have punched the tree and it has become enraged. Prepare for battle.",
        "options": {
            "back": "Back",
            "punch_again": "Punch Again"

        },
    },
    "punch_again": {
        "title": "Battle.",
        "description": "You have punched the tree again and are now engaged in intense combat.",
        "options": {
            "back": "Back",
            "right_hook": "Right Hook",
            "uppercut": "Uppercut"

        },
    },
    "uppercut": {
        "title": "Battle.",
        "description": "You have uppercutted the tree you punched a branch and it flung itself back at you and damagaed you.",
        "options": {
            "back": "Back",
            "right_hook": "Right Hook",
            "run_away": "Run Away"

        },
    },
    "run_away": {
        "title": "Escape attempt.",
        "description": "You have realised you are outmatched, you run as fast as you can away but it is futile.",
        "options": {

        },
    },
    "right_hook": {
        "title": "Battle Won.",
        "description": "You have right hooked the tree and landed a good hit. You take a little damage to the fist but defeat the tree.",
        "options": {
            "leave": "Leave"

        },
    },
    "right_path": {
        "title": "Wise Old Man.",
        "description": "You walk down the right path to come upon a wise old man, he tells you that you must make your way towards the city. Though you must beware there are dangerous creatures roaming the land. He gives you a health potion to help you on your journey.",
        "options": {
            "go_back": "Go Back"

        },
    },
    "middle_path": {
        "title": "",
        "description": "",
        "options": {
            "go_back": "Go Back",
            "": ""

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
    3: {
        "name": "Health Potion",
        "description": "Drink to regain 40 HP."
    }

}

inventory = []

player_stats = {
  "health": 100,
  "strength": 10,
  "magika": 100,
  "defense": 0,
  "agility": 5,
}

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in valid_credentials and valid_credentials[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'logged_in' in session:
        # Save user progress
        session.pop('logged_in', None)
        session.pop('username', None)
    return redirect(url_for('login'))

def sort_array(arr):
    n = len(arr)
    for i in range(n-1):

        swapped = False
        for j in range(0, n-i-1):

            if arr[j] > arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not swapped:
            return

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in valid_credentials:
            return 'Username already exists. Please choose another.'

        with open('user_credentials.txt', 'a') as file:
            file.write(f'{username},{password}\n\n')

        valid_credentials[username] = password

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/game')
def game():
    room = rooms[current_room]
    if player_stats['health'] <= 0:
        # Player's health is 0 or negative, render game over template
        return render_template('game_over.html')
    if current_room == "dark_room":
        if 2 not in inventory:
            room["options"]["pick_up_key"] = "Pick Up Key"
        else:
            room["options"].pop("pick_up_key", None)
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

@app.route('/pick_up_key')
def pick_up_key():
    global current_room

    if current_room == "dark_room":
        if 2 not in inventory:
            inventory.append(2)
            rooms[current_room]["options"].pop("pick_up_key", None)

    room = rooms[current_room]
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

@app.route('/move/<direction>', methods=['GET', 'POST'])
def move(direction):
    global current_room

    if current_room == "wake_up" and direction == "dark_room":
        current_room = direction

    current_options = rooms[current_room]["options"]
    if direction in current_options:
        current_room = current_options[direction].lower().replace(" ", "_")

    room = rooms[current_room]
    if current_room == "right_hook":
        player_stats["health"] -= 10 
    if current_room == "uppercut":
        player_stats["health"] -= 50 
    if current_room == "run_away":
        player_stats["health"] -= 100
    if current_room == "dark_room":
        if 2 not in inventory:
            room["options"]["pick_up_key"] = "Pick Up Key"
        else:
            room["options"].pop("pick_up_key", None)

    if current_room == "end_of_corridor":
        if 2 not in inventory:
            room["options"]["unlock"] = "Locked"
        else:
            room["options"]["unlock"] = "Unlock"
    
    if current_room == "right_path":
        inventory.append(3)
    
    if player_stats['health'] <= 0:
        # Player's health is 0 or negative, render game over template
        return render_template('game_over.html')
    
    sort_array(inventory)

    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))