from datetime import datetime

class Client:

    def __init__(self, mac, user, location):
        self.mac = mac
        self.user = user
        self.locations = [location]

    def move(self, new_location):
        self.locations.append(new_location)

    def get_location(self):
        return self.locations[len(self.locations)-1]


class NetworkController:

    def __init__(self, output=True):
        self.accessPoints = []
        self.output = output

    def get_ap_by_name(self, name):
        ''' Return AP, create if not found '''
        for ap in self.accessPoints:
            if ap.name == name:
                return ap
        self.accessPoints.append(AccessPoint(name))
        return self.accessPoints[len(self.accessPoints)-1]

    def get_client_ap(self, client_mac):
        ''' Get client's AP '''
        for ap in self.accessPoints:
            for c in ap.clients:
                if c.mac == client_mac:
                    return ap
        return None

    def add_client(self, client):
        ''' Add client to AP '''
        self.get_ap_by_name(client.get_location()).add_client(client)

    def get_stats(self):
        responce = []
        for ap in self.accessPoints:
            json = {
                'ap-name': ap.name,
                'users': len(ap.clients)
            }
            responce.append(json)
        return responce

    def update(self, clients, init=False):
        ''' Update how the network has changed since last update '''
        # TODO: TIDY AND MAKE EFFICIENT!!
        for client in clients:
            client_ap = self.get_client_ap(client['mac'])

            # Client already registered
            if client_ap:

                # Client has moved 
                if client_ap.name != client['ap-name']:
                    new_ap = self.get_ap_by_name(client['ap-name'])
                    move_client = client_ap.take_client(client['mac'])
                    new_ap.add_client(move_client)
                    if self.output:
                        print(f'[{client["mac"]}] moved from {client_ap.name} to {client["ap-name"]}')

            # Client is new
            else:

                # Add client
                self.add_client(Client(
                    client["mac"],
                    client["user"],
                    client["ap-name"]
                ))

                if not init and self.output:
                    print(f'[{client["mac"]}] has joined {client["ap-name"]}')

        # Check for deletes
        for ap in self.accessPoints:

            for client in ap.clients:
                found = False
                for new_client in clients:
                    if new_client['mac'] == client.mac:
                        found = True
                        break

                if not found:
                    # delete
                    del_client = ap.take_client(client.mac)
                    if self.output:
                        print(f'[{del_client.mac}] has disconnected from {del_client.get_location()}')


class AccessPoint:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, client):
        client.move(self.name)
        self.clients.append(client)

    def take_client(self, client_mac):
        client = None
        for c in self.clients:
            if c.mac == client_mac:
                client = c
                break
        
        if client:
            self.clients.remove(client)
        
        return client
