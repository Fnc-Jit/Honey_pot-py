# Liabary

import argparse
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
            honey_pot(args.address, args.username, args.password, args.port)

        if not args.username:
            username= None
        if not args.password:
            password = None    
        
        elif args.http:
            print("[-] Starting HTTP honeypot...")

            if not args.username:
                username= 'admin'
            if not args.password:
                password = 'password'

            print(f'Port: {args.port}, Username: {username}, Password: {password}')
            run_web_honey_pot(args.port,args.username, args.password)

        else:
            print("Please specify either --ssh or --http to start the respective honeypot.")

    
    except:
        print("[-] Exiting honeypot...")



