import json
import os
from modules.Manager import Manager
from modules.Utils import Utils

class Firewalld():
    def __init__(self) -> None:
        self.file_location = '{home_dir}/.config/firewalld/'.format(home_dir=os.path.expanduser('~'))
        self.filename = 'ports.json'
        self.filepath = self.file_location + self.filename
        self.ports_detail = {}
        
        if not os.path.exists(self.file_location):
            print('Creating config path')
            os.makedirs(self.file_location)
        else:
            if not os.path.exists(self.filepath):
                print('Creating config file')
                with open(self.filepath, 'w') as f: 
                    f.write('{ }')
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
                self.ports_detail = Manager().addPorts(self.ports_detail)
            case '2':
                self.ports_detail = Manager().removePorts(self.ports_detail)
            case '3':
                self.ports_detail = Manager().generateConfig(self.filepath)
            case '4':
                Manager().applyConfig(self.ports_detail)
            case '9':
                Utils().listAllPorts(self.ports_detail)
            case '10':
                Utils().dump2File(self.filepath, self.ports_detail)
            case '11':
                print('Restarting firewalld')
                os.system('sudo systemctl restart firewalld')
                Utils().dump2File(self.filepath, self.ports_detail)
                exit()
            case '12':
                exit()
            case _:
                pass