# Import libraries 
import os
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__, static_url_path='/static')  # Create a Flask application instance
app.secret_key = 'whoopsiedaisies!'  # Set a secret key for session management

# Define functions to load user credentials and sort arrays
# These functions are used to authenticate users and perform sorting operations
def load_user_credentials():
    # Load user credentials from a file and return them as a dictionary
    # Each line in the file contains a username and password separated by a comma
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

# Load initial user credentials
valid_credentials = load_user_credentials()

def sort_array(arr):
    # Sort an array using the bubble sort algorithm
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return

def binary_search(arr, low, high, x):
    # Search for an item within a sorted array
    if high >= low:
 
        mid = (high + low) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        return -1

# Define global variables for storing game data
# These variables store information about game rooms, items, inventory, and player stats

# Dictionary containing information about different rooms in the game
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
            "unlock": "Unlock",
            "corridor": "Corridor"

        },
    },
    "unlock": {
        "title": "The Outside.",
        "description": "As you exit through the great big door, the sun blazing pierces your eyes. It's been a long time since you've seen the sun. There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "left_path": "Left Path",
            "middle_path": "Middle Path"

        },
    },
    "back": {
        "title": "The Outside.",
        "description": "There is only one thing on the horizon and it is a sight to behold. A great big city awaits you...",
        "options": {
            "left_path": "Left Path",
            "middle_path": "Middle Path",

        },
    },
    "leave": {
        "title": "The Outside.",
        "description": "There is only one thing on the horizon and it is a sight to behold. A great big city awaits you... But you notice another pathway has opened since you were last here...",
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
            "punch_again": "Punch Again"

        },
    },
    "punch_again": {
        "title": "Battle.",
        "description": "You have punched the tree again and are now engaged in intense combat.",
        "options": {
            "right_hook": "Right Hook",
            "uppercut": "Uppercut"

        },
    },
    "uppercut": {
        "title": "Battle.",
        "description": "You have uppercutted the tree you punched a branch and it flung itself back at you and damagaed you.",
        "options": {
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
        "title": "Journey towards the city.",
        "description": "You walk towards the city in the distance though it seems to never get closer...",
        "options": {
            "venture_furthur": "Venture Furthur",
            "go_back": "Go Back",

        },
    },
    "go_backwards": {
        "title": "Journey towards the city.",
        "description": "You walk towards the city in the distance though it seems to never get closer...",
        "options": {
            "venture_furthur": "Venture Furthur",
            "go_backwards": "Go Backwards",

        },
    },
    "venture_furthur": {
        "title": "Encounter.",
        "description": "During your journey you are surprised by a humunoid creature iron clad in armor, though the armor seems incredibly rusted and deteriorated...",
        "options": {
            "talk_to_them": "Talk to them",
            "fight_them": "Fight them",
            "go_backwards": "Go Backwards"

        },
    },
    "talk_to_them": {
        "title": "Skeleton.",
        "description": "You have attempted to communicate to whoever this is but as you open your mouth you notice it's a skelton and unable to talk and he lunges at you scraping you with it's rusty sword...",
        "options": {
            "counter_attack": "Counter Attack",
            "grab_sword": "Grab Sword",
            "attempt_to_flee": "Attempt to flee"

        },
    },
    "grab_sword": {
        "title": "Unsuccessful.",
        "description": "You have attempted to take the sword off the skeleton but its grip is too strong, you only end up cutting yourself...",
        "options": {
            "counter_attack": "Counter Attack",
            "attempt_to_flee": "Attempt to flee"

        },
    },
    "counter_attack": {
        "title": "Battle.",
        "description": "As the skeleton lunges at you swing back at the skeleton damaging it.",
        "options": {
            "brute_force_attack": "Brute force attack",
            "attempt_to_flee": "Attempt to flee",

        },
    },
    "brute_force_attack": {
        "title": "Victory.",
        "description": "You run at it with nothing but your strength and resolve and manage to defeat it... But you take significant damage in the process. You have proved yourself capable of surviving this treacherous land, there is no turning back now...",
        "options": {
            "continue": "Continue"

        },
    },
    "fight_them": {
        "title": "Skeleton.",
        "description": "You get the drop on it, you pull off an incredible dropkick, it's a skeleton, but you have knocked it too the ground with the kick...",
        "options": {
            "pin_them_to_the_ground": "Pin them to the ground",
            "attempt_to_flee": "Attempt to flee"

        },
    },
    "attempt_to_flee": {
        "title": "You cannot flee.",
        "description": "You have tried to run but the skeleton has kept up and it cannot get tired...",
        "options": {
            "face_them": "Face Them",
            "give_up": "Give up"

        },
    },
    "give_up": {
        "title": "You have given up.",
        "description": "You feel this challenge it too great to overcome so you have given in to your fate...",
        "options": {

        },
    },
    "face_them": {
        "title": "Bravery.",
        "description": "You have mustered up the courage to face the skeleton in battle...",
        "options": {
            "brute_force_attack": "Brute force attack"

        },
    },
    "pin_them_to_the_ground": {
        "title": "You have successfully restrained it.",
        "description": "Now you must choose what to do with the skeleton...",
        "options": {
            "finish_it": "Finish It",
            "talk_to_it": "Talk to it"

        },
    },
    "finish_it": {
        "title": "It's dead... Again.",
        "description": "You have successfully killed the undead... You have proved yourself capable of surviving this treacherous land, there is no turning back now...",
        "options": {
            "continue": "Continue"

        },
    },
    "talk_to_it": {
        "title": "It's futile...",
        "description": "It is not alive anymore it cannot converse like it once could...",
        "options": {
            "finish_it": "Finish it"

        },
    },
}

# Initialise variable to store the current room the player is in
current_room = "wake_up" 

 # Dictionary containing information about different items in the game
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

# Initialse inventory array
inventory = []

# Dictionary containing player statistics such as health, strength, etc.
player_stats = {
  "health": 100,
  "strength": 10,
  "magika": 100,
  "defense": 0,
  "agility": 5,
}

# Route for the home page
@app.route('/home')
def home():
    return render_template('home.html')

# Route for user login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user credentials
        if username in valid_credentials and valid_credentials[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')

# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# Route for user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'logged_in' in session:

        session.pop('logged_in', None)
        session.pop('username', None)
    return redirect(url_for('login'))

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in valid_credentials:
            return 'Username already exists. Please choose another.'
        # Register new user
        with open('user_credentials.txt', 'a') as file:
            file.write(f'{username},{password}\n\n')

        valid_credentials[username] = password

        return redirect(url_for('login'))

    return render_template('register.html')

# Route for the game page
@app.route('/game')
def game():
    room = rooms[current_room]
    if player_stats['health'] <= 0:

        return render_template('game_over.html')
    # Modify room options based on game state
    if current_room == "dark_room":
        if 2 not in inventory:
            room["options"]["pick_up_key"] = "Pick Up Key"
        else:
            room["options"].pop("pick_up_key", None)
    if 3 in inventory:
        room["options"]["use_potion"] = "Use Potion"
    else:
        room["options"].pop("use_potion", None)

    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

# Route for picking up the key item
@app.route('/pick_up_key')
def pick_up_key():
    global current_room
    # Check if user is in correct room
    if current_room == "dark_room":
        # Check if item is in user inventory
        if 2 not in inventory:
            # Add item to inventory and remove the option to do it again
            inventory.append(2)
            rooms[current_room]["options"].pop("pick_up_key", None)

    room = rooms[current_room]
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

# Route for using the health potion item
@app.route('/use_potion', methods=['GET'])
def use_potion():
    global player_stats
    global current_room

    if 3 in inventory:

        if player_stats["health"] < 100:

            player_stats["health"] += 40

            if player_stats["health"] > 100:
                player_stats["health"] = 100


            inventory.pop(binary_search(inventory, 0, len(inventory)-1, 3))

            return redirect(url_for('game'))
        else:
            player_stats["health"] = 100
            inventory.pop(binary_search(inventory, 0, len(inventory)-1, 3))

    room = rooms[current_room]
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

# Route for handling player movement within the game
@app.route('/move/<direction>', methods=['GET', 'POST'])
def move(direction):
    global current_room

    # Handle special case where player starts in "wake_up" room and moves to "dark_room"
    if current_room == "wake_up" and direction == "dark_room":
        current_room = direction

    # Get the options available in the current room
    current_options = rooms[current_room]["options"]

    # Update the current room based on the direction chosen by the player
    if direction in current_options:
        # Convert the direction to lowercase and replace spaces with underscores
        current_room = current_options[direction].lower().replace(" ", "_")

    # Get the details of the new current room
    room = rooms[current_room]

    # Adjust player stats based on specific room transitions or actions
    if current_room == "right_hook" or current_room == "talk_to_them" or current_room == "grab_sword":
        player_stats["health"] -= 10 
    if current_room == "uppercut":
        player_stats["health"] -= 50 
    if current_room == "brute_force_attack":
        player_stats["health"] -= 70 
    if current_room == "run_away" or current_room == "give_up":
        player_stats["health"] -= 100
    if current_room == "dark_room":
        # Add option to pick up key if it hasn't been collected yet
        if 2 not in inventory:
            room["options"]["pick_up_key"] = "Pick Up Key"
        else:
            room["options"].pop("pick_up_key", None)

    # Update room options based on inventory contents
    if 3 in inventory:
        room["options"]["use_potion"] = "Use Potion"
    else:
        room["options"].pop("use_potion", None)

    # Adjust room options based on specific conditions
    if current_room == "end_of_corridor":
        if 2 not in inventory:
            room["options"]["unlock"] = "Locked"
        else:
            room["options"]["unlock"] = "Unlock"
    
    # Add health potion to inventory if player chooses the right path
    if current_room == "right_path":
        inventory.append(3)
    
    # Check if player's health has reached zero, triggering game over
    if player_stats['health'] <= 0:
        return render_template('game_over.html')
    
    # Sort inventory after any changes
    sort_array(inventory)

    # Render the game template with updated room, inventory, items, and player stats
    return render_template('game.html', room=room, inventory=inventory, items=items, player_stats=player_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))