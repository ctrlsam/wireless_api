import requests
import urllib3
from datetime import datetime

class ZoneDirector:

    def __init__(self, address, username, password):
        # session to keep login cookies
        self.session = requests.session()
        self.address = address

        # hide SSL warnings
        urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )
        
        # Login
        if not self.login(username, password):
            exit('[!] Login failed')
        print('[+] Logged in')


    def login(self, username, password):
        ''' Login to Zone Director '''
        post_data = {
            'username': username,
            'password': password, 
            'ok': ''
        }
        r = self.session.post(f"https://{self.address}/admin10/login.jsp", data=post_data, verify=False)
        return "<title>Dashboard" in r.text


    def get_clients(self):
        ''' Get Clients on the network '''
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded charset=UTF-8'
        }
        data = '''<ajax-request action='getstat' updater='stamgr.1595202440778.7319' comp='stamgr'><client LEVEL='1'/><pieceStat start='0' number='100000' pid='1' requestId='stamgr.1595202440778.7319'/></ajax-request>'''
        r = self.session.post(f"https://{self.address}/admin10/_cmdstat.jsp", data=data, verify=False, headers=headers)
        return self.xml_to_json(r.text, 'client', ['mac', 'user', 'ap-name', 'signal-strength', 'rssi'])


    def xml_to_json(self, raw_data, tag, filtered_tags=None):
        ''' Convert XML responce to filtered JSON '''
        output = raw_data.replace('</apstamgr-stat></response></ajax-response>', '')
        output = output.replace(' />', '')
        objects = output.split(f'<{tag} ')[1:]

        formatted_clients = []

        for thing in objects:
            json_object = {}

            for info in thing.split('" '):
                info += '"'
                variable = info.split('=')
                key = variable[0]
                try:
                    value = variable[1].strip('"')
                except IndexError:
                    continue
                
                if filtered_tags != None:
                    if key in filtered_tags:
                        json_object[key] = value
                else:
                    json_object[key] = value

            formatted_clients.append(json_object)

        return formatted_clients