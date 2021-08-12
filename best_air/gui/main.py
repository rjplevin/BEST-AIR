#!/usr/bin/env python
import argparse
from best_air.gui.app import main

def parse_args():
    parser = argparse.ArgumentParser(description='''Run BEST-AIR web application locally''')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='''Enable debug mode in the dash server''')

    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='''Set the host address to serve the application on. Default is localhost (127.0.0.1).''')

    parser.add_argument('-P', '--port', default=8050, type=int,
                        help='''Set the port to serve the application on. Default is 8050.''')

    args = parser.parse_args()
    return args

args = parse_args()
main(args)

