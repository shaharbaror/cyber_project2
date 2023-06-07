import json
import time
import os
from random import randint

from Protocol import Protocol
from mememaker import MemeMaker



# If the header contains "index" in it then go to this function
def index_functions(header, body, player_ip):
    ip = player_ip
    print(ip)
    body = body.split("\n")
    username = body[0]
    action = header[1].split("?")[-1]
    print(action)
    if action == "a=c":

        # create a new lobby for players

        with open("lobbies.json", "r") as f:
            lobbies = json.load(f)
            lobby = Protocol.generate_lobby_name()
            print("goes")

            while lobby in lobbies:
                lobby = Protocol.generate_lobby_name()

            print("generated:" + lobby)
            lobbies[lobby] = Protocol.new_lobby(username, ip)

        with open("lobbies.json", "w") as f:
            json.dump(lobbies, f)

        print(Protocol.create_msg(f"{lobby}".encode(), "text/txt"))
        return Protocol.create_msg(f"{lobby}".encode(), "text/txt")
    # add a player to a lobby he chose to join
    if "a=j" in action:
        lobby = header[1].split("/")[0]

        with open("lobbies.json", "r") as f:
            lobbies = json.load(f)
            lobbies[lobby] = Protocol.add_player(username, ip, lobbies[lobby])

        with open("lobbies.json", "w") as f:
            json.dump(lobbies, f)

        return Protocol.create_msg(lobby.encode(), "text/txt")


# if the header contains "firstpage" in it then go to this function
def first_page_functions(header, body, ip = "128.0.0.1"):
    lobby_name = header[1].split("/")[0]
    with open("lobbies.json", "r") as f:
        lobbies = json.load(f)
    lobby = lobbies[lobby_name]

    if ip not in lobby["players_ip"]:
        return Protocol.create_msg('{"send": true}'.encode(), "text/json")

    if "s=t" in header[1]:

        # submit the meme into the right lobby

        meme = json.loads(body)

        for i in range(len(lobby["players"])):

            if lobby["players"][i] == lobby["players"][ip]:

                lobby["finished"][i] = True
                lobby["memes_this_round"].append(Protocol.prepare_meme(meme, i))
                lobbies[lobby_name] = lobby

        with open("lobbies.json", "w") as f:
            json.dump(lobbies, f)

    else:
        if "a=startgame" in header[1]:

            # send the user all the required data for sarting the meme

            rnd = randint(1, 2)
            roll_amount = 5
            timer = 240 #need to make it so that the timer wont reset every time a player joins the game


            player_index = lobby["players_ip"].index(ip)


            lobby["round_timer"] = int(time.time() + timer)
            print(lobby["remaining_rolls"][player_index])

            # if a player already has used up all of his rolls, and he refreshes then just get him his meme back
            if lobby["started"][player_index]:
                msg = Protocol.update_json(lobby["players_meme"][player_index])
                msg += (f', "time": {int(lobby["round_timer"] - time.time())}' + "}").encode()
                print(msg)
                return Protocol.create_msg(msg, "text/json")

            lobby["remaining_rolls"][player_index] = roll_amount
            lobby["started"][player_index] = True
            lobby["players_meme"][player_index] = rnd
            lobbies[lobby_name] = lobby
            with open("lobbies.json", "w") as f:
                json.dump(lobbies, f)

            msg = Protocol.update_json(rnd)
            msg += (f', "time":{timer}' + "}").encode()
            print(msg)
            return Protocol.create_msg(msg, "text/json")

        if "a=newmeme" in header[1]:

            rnd = randint(1, 2)
            print("got there")

            players_index = lobby["players_ip"].index("127.0.1.2")
            for i in range(len(lobby["players_ip"])):
                print(lobby["players_ip"][i])

                if lobby["players_ip"][i] == ip:
                    if lobby["remaining_rolls"][i] >= 1:
                        lobby["remaining_rolls"][i] -= 1
                        lobby["players_meme"][i] = rnd
                        print(lobby["remaining_rolls"][i])
                        new_meme = Protocol.update_json(rnd)
                        new_meme += "}".encode()
                        lobbies[lobby_name] = lobby
                        with open("lobbies.json", "w") as f:
                            json.dump(lobbies, f)
                        print(new_meme)
                        return Protocol.create_msg(new_meme, "text/json")
                    else:
                        return Protocol.create_msg('{"is_ok":false}'.encode(), "text/json")

        if "a=gettime" in header[1]:
            timer = str(time.time() - lobby["round_timer"])

            return Protocol.create_msg(timer.encode(), "text/txt")


def ratememe_functions(header,body, ip):
    lobby_name = header[1].split("/")[0]

    if "getmeme" in header[1]:
        with open("lobbies.json", "r") as f:
            lobbies = json.load(f)
            lobby = lobbies[lobby_name]
            if len(lobby["memes_this_round"]) > 0:
                if not lobby["memes_this_round"][0] == {}:
                    lobby["all_memes_made"].append(lobby["memes_this_round"][0])
                lobby["memes_this_round"] = lobby["memes_this_round"][1:]

                msg = Protocol.prepare_meme(lobby["memes_this_round"][0], -1)
            else:
                # if the players are done with rating all of the memes this round
                msg = ("{" + '"has_finished":true' + "}").encode()
            return Protocol.create_msg(msg, "text/json")

    if "rated" in header[1]:
        rating = header[1][-1]
        with open("lobbies.json", "r") as f:
            lobbies = json.load(f)
            lobby = lobbies[lobby_name]

        if rating == 0:
            lobby["memes_this_round"]["score"] += 1
        elif rating == 2:
            lobby["memes_this_round"]["score"] -= 1

        lobbies[lobby_name] = lobby
        with open("lobbies.json", "w") as f:
            json.dump(lobbies, f)
        return Protocol.create_msg("done".encode(), "text/txt")
    # If player needs the first meme get them the first meme, after everyone done voting: get the meme to the all_time_meme zone and update the player's score


def check_for_errors(header, body, ip):
    some_error = None
    lobby_name = header[1].split("/")[0]

    with open("lobbies.json", "r") as f:
        lobbies = json.load(f)

    if (lobby_name not in lobbies) and (not os.path.isfile(lobby_name)):
        some_error = "404 not found"

    if some_error:
        msg = f'''
                <html>
                    <body>
                        <h1> {some_error} </h1>
                    </body>
                </html>
                '''.encode()
        return Protocol.create_msg(msg, "text/html")
    return b"ok"

class HandleResponse:

    @staticmethod
    def handle_request(request, ip):
        print("ehy")

        header, body = Protocol.proces_request(request)
        header[1] = header[1][1:]
        # header: 127.0.0.1/firstpage/WHDSK?s=f&a=something

        # header: 127.0.0.1/index?a=c

        is_error = check_for_errors(header, body, ip[0])
        if not is_error == b"ok":
            return is_error

        # get info about the file and its name
        file_name = header[1].split("/")
        if len(file_name) > 1:
            file_name = file_name[1:]
            file_name = "/".join(file_name)
        else:
            file_name = file_name[0]

        header_without_lobby = header[1].split("/")
        if len(header_without_lobby) > 2:
            header_without_lobby = header_without_lobby[2:]
        else:
            header_without_lobby = header_without_lobby[1:]
        header_without_lobby = "/".join(header_without_lobby)
        print(header)
        print(file_name)

        # if the file is accessible then access and send it
        if os.path.isfile(file_name) or file_name == "":
            if file_name == "":
                file_name = "index.html"
            file_type = Protocol.get_file_type(file_name)

            with open(file_name, "rb") as f:
                f = f.read()
                msg = Protocol.create_msg(f, file_type)
                print(msg)
                return msg

        print(header_without_lobby)

        # if the request is fetch then respond correctly
        if "index" in header_without_lobby:
            print("ok")
            return index_functions(header, body, ip[0])
        if "firstpage" in header_without_lobby:
            print("here")
            return first_page_functions(header, body)
        if "ratememe" in header_without_lobby:
            return ratememe_functions(header, body, ip[0])
        return Protocol.create_msg(b" ", "text/txt")

