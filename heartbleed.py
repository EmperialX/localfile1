import sys
import socketserver
import string
import threading
from time import sleep
from colorama import Fore, Style

caption = """
=================================
HEARTBLEED
=================================
"""

class Service(socketserver.BaseRequestHandler):
    def print_out(self, message, hang=0.04):
        for character in message:
            self.send(character.encode("utf-8"), newline=False)
            if character in string.punctuation:
                sleep(hang * 4)
            else:
                sleep(hang)

    def handle(self):
        self.send(Fore.GREEN + Style.BRIGHT + caption + Fore.RESET + Style.NORMAL)
        self.print_out("THANK YOU FOR CONNECTING TO THE SERVER.\n")

        while True:
            self.send("\n")
            self.print_out("TO VERIFY IF THE SERVER IS STILL THERE, PLEASE SUPPLY A STRING.\n\n")
            sleep(1)
            self.print_out("STRING ['apple']: ")
            self.send(Fore.YELLOW + Style.BRIGHT)
            entered = self.receive("")
            self.send(Fore.RESET + Style.NORMAL)

            if entered == "apple":
                size = len(entered)
                self.print_out("LENGTH ['%d']: " % size)
                sleep(1)
                self.send(Fore.YELLOW + Style.BRIGHT)
                length = self.receive("")
                self.send(Fore.RESET + Style.NORMAL)

                if length == "":
                    length = int(size)

                length = int(length)
                with open('file', 'r+') as h:
                    original = h.read()
                    if len(original) > 20000 or size > 20000:
                        self.print_out("\n... THE SERVER IS OVERLOADED. PLEASE TRY AGAIN LATER.\n\n")
                        return

                    new = original.replace("#@", "#@" + entered + "@", 1)
                    new = new.replace("# @", "#@" + entered + "@", 1)
                    h.seek(0)
                    h.write(new)
                    h.truncate()

                with open('file', 'r') as n:
                    returned = n.read(2 + length)[2:].split("###ENDDELIMETER###")[0].lstrip()
                    if "flag{bfca3d71260e581ba366dca054f5c8e5}" in returned:
                        returned = returned.replace(
                            "flag{bfca3d71260e581ba366dca054f5c8e5}",
                            Fore.GREEN + Style.BRIGHT + "flag{bfca3d71260e581ba366dca054f5c8e5}" + Fore.CYAN + Style.BRIGHT,
                        )
                        self.print_out("\n... THE SERVER RETURNED:\n\n")
                        sleep(1)
                        self.send(Fore.CYAN + Style.BRIGHT)
                        self.print_out(returned, 0.01)
                        self.send(Fore.RESET + Style.NORMAL)
                        sleep(1)

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")
        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip().decode("utf-8")

class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    port = 6573
    host = "0.0.0.0"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server started on " + str(server.server_address) + "!")

if __name__ == "__main__":
    main()
