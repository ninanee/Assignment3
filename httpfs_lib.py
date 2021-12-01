import os
import json
import shutil
import socket
import datetime
import threading
from urllib.parse import urlparse

from env import Debug
from packet import Packet

FORMAT = 'utf-8'
BUFFER_SIZE = 102400


class httpserver:
    """This is the http class for Server side operations"""
    lock = threading.Lock()
    directory = "./data"
    is_get = is_post = False
    format = "text/plain"

    def __init__(self, verbose, directory):
        """Init required params"""
        self.verbose = verbose
        if directory is not None:
            self.directory = directory
        # For Path & Extra Params
        self.path = self.query = self.body = None

    def parse(self, request):
        header_lines = request[0].split("\r\n")

        # GET /get?course=networking&assignment=1 HTTP/1.1
        first_header_line = header_lines[0]
        req_type = str(first_header_line.split()[0]).upper()

        # Parse the path & query
        self.parse_url(first_header_line.split()[1])

        # Parse Headers
        for header_line in header_lines:
            header_line = str(header_line)
            if "application/json" in header_line:
                self.format = "application/json"
                break
            elif "application/xml" in header_line:
                self.format = "application/xml"
                break
            elif "text/html" in header_line:
                self.format = "text/html"
                break

        # Store the request body
        if len(request) > 1:
            self.body = request[1]

        # Get Request Type
        if "GET" == req_type:
            self.is_get = True
            return self.get_handler()
        elif "POST" == req_type:
            self.is_post = True
            return self.post_handler()

    def parse_url(self, url):
        parsed_url = urlparse(url)
        self.path = parsed_url.path
        self.query = parsed_url.query

    def get_handler(self):
        files = self.get_files()
        body = ""

        if self.path == "/" or len(set(self.path)) == 1 or not self.path:
            if "application/json" == self.format:
                body = json.dumps(files)
            elif "application/xml" == self.format:
                body = '<?xml version="1.0" encoding="UTF-8"?>'
                body += "<files>"
                for f in files:
                    body += "<file>" + f + "</file>"
                body += "</files>"
            elif "text/html" == self.format:
                body = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Files on 
                Server</title></head><body><h2>Files' List on Server</h2><ul> """
                for f in files:
                    body += "<li>" + f + "</li>"
                body += """</ul></body></html>"""
            else:
                body = "\n".join(files)
            return self.response_generator(code=200, body=body)
        elif len(self.path.split("/")) > 2:
            body = "401 Unauthorized.\n"
            body += "The requested URL " + self.path + " is not allowed to access.\n"
            body += "The requested file is located outside the working directory."
            return self.response_generator(code=401, body=body)
        else:
            file = [p for p in self.path.split("/") if p][0]
            if file in files:
                # Lock the file before reading it
                with self.lock:
                    with open(self.directory + '/' + file, 'r') as file:
                        body = file.read()
                filename = str(self.path)
                content_disposition = "Content-Disposition: attachment; filename=" + filename.replace("/", "")
                return self.response_generator(code=200, body=body, content_disposition=content_disposition)
            else:
                body = "404. There is an error.\n"
                body += "The requested URL " + self.path + " was not found on this server.\n"
                body += "That is all we know."

                return self.response_generator(code=404, body=body)

    def post_handler(self):
        files = self.get_files()
        body = ""

        if self.path == "/" or len(set(self.path)) == 1 or not self.path:
            body = "404. That’s an error.\n"
            body += "The requested URL " + self.path + " was not found on this server.\n"
            body += "We cannot create a file without a name.\n"
            return self.response_generator(code=404, body=body)

        elif len(self.path.split("/")) > 2:

            body = "401 Unauthorized.\n"
            body += "The requested URL " + self.path + " is not allowed to access.\n"
            body += "The requested file is located outside the working directory."
            return self.response_generator(code=401, body=body)

        else:
            file = [p for p in self.path.split("/") if p][0]

            # Check if it's Folder
            if os.path.isdir(self.directory + '/' + file):
                body = "401 Unauthorized.\n"
                body += "You are not allowed to create " + self.path + ".\n"
                body += "Folder is exist with provided name."

                return self.response_generator(code=401, body=body)
            else:
                # File exist
                if file in files:
                    if "overwrite=true" in str(self.query):
                        # Using Lock for thread safe
                        with self.lock:
                            self.create_file(file, self.body)
                        body = "File has been successfully overwritten."
                        return self.response_generator(code=204, body=body)
                    else:
                        # Using Lock for thread safe
                        with self.lock:
                            self.create_file(file, self.body, "a")
                        body = "File has been successfully updated."
                        return self.response_generator(code=204, body=body)
                else:
                    # Using Lock for thread safe
                    with self.lock:
                        self.create_file(file, self.body)
                    body = "File has been successfully created."
                    return self.response_generator(code=201, body=body)

    def response_generator(self, code, body, content_disposition=None):
        # Create Response
        response = ""
        if code == 200:
            response += "HTTP/1.1 200 OK\r\n"
        elif code == 201:
            response += "HTTP/1.1 201 Created\r\n"
        elif code == 204:
            response += "HTTP/1.1 204 No Content\r\n"
        elif code == 401:
            response += "HTTP/1.1 401 Unauthorized\r\n"
        elif code == 404:
            response += "HTTP/1.1 404 Not Found\r\n"

        response += "Date: " + self.get_time() + "\r\n"
        if content_disposition is not None:
            response += "Content-Type: text/plain\r\n"
            response += content_disposition + "\r\n"
        else:
            response += "Content-Type: text/html\r\n"
        response += "Content-Length: " + str(len(str(body).encode(FORMAT))) + "\r\n"
        response += "Server: httpfs/1.0\r\n"

        if code == 201:
            response += "Location: " + self.path + "\r\n"
        response += "\r\n"
        response += body

        return response

    def get_files(self):
        list_of_files = []
        for root, dirs, files in os.walk(self.directory, topdown=True):
            dirs.clear()
            for name in files:
                list_of_files.append(name)
        return list_of_files

    def get_time(self):
        return str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))

    def create_folder(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_file(self, name, text, mode="w"):
        f = open(self.directory + '/' + name, mode)
        f.write(text)
        f.close()

    def save(self, id, name, content):
        self.create_folder(self.directory + "/" + id)
        self.create_file(self.directory + "/" + id + "/" + name, str(content))

    def remove_old_outputs(self):
        try:
            shutil.rmtree(self.directory)
        except:
            pass


def run_server(port, verbose, directory):
    print("[Server] - Server Started.")
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #  This allows the address/port to be reused immediately instead of
    #  it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive.
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        conn.bind(('', port))

        while True:
            data, sender = conn.recvfrom(1024)
            t = threading.Thread(target=handle_client, args=(conn, data, sender, verbose, directory))
            # t.start()
            # t.join()

    finally:
        conn.close()


def handle_client(conn, data, sender, verbose, directory):
    try:
        p = Packet.from_bytes(data)
        print("[Server] - Request from Client @: ", sender)
        request = p.payload.decode(FORMAT)

        if verbose:
            print(request.strip(), "\n")

        server = httpserver(verbose=verbose, directory=directory)
        # Divide Request to 2 parts (Header & Body)
        request = request.split("\r\n\r\n")

        # Parse Request Here and Return the Response
        if p.packet_type == 0:
            print("[Server] - Request : ", p.packet_type)
            print("[Server] - Payload : ", type(request))
            print("[Server] - Payload : ", request)

            response = server.parse(request.encode(FORMAT))
            print("[Server] - Response : ", type(response))
            print("[Server] - Response : ", response)

            p.payload = response.encode()

            conn.sendto(p.to_bytes(), sender)

        # If packet type is 1, then perform a handshake. (done)
        # Client has sent a SYN, so the Server has to send back an SYN-ACK
        if p.packet_type == 1:
            print("[Server] - PacketType (SYN): ", p.packet_type)
            response = server.parse(request.encode(FORMAT))

            # response
            p.packet_type = 2
            p.payload = "SYN is Received. Here is your SYN-ACK".encode()
            print("[Server] - SYN is Received. Here is your SYN-ACK")
            conn.sendto(p.to_bytes(), sender)

        if p.packet_type == 3:
            # response
            response = server.parse(request.encode(FORMAT))
            p.packet_type = 3
            p.payload = "ACK is Received. Here is your ACK.".encode()
            print("[Server] - ACK is Received. Here is your ACK")
            conn.sendto(p.to_bytes(), sender)

    except Exception as e:
        print("[Server] - Error: ", e)
