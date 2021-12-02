# #! /usr/bin/python3
# import sys
# from env import Debug, Q_HTTP
# from httpc_lib import httpclient
#
#
# def main(argv):
#     """The Entry Point of httpc"""
#
#     if len(argv) == 1 and argv[0] == "help":
#         help_info = """\nhttpc is a curl-like application but supports HTTP protocol only.
#
#     Usage:
#         httpc command [arguments]
#
#     The commands are:
#         get     executes a HTTP GET request and prints the response.
#         post    executes a HTTP POST request and prints the response.
#         help    prints this screen.
#
#     Use \"httpc help [command]\" for more information about a command."""
#
#         print(help_info)
#
#     elif len(argv) == 1 and argv[0] == "info":
#         info = "Develped by:\n@starfreck (https://github.com/starfreck)\n@ninanee (https://github.com/ninanee)"
#         print(info)
#
#     elif len(argv) == 2 and argv[0] == "help" and argv[1] == "get":
#         get_info = """\nUsage:
#         httpc get [-v] [-h key:value] URL
#
#     Get executes a HTTP GET request for a given URL.
#
#         -v              Prints the detail of the response such as protocol, status and headers.
#         -h key:value    Associates headers to HTTP Request with the format 'key:value'."""
#
#         print(get_info)
#
#     elif len(argv) == 2 and argv[0] == "help" and argv[1] == "post":
#         post_info = """\nUsage:
#         httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
#
#     Post executes a HTTP POST request for a given URL with inline data or from file.
#
#         -v              Prints the detail of the response such as protocol, status and headers.
#         -h key:value    Associates headers to HTTP Request with the format 'key:value'.
#         -d string       Associates an inline data to the body HTTP POST request.
#         -f file         Associates the content of a file to the body HTTP POST request.
#
#     Either [-d] or [-f] can be used but not both."""
#
#         print(post_info)
#
#     elif len(argv) > 1 and argv[0] == "get":
#         get_handler(argv[1:])
#     elif len(argv) > 1 and argv[0] == "post":
#         post_handler(argv[1:])
#     else:
#         default_info = Q_HTTP
#         print(default_info)
#         print("Invalid choice. Please try again!")
#         print('Usage:\n\thttpc (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL')
#
#
# def get_handler(argv):
#     """GET request handler"""
#     headers = None
#     verbose = False
#     redirect = False
#     output_file = None
#
#     # Process verbose
#     if "-v" in argv:
#         argv.remove("-v")
#         verbose = True
#     # Process header
#     if "-h" in argv:
#         location = argv.index("-h")
#         argv.remove("-h")
#         headers = argv[location]
#         argv.remove(headers)
#         headers = headers.split(",")
#     # Process Redirection
#     if "-r" in argv:
#         argv.remove("-r")
#         redirect = True
#     # Process output file
#     if "-o" in argv:
#         location = argv.index("-o")
#         argv.remove("-o")
#         output_file = argv[location]
#         argv.remove(output_file)
#
#     if len(argv) >= 1:
#         if Debug:
#             print("\nverbose:", verbose, "headers:", headers, "url:", argv[0], "\n")
#         # Call GET Method
#         httpclient(verbose=verbose, headers=headers, url=argv[0], output_file=output_file, redirection=redirect).get()
#     else:
#         print("Invalid choice. Please try again!")
#
#
# def post_handler(argv):
#     """POST request handler"""
#
#     file = None
#     string = None
#     headers = None
#     verbose = False
#     redirect = False
#     output_file = None
#
#     # Check if string and file are specified together
#     if "-d" in argv and "-f" in argv:
#         print("Either [-d] or [-f] can be used but not both.")
#         return
#     else:
#         # Process verbose
#         if "-v" in argv:
#             argv.remove("-v")
#             verbose = True
#         # Process header
#         if "-h" in argv:
#             location = argv.index("-h")
#             argv.remove("-h")
#             headers = argv[location]
#             argv.remove(headers)
#             headers = headers.split(",")
#         # Process Redirection
#         if "-r" in argv:
#             argv.remove("-r")
#             redirect = True
#         # Process string
#         if "-d" in argv:
#             location = argv.index("-d")
#             argv.remove("-d")
#             string = argv[location]
#             argv.remove(string)
#         # Process file
#         if "-f" in argv:
#             location = argv.index("-f")
#             argv.remove("-f")
#             file = argv[location]
#             argv.remove(file)
#         # Process output file
#         if "-o" in argv:
#             location = argv.index("-o")
#             argv.remove("-o")
#             output_file = argv[location]
#             argv.remove(output_file)
#         if len(argv) >= 1:
#             if Debug: print("\nverbose:", verbose, "headers:", headers, "url:", argv[0], "string:", string, "file:",
#                             file, "\n")
#             # Call POST Method
#             httpclient(verbose=verbose, headers=headers, url=argv[0], string=string, file=file, output_file=output_file,
#                        redirection=redirect).post()
#         else:
#             print("Invalid choice. Please try again!")
#
#
# def filter_args(argv):
#     """handle users wrong cmd input"""
#     for arg in argv:
#         if len(arg) == 3 and "--" in arg:
#             index = argv.index(arg)
#             argv[index] = arg.replace("--", "-")
#     return argv


#
#
# if __name__ == "__main__":
#     sys.argv = sys.argv[1:]
#     argv = filter_args(sys.argv)
#     main(argv)

import socket
import argparse
import re
import sys
from argparse import RawTextHelpFormatter
from packet import Packet
import ipaddress
from thread import myThread

url_regex = r"^((http?):\/)?\/?([^:\/\s\?]+)\/?([^:\/\s\?]+)?"


def syn(router_address, router_port, server_address, server_port):
    while True:
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_address))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            p = Packet(packet_type=1,
                       seq_num=1,
                       peer_ip_addr=peer_ip,
                       peer_port=server_port,
                       payload=message.encode("utf-8"))

            conn.sendto(p.to_bytes(), (router_address, router_port))
            print(" \n ")
            print("-------------------BEGINNING HANDSHAKE-----------------")
            print("[CLIENT] - Sending SYN - (PacketType = 1)")
            conn.settimeout(timeout)
            print('[CLIENT] - Waiting For A Response - Should be an SYN-ACK')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            print("[CLIENT] - Response is Received. Is it a SYN-ACK? (Packet Type of 2)")
            print('[CLIENT] - PacketType =  ', p.packet_type)

            if p.packet_type == 2:
                print("[CLIENT] - Yes, Got a SYN-ACK back, send back ACK (Packet Type of 3)")
                # just fucking send packet of type 3 send here and don't get anything back.
                return True

        except socket.timeout:
            print('[CLIENT] - No response after %d for Packet %d ' % (timeout, p.seq_num))
        finally:
            conn.close()


def ack(router_address, router_port, server_address, server_port):
    while True:
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_address))
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = 5
        try:
            # Packet type to 1 (SYN). Then have the server recognize the packet_type and return a 2 (SYN-ACK)
            p = Packet(packet_type=3,
                       seq_num=1,
                       peer_ip_addr=peer_ip,
                       peer_port=server_port,
                       payload=message.encode("utf-8"))

            print("[CLIENT] - Sending ACK")
            conn.sendto(p.to_bytes(), (router_address, router_port))

            # Receive a response within timeout
            conn.settimeout(timeout)
            print("[CLIENT] - Waiting For A Response -  (Should be an ACK)")
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)

            print("[CLIENT] - Response is Received. Is it a SYN-ACK? (Packet of Type 3)")
            print('[CLIENT] - PacketType = ', p.packet_type)
            print("[CLIENT] - Yes, Got an ACK back. Proceed with request.")
            return True

        except socket.timeout:
            print('[CLIENT] - No response after %ds for Packet %d ' % (timeout, p.seq_num))
        finally:
            conn.close()


# create parser to pull out url from the command line
parser = argparse.ArgumentParser(
    description='httpc is a curl-like application but supports HTTP protocol only',
    add_help=False, formatter_class=RawTextHelpFormatter)
parser.add_argument('--help', action='help', help='show this help message and exit')

parser.add_argument('mode', choices=['get', 'post'],
                    help="Executes a HTTP GET or POST request for a given URL with inline data")

# positional requirement (mandatory no dash)
parser.add_argument('url', action="store", help="mandatory uniform resource locator to perform request on")

# data command (optional)
parser.add_argument('-d', dest="data", action="store", metavar="inline-data",
                    help="associates inline data to the body HTTP POST")
# header command (optional)
parser.add_argument('-h', dest="header", action="store", metavar="inline-data",
                    help="associates headers to HTTP Request with the format")

# read from file command (optional)
parser.add_argument('-f', dest="file", action="store", metavar="inline-data",
                    help="associates the content of a file to the body HTTP POST")

# output to file(optional)
parser.add_argument('-o', dest="output", action="store", metavar="inline-data", help="stores terminal output in a file")

# verbose command (optional)
parser.add_argument('-v', '--verbose', action="store_true")

# port command (optional)
parser.add_argument('-p', '--port', help="server port", type=int, default=8007)

parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)
parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)

args = parser.parse_args()

# chop up the found url using regex
matcher = re.search(url_regex, args.url)

server = matcher.group(3)

query_param = ''
if matcher.group(4):
    query_param = matcher.group(4)

if args.port:
    port = args.port


def handshake():
    handShake = False
    # Always perform a handshake before initial request.
    while not handShake:
        sendSyn = False
        sendSyn = syn(args.routerhost, args.routerport, args.serverhost, args.serverport)

        # Only return true when the whole thing comes back. check at each step.
        if sendSyn:
            sendAck = ack(args.routerhost, args.routerport, args.serverhost, args.serverport)
            if sendAck:
                print("--------------------HANDSHAKE COMPLETE-----------------")
                handShake = True
    return True


# GET REQUEST
if args.mode == 'get':
    message = 'GET /' + query_param + ' HTTP/1.1\r\n'
    message += 'Host:' + server + ':' + str(port) + '\r\n'
    message += 'Connection: close\r\n'
    message += '\r\n'

    handShakeComplete = handshake()
    if handShakeComplete:

        objs = [myThread(i, "Thread", i, message, args.routerhost, args.routerport, args.serverhost, args.serverport)
                for i in range(10)]
        for obj in objs:
            obj.start()
        for ojb in objs:
            obj.join()

# POST REQUEST
if args.mode == 'post':
    if args.data:
        data = args.data
    if args.file:
        with open(args.file, "r") as myfile:
            data = myfile.read()

    print(data)
    data_bytes = data.encode()

    message = 'POST /' + query_param + ' HTTP/1.1\r\n'
    message += 'Content-length:' + str(len(data_bytes)) + '\r\n'
    message += 'Host:' + server + ':' + str(port) + '\r\n'
    message += 'Connection: close\r\n\r\n'
    message += data + '\r\n'
    handShakeComplete = handshake()
    if handShakeComplete:
        objs = [myThread(i, "Thread", i, message, args.routerhost, args.routerport, args.serverhost, args.serverport)
                for i in range(10)]
        for obj in objs:
            obj.start()
        for ojb in objs:
            obj.join()

# TODO Check that this still works.
# if(args.output):
#     f = open(args.output, 'w')
#     sys.stdout = f
#     connect()
#     f.close()
