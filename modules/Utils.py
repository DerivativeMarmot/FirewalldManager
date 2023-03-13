import json
import re

class Utils:

    def dump2File(self, filepath, ports_detail) -> None:
        print('Adding details to file')
        with open(filepath, 'w') as f:
            json.dump(ports_detail, f)
    
    def getAllPorts(self, ports_detail:dict) -> list:
        ports = []
        for key in ports_detail:
            ports += ports_detail[key]
        return ports
    
    def validatePorts(self, ports_detail:dict, ports:str, option:str) -> list:
        print('---Validating ports---')
        pattern = re.compile('\d+/(?:tcp|udp)') # '?:' non-capturing group
        validPorts = []
        allActivePorts = self.getAllPorts(ports_detail)
        for port in set(pattern.findall(ports)):
            if int(port.split('/')[0]) in range(1, 65535):
                match(option):
                    case 'add':
                        if port not in allActivePorts:
                            validPorts.append(port)
                        else:
                            print(port, 'exists')
                    case 'remove':
                        if port in allActivePorts:
                            validPorts.append(port)
                        else:
                            print(port, 'does not exist')
            else:
                print(port, 'is invalid')
        
        print('---Valid ports---')
        for port in validPorts:
            print(port, end=' ')
        print('\n---')
        
        return validPorts
    
    def listAllPorts(self, ports_detail):
        promptCat = '1. With categories\n2. Without categories\n> '
        if input(promptCat)[0] == '1':
            for cat in ports_detail:
                print(cat, end=': ')
                for port in ports_detail[cat]:
                    print(port, end=' ')
                print()
        else:
            ports = self.getAllPorts()
            ports.sort(key = lambda x : int(x.split('/')[0]))
            for port in ports:
                print(port, end=' ')
            print()