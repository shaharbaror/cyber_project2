import json
import os
from socket import create_server
from select import select
from random import randint
import time

from HandleResponse import HandleResponse
from Protocol import Protocol
from mememaker import MemeMaker

#['GET', '127.0.0.1/FirstPage?s=t&i=2&c=%20Caption%201%20hello%20my%20frient,Caption%202', 'HTTP/1.1']
class Server:


    def __init__(self, address, port):
        self.port = port
        self.address = address
        self.s = create_server(("127.0.0.1", 8000))
        self.s.listen(9)
        self.clients = {}
        self.running = True

    def handle_request(self, requests, ip):
        return HandleResponse.handle_request(requests, ip)
        # print(ip)
        # header, body = Protocol.proces_request(requests)
        # http_header = ""
        # header[1] = header[1][1:]
        # print(header)
        # if os.path.isfile(header[1]) or header[1] == "":
        #     if header[1] == "":
        #         header[1] = "index.html"
        #     with open(header[1], "rb") as f:
        #         f = f.read()
        #
        #         file_type = Protocol.get_file_type(header[1])
        #         msg = Protocol.create_msg(f, file_type)
        #         return msg
        # if "ratememe" in header[1]:
        #     if "getmeme" in header[1]:
        #         with open("lobby1.json", "r") as f:
        #             data = json.load(f)
        #             print(data["memes_this_round"][0]["text"])
        #             data["memes_this_round"][0]["style"] = MemeMaker.getStyles(data["memes_this_round"][0]["index"])
        #                 #the PROBLEM IS HERE
        #             return Protocol.create_msg(data["memes_this_round"][0], "text/json")
        #
        #
        # if "makeuser/s" in header[1]:
        #     rnd = randint(1, 80000)
        #     with open("lobby1.json", "r") as f:
        #         data = json.load(f)
        #         while str(rnd) in data["players_id"]:
        #             rnd = randint(1, 80000)
        #
        #         data["players_id"].append(str(rnd))
        #         data["players"].append(body[1:-1])
        #         data["players_finished"].append(False)
        #         data["players_score"].append(0)
        #         data["remaining_rolls"].append(0)
        #
        #     with open("lobby1.json", "w") as f:
        #         json.dump(data, f)
        #
        #     return Protocol.create_msg(str(rnd).encode(), "text/txt")
        #     # make it so the username is added to the lobby with the correct id and send the user its id
        # if "FirstPage" in header[1]:
        #     status = header[1].split("?")[1:]
        #     status = "?".join(status).split("&")
        #
        #     if status[0] == "s=t":
        #         print("hi")
        #
        #         bodies = json.loads(body)
        #         print(bodies)
        #         with open("lobby1.json", "r") as f:
        #             data = json.load(f)
        #             print(data["players"])
        #
        #             for i in range(len(data["players_id"])):
        #                 print(data["players"][i])
        #                 if bodies["player_id"] == data["players_id"][i] and not data["players_finished"][i]:
        #                     data["players_finished"][i] = True
        #                     meme_submition = {"index": bodies["memeIndex"], "text": bodies["captions"], "creator": i}
        #                     data["memes_this_round"].append(meme_submition)
        #         with open("lobby1.json", "w") as f:
        #             json.dump(data, f)
        #
        #         # needs to send all the players that another player has finished
        #
        #
        #
        #     else:
        #         action = status[1][2:]
        #         if action == "startgame":
        #             # with open("response.json", "wb") as r:
        #             #     r.write(b'"time" : 20')
        #             rnd = randint(1, 2)
        #             roll_amount = 5
        #             with open("lobby1.json", "r") as f:
        #                 data = json.load(f)
        #                 data["round_timer"] = int(time.time() + 120)
        #                 data["round_rolls"] = roll_amount
        #                 for i in range(len(data["remaining_rolls"])):
        #                     data["remaining_rolls"][i] = roll_amount
        #
        #             with open("lobby1.json","w") as f:
        #                 json.dump(data, f)
        #             print(time.time())
        #             timer = 120
        #
        #             msg = Protocol.update_json(rnd, timer)
        #             msg = Protocol.create_msg(msg, "text/json")
        #
        #             return msg
        #
        #         if action == "newmeme":
        #             rnd = randint(1, 2)
        #             with open("lobby1.json", "r") as f:
        #
        #                 data = json.load(f)
        #
        #                 # need to get the index of the id, to find how many rolls are left and if enough then allow if not then dont
        #
        #                 player_id = status[2][2:]
        #                 if str(player_id) not in data["players_id"]:
        #                     return Protocol.create_msg('{"isOk":false, }'.encode(),"text/json")
        #                 player_index = data["players_id"].index(str(player_id))
        #             if data["remaining_rolls"][player_index] > 0:
        #
        #                 data["remaining_rolls"][player_index] -= 1
        #                 json_file = Protocol.update_json(rnd, data["round_timer"] - time.time())
        #                 print(json_file)
        #                 with open("lobby1.json","w") as f:
        #                     json.dump(data, f)
        #                 return Protocol.create_msg(json_file, "text/json")
        #             else:
        #                 json_file = '{"isOk": false}'
        #                 return Protocol.create_msg(json_file.encode(), "text/json")
        #
        #         if action == "getplayersdone":
        #
        #             with open("lobby1.json", "r") as f:
        #                 data = json.load(f)
        #             players_done = data["players_finished"].count(True)
        #             response = f'{players_done} \n {players_done}/{len(data["players"])} are done'
        #             return Protocol.create_msg(response.encode(),"text/txt")
        #
        #
        # return Protocol.create_msg(b" ", "text/txt")

    def handle_post(self, data):
        header, body = Protocol.proces_request(data)
        print(body)
        header[1] = header[1][1:]
        if "firstpage" in header[1]:
            status = header[1].split("?")[1:]
            status = "?".join(status).split("&")
            if status[0] == "s=t":
                with open("lobby1.json", "r") as f:
                    lobby_data = json.load(f)
        return b" "

    def accept(self):

        readable, _, _ = select([self.s], [], [])

        if self.s in readable:

            connection, address = self.s.accept()
            self.clients.update({connection: address})

    def respond(self):
        if len(self.clients.keys()) > 0:
            readable, _, _ = select(self.clients.keys(), [], [])

            for client in readable:

                data = Protocol.receive(client).decode()

                client.send(HandleResponse.handle_request(data, self.clients[client]))
                self.clients.pop(client)

    def run(self):
        while self.running:

            self.accept()

            self.respond()


def main():
    server = Server("127.0.0.1", 8000)
    server.run()


if __name__ == "__main__":
    main()