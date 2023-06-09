import socket
import os


class Server:
   file_types = {
       "txt": "text/html; charset=utf-8",
       "html": "text/html; charset=utf-8",
       "jpg": "image/jpeg",
       "png": "image/png",
       "js": "text/javascript; charset=UTF-8",
       "css": "text/css",
       "ico": "image/x-icon",
       "gif": "image/gif"
   }

   forbidden_files = [b"server2.py"]
   moved_files = [b"index1.html", b"index2.html"]

   def __init__(self):
       self.sock = socket.socket()
       self.sock.bind(("127.0.0.1", 80))
       self.sock.listen()

   def connect_client(self):
       (self.client_socket, self.client_address) = self.sock.accept()

   def get_data(self):
       data = b""
       length = -1
       while True:
           response = self.client_socket.recv(1024)
           data += response


           if b"Content-Length" not in data and b"\r\n\r\n" in data:

               return data
           elif b"Content-Length" in data and b"\r\n\r\n" in data:
               arr = data.split(b"\r\n\r\n")
               if length == -1:
                   length = int(arr[0].split(b"Content-Length: ")[1].split(b"\r\n")[0])


               arr = b"\r\n\r\n".join(arr[1:])


               if len(arr) == length:
                   return data


   def authenticate(self, data: bytes):
       if data == b"":
           self.client_socket.close()
           return False, b""

       msg = data.split(b"\r\n")
       msg = msg[0].split(b" ")

       return True, msg

   def get_others(self, msg: bytes, is_forbidden: bool, is_moved: bool, is_supported: bool, is_understand: bool):
       data = b"""
               <html>
                   <body>
               """
       if b"calculate-next" in msg:
           num = msg.split(b"?")[-1]
           num = int(num.split(b"=")[-1].decode()) +1
           data += f"<h1> {num} </h1>".encode()
       elif b"calculate-area" in msg:
           num1 = msg.split(b"?")[-1]
           num1 = num1.split(b"&")
           num2 = int(num1[1].split(b"=")[-1])
           num1 = int(num1[0].split(b"=")[-1])
           data += f"<h1> {num1* num2 /2} </h1>".encode()

       elif is_forbidden:
           data += b"<h1> Error 403, file is Forbidden </h1>"

       elif is_moved:
           data += b"<h1> Error 302, file is moved </h1>"

       elif not is_supported:
           data += b"<h1> Error 415, file is not supported </h1>"

       elif not is_understand:
           data += b"<h1> Error 500, did not understand the request </h1>"

       else:
           data += b"<h1> Error 404, file is not found </h1>"
       data += b"""
                   </body>
               </html>
               """
       return data

   def send_msg(self, msg: bytearray):

       filename = msg[1][1:]
       if msg[1] == b"/":
           filename = b"index.html"

       # checking if the files are allowed to be sent
       is_forbidden = filename in self.forbidden_files
       is_moved = filename in self.moved_files
       is_supported = filename.split(b".")[-1].decode() in self.file_types
       is_understand = (msg[0] == b"GET") and (msg[2] == b"HTTP/1.1")

       # the last check
       is_allow = not is_forbidden and not is_moved and is_supported and is_understand
       # if msg[0] == b"POST" and is_supported:
       #     f = open("./uploads/post")

       if b"image?" in msg[1]:
           ft = bytes(msg[1])
           img_path = "./uploads/" + ft.split(b"image-name=")[-1].decode()
           data = f"""
           <html>
            <body>
                <img src='{img_path}' href='{img_path}' />"
            </body>
           </html>
            """.encode()

           ft = self.file_types[ft.split(b".")[-1].decode()]
           header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(data)}\r\nContent-Type:{ft} \r\n\r\n"

       elif os.path.isfile(filename) and is_allow:
           f = open(filename, "rb")
           data = f.read()
           f.close()

           ft = self.file_types[filename.split(b".")[-1].decode()]
           header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(data)}\r\nContent-Type:{ft} \r\n\r\n"

       else:
           data = self.get_others(filename, is_forbidden, is_moved, is_supported, is_understand)
           header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(data)}\r\nContent-Type:text/html; charset=utf-8 \r\n\r\n"

       final_response = header.encode()
       final_response += data

       self.client_socket.send(final_response)
       return True

   def get_msg(self, msg: bytes, data: bytes):

       fname = msg.split(b"file-name=")[-1].decode()
       is_supported = fname.split(".")[-1] in self.file_types
       response = b"""
                      <html>
                          <body>
                      """

       data = data.split(b"\r\n\r\n")
       data = b"\r\n\r\n".join(data[1:])


       if is_supported:
           f = open(f"./uploads/{fname}","wb")
           f.write(data)
           f.close()
           response += f"sucsefully uploaded {fname}".encode()
       else:
           response += b"<h1> File is not supported </h1>"

       response += b"""
            </body>
       </html>
       """
       header = f"HTTP/1.0 200 OK\r\nContent-Length:{len(response)}\r\nContent-Type:text/html; charset=utf-8 \r\n\r\n"
       final_response = header.encode()
       final_response += data

       self.client_socket.send(final_response)



def main():
   server = Server()
   while True:
       is_client = True
       while is_client:
           server.connect_client()
           print("client connected")
           data = server.get_data()
           (is_client, msg) = server.authenticate(data)
           if is_client:
               if msg[0] == b"POST":
                   is_client = server.get_msg(msg[1],data)
               else:
                   is_client = server.send_msg(msg)


if __name__ == "__main__":
   main()
