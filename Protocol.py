import json
from random import randint

from mememaker import MemeMaker


class Protocol:

    @staticmethod
    def receive(socket):
        return socket.recv(1024)

    # receives the http request and returns the type of request
    @staticmethod
    def proces_request(request):
        data = request.split("\r\n\r\n")
        header = data[0].split("\r\n")
        header = header[0].split(" ")

        response = {
            "header_top": header,
            "type": header[0],
            "body": data[1]
        }
        return header, data[1]

    @staticmethod
    def get_file_type(filenames):

        filename = filenames.split(".")[-1]

        if 'jpg' in filename or 'jpeg' in filename or 'ico' in filename or 'gif' in filename or 'png' in filename:
            filename = f"image/{filename}"
        elif 'js' in filename:
            filename = f"text/javascript"
        else:
            filename = f"text/{filename}"

        return filename

    @staticmethod
    def create_msg(body: bytes, body_type):
        # gets the message body and its type, and returns the full http request template for use
        header = f"HTTP/1.0 200 OK \r\nContent-Length:{len(body)}\r\nContent-Type:{body_type}; charset=utf-8\r\n\r\n"
        response = header.encode()
        response += body
        return response

    @staticmethod
    def create_msg_lasting(body: bytes, body_type):

        # gets the message body and its type, and returns the full http request template for use
        header = f"HTTP/1.0 200 OK\r\nConnection: keep-alive \r\nContent-Length:{len(body)}\r\nContent-Type:{body_type}; charset=utf-8\r\n\r\n"
        response = header.encode()
        response += body
        return response

    @staticmethod
    def update_json(rnd: int):

        styles = MemeMaker.getStyles(rnd)
        captions = MemeMaker.get_caption_amount(rnd)

        res = ("{" + f'''
                "is_ok": true,
               "memeIndex": {rnd},
               "captions": {captions},
               "styles":"{f'{styles}'[2:][:-1]}"
               
               ''').encode()
        return res

    @staticmethod
    def prepare_meme(meme, creator):
        player = creator
        if player == -1:
            player = meme["creator"]
        res = ("{" + f'''
                "creator":{player},
                "captions":{len(meme["captions"])},
                "styles":{MemeMaker.getStyles(meme["index"])},
                "content":{meme["captions"]}
            ''' + "}").encode()

        return res
        # styles = MemeMaker.getStyles(index)
        # captions = MemeMaker.get_caption_amount(index)
        #
        # res = ("{" + f'''
        #                 "creator": {creator},
        #                "captions": {captions},
        #                "styles":"{f'{styles}'[2:][:-1]}",
        #                "content":{captions2},
        #                ''' + "}").encode()
        #
        # return res

    @staticmethod
    def generate_lobby_name():
        word = ""
        for i in range(8):
            word += chr(randint(ord('A'), ord('Z')))
        print(word)
        return word

    @staticmethod
    def new_lobby(username, ip):
        # #option 1
        # with open("lobbies.json","r") as f:
        #     lobbies = json.load(f)
        #     with open("cleanLobby.json","r") as f2:
        #         clean_lobby = json.load(f2)
        # clean_lobby["players"][ip] = username
        # lobbies[lobby] = clean_lobby
        # with open("lobbies.json", "w") as f:
        #     json.dump(lobbies, f)

        # option 2
        with open("cleanLobby.json", "r") as f:
            clean_lobby = json.load(f)

        clean_lobby["players"].append(username)
        clean_lobby["players_ip"].append(ip)
        clean_lobby["score"].append(0)
        clean_lobby["finished"].append(False)
        clean_lobby["remaining_rolls"].append(0)
        clean_lobby["started"].append(False)

        return clean_lobby

    @staticmethod
    def add_player(username, ip, lobby):

        lobby["players"].append(username)
        lobby["players_ip"].append(ip)
        lobby["score"].append(0)
        lobby["finished"].append(False)
        lobby["remaining_rolls"].append(0)
        lobby["started"].append(False)
        lobby["players_meme"].append(-1)

        return lobby
