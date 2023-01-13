from modules.Utils import Utils
import os
import subprocess

class Manager:

    def managePorts(operation:str, ports:list):
        cmd = 'sudo firewall-cmd --zone=public --permanent --{operation}-port={port}'
        for port in ports:
            print(cmd.format(operation=operation, port=port))
            # os.system(cmd.format(operation=operation, port=port))
        print()

    def addPorts(self, ports_detail) -> dict:
        prompt = 'Enter the port(s) you want to open(separate using space)\nExample ports: 666/udp 9443/tcp\n> '

        # valid ports
        ports = Utils.validatePorts(input(prompt), 'add')
        print()
        if len(ports) == 0:
            print('No ports added, requests canceled')
            return ports_detail
        
        # confirm
        if (input('Confirm the ports(y/n)')[0] == 'y'):
            print('ports confirmed')
            self.managePorts('add', ports)
        else:
            print('No ports added, requests canceled')
            return ports_detail
        
        # add ports to json
        print('Existing categories: ', end='')
        for key in ports_detail:
            print(key, end=' ')
        print()
        cat = input('Input a new/existing category: ')
        if cat in ports_detail:
            s_ports:list = ports_detail[cat]
            for port in ports:
                s_ports.append(port)
        else:
            ports_detail[cat] = ports
        # Utils(.filepath, ports_detail).dump2File()

        print('Done')
        return ports_detail
    
    def removePorts(ports_detail):
        prompt = 'Enter the port(s) you want to remove(separate using space)\nExample ports: 666/udp 9443/tcp\n> '

        # valid ports
        ports = Utils.validatePorts(input(prompt), 'remove')
        print()
        if len(ports) == 0:
            print('No ports removed, requests canceled')
            return ports_detail
        
        empty_cat = []
        for port in ports:
            for cat in ports_detail:
                if port in ports_detail[cat]:
                    ports_detail[cat].remove(port)
                    if len(ports_detail[cat]) == 0:
                        empty_cat.append(cat)
        
        # clean empty category
        for cat in empty_cat:
            ports_detail.pop(cat, None)

        print(ports_detail)
        return ports_detail
    
    def generateConfig(filepath): # need improvement
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
                Utils.dump2File(filepath, new_ports_details)
                break
            
            if input('Continue?(y/n): ') != 'y':
                print('Saving current progress')
                Utils.dump2File(filepath, new_ports_details)
                break
        return new_ports_details
    
    def applyConfig(self, ports_detail):
        ports = []
        for cat in ports_detail:
            ports += Utils.validatePorts(' '.join(ports_detail[cat]), 'add')
        for port in ports:
            self.managePorts('add', port)