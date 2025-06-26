# Liabary

import argparse
import os
import paramiko

# AUTO-GENERATE SSH KEY BEFORE IMPORTING SSH MODULE
if not os.path.exists('server.key'):
    print("Generating server.key...")
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file('server.key')
    print("server.key generated successfully!")

# NOW IMPORT MODULES (after key is created)
from ssh_honey import *
from web_honeypot import *

# parse command line arguments

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a',"--address", type=str, required=True,)
    parser.add_argument('-p',"--port", type=int, required=True)
    parser.add_argument('-u',"--username", type=str)
    parser.add_argument('-pw',"--password", type=str)

    parser.add_argument('-s',"--ssh", action='store_true')
    parser.add_argument('-w',"--http", action='store_true')

    args = parser.parse_args()

    print(f"Parsed arguments: {args}")

    try:
        if args.ssh:
            print("[-] Starting SSH honeypot...")
            
            # Set defaults for SSH if not provided
            username = args.username if args.username else 'root'
            password = args.password if args.password else 'password'
            
            honey_pot(args.address, username, password, args.port)
        
        elif args.http:
            print("[-] Starting HTTP honeypot...")

            # Set defaults for HTTP if not provided
            username = args.username if args.username else 'admin'
            password = args.password if args.password else 'password'

            print(f'Port: {args.port}, Username: {username}, Password: {password}')
            run_web_honey_pot(args.port, username, password)

        else:
            print("Please specify either --ssh or --http to start the respective honeypot.")

    except KeyboardInterrupt:
        print("\n[-] Exiting honeypot...")
    except Exception as e:
        print(f"[-] Error: {e}")
        print("[-] Exiting honeypot...")



