from zonedirector import ZoneDirector
from datetime import datetime
from time import sleep

class NetworkController:
    def __init__(self):
        self.accessPoints = []

    def _get_ap_by_name(self, name):
        for ap in self.accessPoints:
            if ap.name == name:
                return ap

    def add_client(self, mac, location):
        ap = self._get_ap_by_name(location)
        if ap:
            ap.add_client(mac)
        else:
            new_ap = AccessPoint(location)
            new_ap.add_client(mac)
            self.accessPoints.append(new_ap)

    def client_disconnect(self, client_mac, ap_name):
        ap = self._get_ap_by_name(ap_name)
        if ap:
            ap.remove_client(client_mac)

    def client_roam_out(self, client_mac, ap_from, ap_to):
        pass

    def get_stats(self):
        responce = []
        for ap in self.accessPoints:
            json = {
                'ap-name': ap.name,
                'clients connected': len(ap.clients)
            }
            responce.append(json)
        return responce


class AccessPoint:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, client_mac):
        self.clients.append(client_mac)

    def remove_client(self, client_mac):
        self.clients.remove(client_mac)

class Main:

    def __init__(self):
        self.zd = ZoneDirector('monitor', 'monitor')
        self.nw = NetworkController()

        clients = self.zd.get_clients()
        self.lastScan = datetime.now()

        for client in clients:
            self.nw.add_client(client['mac'], client['location'])

        while True:
            self.update()
            sleep(1)

    def update(self):
        events = self.zd.get_events()
        for e in events:
            if float(e['time']) >= self.lastScan.timestamp():
                print(e)
                '''if e['msg'] == "MSG_client_leave":
                    self.nw.client_disconnect('mac', 'ap-desc')
                    print(f"[{e['mac']}] left {e['ap-desc']}")

                elif e['msg'] == "MSG_client_roam_in" or e['msg'] == "MSG_client_join_with_vlan" or e['msg'] == "MSG_client_rejoin_with_vlan":   
                    self.nw.add_client(e['mac'], e['ap-desc'])
                    print(f"[{e['mac']}] joined {e['ap-desc']}")'''

        self.lastScan = datetime.now()



if __name__ == "__main__":
    Main()
