#! /usr/bin/python3
import argparse
import time
import os
import sys
from subprocess import call

parser = argparse.ArgumentParser(description='Handle reporting ssh remote forwarding dynamic ports for field boxes.')

parser.add_argument('hostname', type=str, help='Hostname of field box')

parser.add_argument('action', choices=["set-port", "sleep", "allowed-command"], help='Action to be taken')

parser.add_argument('--port', type=int, help='Port number on cloud machine that is ssh remote forwarded to a field box with the given hostname.')
#parser.add_argument('sleep', action='store_true', help='')
parser.add_argument('--command', nargs=argparse.REMAINDER, help='Runs a command if it is in the cloud/allowed-commands.conf whitelist')

args = parser.parse_args()

if args.action == "set-port":
    if args.port is None:
        print("Must use --port option to set port.")
        exit(1)

    port = str(args.port)
    print("Setting port " + port + " for hostname " + args.hostname)
    ports_dir = "/tmp/remote_connect_ports"
    if not os.path.exists(ports_dir):
        os.mkdir(ports_dir)
    temp_port_filename = '/tmp/remote_connect_ports/.' + args.hostname + str(time.perf_counter())
    f = open(temp_port_filename, 'w')
    f.write(port)
    f.flush()
    os.fsync(f.fileno())
    f.close()

    proper_port_filename = '/tmp/remote_connect_ports/' + args.hostname
    os.rename(temp_port_filename, proper_port_filename)

# Sleeps indefinitely, used to keep ssh connections open.
if args.action == "sleep":
    print("Sleeping")
    while True:
        time.sleep(60)

if args.action == "allowed-command":
    if args.command is None:
        print("Use --command option to define command to run.")
        exit(1)
    command_to_check = args.command[0]
    allowed_commands = open(os.path.join(sys.path[0], "allowed-commands.conf"), "r").read().splitlines()
    for allowed_command in allowed_commands:
        if command_to_check == allowed_command:
            print("Command: " + command_to_check + " found in cloud/allowed-commands.conf. Calling it with added arguments..")
            call(args.command)
            exit(0)
    print("Command: " + command_to_check + " not in cloud/allowed-commands.conf")
    exit(1)
