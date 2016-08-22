#! /usr/bin/python3
import argparse
import time
import os
import sys
from subprocess import Popen, call, PIPE
import re
import ipaddress

parser = argparse.ArgumentParser(description='Establish and try to maitain a remote host tunnel to calling machine')

parser.add_argument('cloud_username', type=str, help='Username to SSH into for cloud box')

parser.add_argument('cloud_ip', type=ipaddress.ip_address, help='IP address of cloud box')

args = parser.parse_args()

os.environ["AUTOSSH_GATETIME"] = "0"
os.environ["AUTOSSH_POLL"] = "60" # poll for a connection every 60 seconds

while True: # in case autossh returns
    autossh_cmd = ["autossh", args.cloud_username + "@" + str(args.cloud_ip), "-R", "0:localhost:22", "sleep"]
    autossh_process = Popen(autossh_cmd, stderr=PIPE, universal_newlines=True)

    for line in autossh_process.stderr:
        print(line)
        match = re.search("Allocated port ([0-9]*)", line)
        if match:
            port = match.group(1)
            set_port_cmd = ['autossh', args.cloud_username + '@' + str(args.cloud_ip), 'set-port --port '+ port]
            call(set_port_cmd) # autossh so automatically retries on poor connection


    autossh_process.wait()
