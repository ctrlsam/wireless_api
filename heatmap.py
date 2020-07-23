from zonedirector import ZoneDirector
from network_manager import NetworkController
from time import sleep
from threading import Thread

def update():
    while True:
        clients = zd.get_clients()
        nw.update(clients)
        sleep(1)


if __name__ == "__main__":
    zd = ZoneDirector('monitor', 'monitor')
    nw = NetworkController()

    clients = zd.get_clients()
    nw.update(clients, init=True) 

    # start scanning
    Thread(target = update).start()  

    while True:
        output = ""
        for ap in nw.get_stats():
            output += f"| {ap['ap-name']}: {ap['users']}"
        print(output)
