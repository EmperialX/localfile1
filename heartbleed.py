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
        self.print_out("THANK YOU FOR CONNECTING TO THE SERVER.\n\n")

        while True:
            self.send("\n")
            self.print_out("TO VERIFY IF THE SERVER IS STILL THERE, PLEASE SUPPLY A STRING.\n\n")
            sleep(1)
            
            self.print_out("STRING ['apple']: ")
            entered = self.receive("").strip()
            if entered == "apple":
                size = len(entered)
                self.print_out("LENGTH ['%d']: "% size)
                sleep(1)
                length = int(self.receive("").strip())
                
                if length <= 0:
                    length = size
                elif length > 20000 or size > 20000:
                    self.print_out("\n... THE SERVER IS OVERLOADED. PLEASE TRY AGAIN LATER.\n\n")
                    continue

                original = open("file").read()
                new = original.replace("#@", "#@" + entered + "@", 1).replace("# @", "#@" + entered + "@", 1)
                with open("file", "w") as f:
                    f.write(new)

                returned = open("file").read(2 + length).split("###ENDDELIMETER###")[0].strip()
                if "flag{bfca3d71260e581ba366dca054f5c8e5}" in returned:
                    returned = returned.replace("flag{bfca3d71260e581ba366dca054f5c8e5}",
                                                Fore.GREEN + Style.BRIGHT + "flag{bfca3d71260e581ba366dca054f5c8e5}" +
                                                Fore.CYAN + Style.BRIGHT)
                self.print_out("\n... THE SERVER RETURNED:\n\n")
                self.print_out(returned, 0.01)
                sleep(1)

    def send(self, string, newline=True):
        if isinstance(string, str):
            string = string.encode("utf-8")
        if newline:
            string += b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip().decode("utf-8")

class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    port = 7333
    host = "0.0.0.0"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server started on " + str(server.server_address) + "!")

    # Now let the main thread just wait...
    while True:
        sleep(10)

if __name__ == "__main__":
    main()
