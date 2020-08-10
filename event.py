import enum
from time import sleep
import config
from zonedirector import ZoneDirector
from database import Database
from datetime import datetime

class Action(enum.Enum):
   CONNECT = 1
   DISCONNECT = 2
   MOVE = 3

class Change:
    def __init__(self, user_mac, action, ap_source, ap_new=None):
        self.user_mac = user_mac
        self.action = action
        self.ap_source = ap_source
        self.ap_new = ap_new

class EventMonitor:
    def __init__(self):
        self.last_clients = None
        self.zd = ZoneDirector(config.server_address, config.username, config.password)
        self.db = Database()

        while True:
            self.update()
            sleep(2)

    def get_changes(self, old_clients, new_clients):
        changes = []

        for old_client in old_clients:
            
            # set if client hasn't disconnected
            matched_client = None

            for new_client in new_clients:
                if old_client['mac'] == new_client['mac']:
                    matched_client = new_client
                    break
            
            # client still connected
            if matched_client:
                # client has moved
                if matched_client['ap-name'] != old_client['ap-name']:
                    changes.append(Change(
                        old_client['mac'],
                        Action.MOVE,
                        old_client['ap-name'],
                        matched_client['ap-name']
                    ))

            # client has disconnected
            else:
                changes.append(Change(
                    old_client['mac'],
                    Action.DISCONNECT,
                    old_client['ap-name'],
                ))

        # check for new clients
        for new_client in new_clients:
            isNewClient = True

            for old_client in old_clients:
                if old_client['mac'] == new_client['mac']:
                    isNewClient = False
                    break

            if isNewClient:
                self.db.add_client(new_client['mac'], new_client['user'])
                changes.append(Change(
                    new_client['mac'],
                    Action.CONNECT,
                    new_client['ap-name'],
                ))
        
        return changes


    def update(self):
        new_clients = self.zd.get_clients()

        # first update
        if self.last_clients == None:
            for client in new_clients:
                self.db.add_client(client['mac'], client['user'])
            self.last_clients = new_clients
            return

        # later updates
        changes = self.get_changes(self.last_clients, new_clients)
        for change in changes:
            client_id = self.db.get_client_id(change.user_mac)
            self.db.add_activity(client_id, datetime.now(), str(change.action), change.ap_source, change.ap_new)
            print(f"[{change.user_mac}] has {change.action} to the network")


EventMonitor()
