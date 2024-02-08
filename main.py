from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, emit,SocketIO,ConnectionRefusedError
import os
import random
from string import ascii_uppercase
app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
#config for getting it to run on codermerlin
socketio = SocketIO(app)
#dictionary with rooms and their corresponding codes
rooms = {}
socketCount = 0
allocatedMem = 300
print(allocatedMem)

#memory check function
def memCheck(room):
    if socketCount*70> allocatedMem*1000 - 10:
        print(f"memory close to being exceeded refusing connection for {room}")
        print(allocatedMem*1000 -10,socketCount*70)
        return True
    else:
        print("safe amount of memory is being used")
        return False


#room code generator
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code




@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    #get form data
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
    #error for not entering a name in the home screen
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
    #error for if you try and join a room without a code
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
    # if you enter a code set it to room else if the code isnt in the dict return an error
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect("room")

    return render_template("home.html")




@app.route("/room")
def room():
    #if you try and load the room route without being in a room or without a name it redirects you to the homepage
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect("/")
    #all goes well? cool! you get loaded into a room
    return render_template("room.html", code=room, messages=rooms[room]["messages"])
#socketio message event listener
@socketio.on("message")
def message(data):
    #gets session and if the session doesnt exist return none
    room = session.get("room")
    if room not in rooms:
        return 
    #when ever a message is sent get the name and message data from the websocket
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")




#socketio connection event listener
@socketio.on("connect")
def connect(auth):
    #socket counting for memory management
    global socketCount
    socketCount += 1
    #session data
    room = session.get("room")
    name = session.get("name")
    #memory check
    if memCheck(room):
        raise ConnectionRefusedError(f"out of memory connection refused please wait to try opening another chatroom \n allocated memory(MB): {allocatedMem} \n socketMemory(MB): {socketCount*70/1000}")
    else:
        print("memory good")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")




@socketio.on("disconnect")
def disconnect():
    global socketCount
    socketCount = socketCount-1
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")



if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0", port="12199",debug=True, allow_unsafe_werkzeug=True)
