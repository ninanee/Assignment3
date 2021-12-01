import os
import json
import socket
from env import Debug
from urllib.parse import urlparse


# It supports 330 Redirections due to Recursion Stack
# import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(1500)
# print(sys.getrecursionlimit())

class httpclient:
    """This is the http class for client side operations"""
    port = 80
    FORMAT = 'utf-8'
    BUFFER_SIZE = 102400
    is_get = is_post = None

    def __init__(self, verbose, headers, url, string=None, file=None, output_file=None, redirection=False):
        """Init required params"""
        self.verbose = verbose
        self.redirection = redirection
        self.headers = headers
        # Define URL Vars
        self.parsed_url = self.host = self.path = self.query = None
        # Parse URL
        self.parse_url(url)
        # Extra Params for POST
        self.string = string
        self.file = file
        self.output_file = output_file
        # self.parsed_url.hostname

    def parse_url(self, url):
        self.parsed_url = urlparse(url)
        self.host = self.parsed_url.netloc
        self.path = self.parsed_url.path
        self.query = self.parsed_url.query
        if self.parsed_url.port is not None:
            self.port = self.parsed_url.port
            self.host = self.host.split(":")[0]

    def is_json_data(self):
        if self.headers is not None and "application/json" in self.headers:
            return True
        return False

    def to_json(self, string):
        return json.dumps(json.loads(string))

    def save_as_file(self, response):
        if not os.path.isdir("./Downloads/"):
            os.makedirs("./Downloads/")
        with open("./Downloads/" + self.output_file, 'w') as file:
            file.write(response)

    def is_redirect(self, response):
        header_lines = response[0].split("\r\n")
        code = str(header_lines[0].split()[1])
        if code.startswith("3"):
            return True
        return False

    def redirect(self, response):
        header_lines = response[0].split("\r\n")
        location = "Location: "
        for line in header_lines:
            if location in line:
                index = line.find(location) + len(location)
                new_url = line[index:]
                if Debug: print("""--------------------------------------------------------""")
                if Debug: print("Redirections Detected:", new_url)
                if Debug: print("""--------------------------------------------------------""")
                self.parse_url(new_url)
                break
        if self.is_get:
            self.get()
        if self.is_post:
            self.post()

    def get(self):
        """ Build GET and send to host"""
        request = ""
        request += "GET " + self.path + "?" + self.query + " HTTP/1.1\r\n"
        request += "Host: " + self.host + "\r\n"
        request += "User-Agent: Concordia-HTTP/1.0\r\n"
        if self.headers is not None:
            for header in self.headers:  # Multiple Headers
                request += str(header).strip() + "\r\n"

        # Ending of the request or body
        request += "\r\n"
        # Pass this data to TCP Client

        # Show the GET request
        if Debug: print("""-----------------------GET REQUEST------------------------""")
        if Debug: print(request)
        if Debug: print("""-------------------------RESPONSE------------------------""")

        # Pass this data to TCP Client
        self.is_get = True
        self.run_client(request)

    def post(self):
        """ Build POST and send to host"""

        # Guard
        if self.string and self.file is not None:
            print("Either [-d] or [-f] can be used but not both.")
            return

        # Start Building our POST request
        request = ""
        request += "POST " + self.path + "?" + self.query + " HTTP/1.1\r\n"
        request += "Host: " + self.host + "\r\n"
        request += "User-Agent: Concordia-HTTP/1.0\r\n"

        # Add Headers
        if self.headers is not None:
            for header in self.headers:  # Multiple Headers
                request += str(header).strip() + "\r\n"

        # Load file as string in self.file if file is present
        if self.file is not None:
            with open(self.file, 'r') as f:
                self.file = f.read().replace('\n', '')

        # See if the data is JSON
        if self.is_json_data():
            if self.string is not None:
                self.string = self.to_json(self.string)
            if self.file is not None:
                with open(self.file, 'r') as f:
                    self.file = self.to_json(self.file)

        # Add Content-Length in Header
        if self.string is not None:
            request += "Content-Length: " + str(len(self.string)) + "\r\n"
        if self.file is not None:
            request += "Content-Length: " + str(len(self.file)) + "\r\n"

        # Ending of the request header
        request += "\r\n"

        # Adding POST Body
        if self.string is not None:
            request += self.string
        if self.file is not None:
            request += self.file

        # Show the post request
        if Debug: print("""-----------------------POST REQUEST------------------------""")
        if Debug: print(request)
        if Debug: print("""-------------------------RESPONSE------------------------""")

        self.is_post = True
        # Pass this data to TCP Client
        self.run_client(request)

    def run_client(self, request):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #  This allows the address/port to be reused immediately instead of
        #  it being stuck in the TIME_WAIT state for several minutes, waiting for late packets to arrive.
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            client.connect((self.host, self.port))
            request = request.encode(self.FORMAT)
            client.sendall(request)
            # MSG_WAITALL waits for full request or error
            response = client.recv(self.BUFFER_SIZE)

            response = response.decode(self.FORMAT)
            response = response.split("\r\n\r\n")

            # Check Response
            if len(response) >= 2:
                if self.is_redirect(response) and self.redirection:
                    self.redirect(response)
                else:
                    if self.verbose:
                        print(response[0].strip(), "\n")
                    print(response[1].strip())
                    if self.output_file is not None:
                        self.save_as_file(response[1].strip())
            else:
                if Debug:
                    print("Response:\n", response, "\n")
                print("Oops! Something went wrong ;(")
        finally:
            client.close()
