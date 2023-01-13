from modules.Utils import Utils
import os
import subprocess

class Manager():
    def __init__(self, filepath:str, ports_detail:dict) -> None:
        self.filepath = filepath
        self.ports_detail = ports_detail

    def managePorts(self, operation:str, ports:list):
        cmd = 'sudo firewall-cmd --zone=public --permanent --{operation}-port={port}'
        for port in ports:
            print(cmd.format(operation=operation, port=port))
            # os.system(cmd.format(operation=operation, port=port))
        print()

    def addPorts(self) -> dict:
        prompt = 'Enter the port(s) you want to open(separate using space)\nExample ports: 666/udp 9443/tcp\n> '

        # valid ports
        ports = Utils(self.filepath, self.ports_detail).validatePorts(input(prompt), 'add')
        print()
        if len(ports) == 0:
            print('No ports added, requests canceled')
            return self.ports_detail
        
        # confirm
        if (input('Confirm the ports(y/n)')[0] == 'y'):
            print('ports confirmed')
            self.managePorts('add', ports)
        else:
            print('No ports added, requests canceled')
            return self.ports_detail
        
        # add ports to json
        print('Existing categories: ', end='')
        for key in self.ports_detail:
            print(key, end=' ')
        print()
        cat = input('Input a new/existing category: ')
        if cat in self.ports_detail:
            s_ports:list = self.ports_detail[cat]
            for port in ports:
                s_ports.append(port)
        else:
            self.ports_detail[cat] = ports
        # Utils(self.filepath, self.ports_detail).dump2File()

        print('Done')
        return self.ports_detail
    
    def removePorts(self):
        prompt = 'Enter the port(s) you want to remove(separate using space)\nExample ports: 666/udp 9443/tcp\n> '

        # valid ports
        ports = Utils(self.filepath, self.ports_detail).validatePorts(input(prompt), 'remove')
        print()
        if len(ports) == 0:
            print('No ports removed, requests canceled')
            return self.ports_detail
        
        empty_cat = []
        for port in ports:
            for cat in self.ports_detail:
                if port in self.ports_detail[cat]:
                    self.ports_detail[cat].remove(port)
                    if len(self.ports_detail[cat]) == 0:
                        empty_cat.append(cat)
        
        # clean empty category
        for cat in empty_cat:
            self.ports_detail.pop(cat, None)

        print(self.ports_detail)
        return self.ports_detail
    
    def generateConfig(self):
        command = 'sudo firewalld-cmd --list-ports'
        ports:set = set(subprocess.run(command.split(' '), stdout=subprocess.PIPE).stdout.decode('utf-8').split(' '))
        print('All opening ports\n', ports)
        print('Add category to each of the ports')
        new_ports_details = {}
        while True:
            cat = input('new category: ')
            selected_ports = set(input('ports belongs to this category(separate using space)\nExample ports: 666/udp 9443/tcp: '))
            valid_ports:set = ports.intersection(selected_ports)
            new_ports_details[cat] = list(valid_ports)
            print('Adding', valid_ports, 'to category', cat)
            ports.difference_update(valid_ports)
            print('Remaining ports: ', ports)

            if len(ports) == 0:
                print('all ports are categorized, exit')
                Utils(self.filepath, new_ports_details).dump2File()
                break
            
            if input('Continue?(y/n): ') != 'y':
                Utils(self.filepath, new_ports_details).dump2File()
                break
        return new_ports_details
    
    def applyConfig(self):
        ports = []
        for cat in self.ports_detail:
            ports += Utils(self.filepath, self.ports_detail).validatePorts(' '.join(self.ports_detail[cat]), 'add')
        for port in ports:
            self.managePorts('add', port)