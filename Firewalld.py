import json
import os
from modules.Manager import Manager
from modules.Utils import Utils

class Firewalld():
    def __init__(self) -> None:
        self.file_location = '{home_dir}/.config/firewalld/'.format(home_dir=os.path.expanduser('~'))
        self.filename = 'ports.json'
        self.filepath = self.file_location + self.filename
        
        if not os.path.exists(self.file_location):
            print('Generating new config file')
            os.makedirs(self.file_location)
            open(self.filepath, 'x') # create config file
            self.ports_detail = {}
        else:
            print('Loading config file')
            with open(self.filepath, 'r') as f:
                self.ports_detail:dict = json.load(f)

    def menu(self):
        print("""
        1. add ports
        2. remove ports
        3. generate config file
        4. apply config file
        9. show all opening ports
       10. save changes
       11. restart firewalld, save changes and exit
       12. exit without saving changes
        """)
        match input('> '):
            case '1':
                self.ports_detail = Manager(self.filepath, self.ports_detail).addPorts()
                print(self.ports_detail)
            case '2':
                self.ports_detail = Manager(self.filepath, self.ports_detail).removePorts()
            case '3':
                self.ports_detail = Manager(self.filepath, self.ports_detail).generateConfig()
            case '4':
                Manager(self.filepath, self.ports_detail).applyConfig()
            case '9':
                Utils(self.filepath, self.ports_detail).listAllPorts()
            case '10':
                Utils(self.filepath, self.ports_detail).dump2File()
            case '11':
                print('Restarting firewalld')
                # os.system('sudo systemctl restart firewalld')
                Utils(self.filepath, self.ports_detail).dump2File()
                exit()
            case '12':
                exit()
            case _:
                pass