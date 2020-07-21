import requests
import urllib3
from datetime import datetime

class ZoneDirector:

    def __init__(self, username, password):
        # session to keep login cookies
        self.session = requests.session()

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
        r = self.session.post("https://zonedirector/admin10/login.jsp", data=post_data, verify=False)
        return "<title>Dashboard" in r.text

    def get_clients(self):
        ''' Get Clients on the network '''
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded charset=UTF-8'
        }
        data = '''<ajax-request action='getstat' updater='stamgr.1595202440778.7319' comp='stamgr'><client LEVEL='1'/><pieceStat start='0' number='100000' pid='1' requestId='stamgr.1595202440778.7319'/></ajax-request>'''
        r = self.session.post("https://zonedirector/admin10/_cmdstat.jsp", data=data, verify=False, headers=headers)
        return self.xml_to_json(r.text, 'client', ['mac', 'location', 'signal-strength', 'rssi'])

    def get_events(self):
        ''' Get Events on the network '''
        events = []

        timestamp = datetime.now().timestamp()

        request_data = [
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='0' number='300' pid='1' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='300' number='300' pid='2' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='600' number='300' pid='3' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='900' number='300' pid='4' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='1200' number='300' pid='5' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='1500' number='300' pid='6' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='1800' number='300' pid='7' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='2100' number='300' pid='8' requestId='eventd.{timestamp}'/></ajax-request>''',
            f'''<ajax-request action='getstat' updater='eventd.{timestamp}' comp='eventd'><xevent sortBy='time' sortDirection='-1' c='user'/><pieceStat start='2400' number='300' pid='9' requestId='eventd.{timestamp}'/></ajax-request>'''
        ]

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded charset=UTF-8'
        }

        for request in request_data:
            r = self.session.post("https://zonedirector/admin10/_cmdstat.jsp", data=request, verify=False, headers=headers)
            events += self.xml_to_json(r.text, 'xevent', ['time', 'msg', 'mac', 'ap-desc', 'apto-desc', 'user'])

        return events

    def xml_to_json(self, raw_data, tag, filtered_tags=None):
        ''' Convert XML responce to filtered JSON '''
        output = raw_data.replace('</apstamgr-stat></response></ajax-response>', '')
        output = output.replace(' />', '')
        objects = output.split(f'<{tag} ')[1:]

        formatted_clients = []

        for thing in objects:
            json_object = {}

            for info in thing.split(' '):
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


if __name__ == '__main__':
    zd = ZoneDirector('monitor', 'monitor')
    print(zd.get_events())