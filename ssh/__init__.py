#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from netmiko import ConnectHandler
from netmiko import SSHDetect

from local_settings import h3c, hill_stone


def ssh_dev_exc(ip, commands, port=22, username='readonly', password='readonly'):

    dev_info = {
        'device_type': 'autodetect',
        'ip': ip,
        'port': port,
        'username': username,
        'password': password
    }

    guesser = SSHDetect(**dev_info)
    best_match = guesser.autodetect()
    print(best_match)  # Name of the best device_type to use further
    print(guesser.potential_matches)  # Dictionary of the whole matching result

    dev_info['device_type'] = best_match

    with ConnectHandler(**dev_info) as dev_connection:
        echos = []
        for c in commands:
            print(c)
            echo = dev_connection.send_command_timing(c)
            print(repr(echo))
            print(dev_connection.find_prompt())
            echos.append(echo)

        return echos


if __name__ == '__main__':
    outputs = ssh_dev_exc(**h3c)
    print(outputs)