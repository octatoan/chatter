#!/usr/bin/env python

from __future__ import absolute_import

import argparse
import getpass
import os.path
import json
import sys
import pickle
import logging
from colorlog import ColoredFormatter

class Chatbot:

    def main(self):
        self.config_file_name = "chatbot.config"
        self.log_file_name = "chatbot.log"
        self.setup_logging()
        self.get_args()
    
    def get_args(self):
        data = {"room": False, "site": False, "email": False}
        
        parser = argparse.ArgumentParser(description="Troll the (M)S(E|O) chatrooms.")
        parser.add_argument("--site", "-s")
        parser.add_argument("--room", "-r", type=int)
        parser.add_argument("--email", "-e")
        
        parse_cmdline_args = False
        
        #Try to unpickle the config file (if it's there!)
        try:
            file_data = pickle.load(open(self.config_file_name, "rb"))
            data.update(file_data)
            if not data["email"] or not data["room"] or not data["site"]:
                self.logger.warn("Not all data was found, searching command-line args.")
                parse_cmdline_args = True
            else:
                self.logger.info("Valid config file found; data unpickled.")
                
        except FileNotFoundError:
            self.logger.warn("The config file does not exist.")
            parse_cmdline_args = True
            
        except PickleError:
            self.logger.warn("Error while unpickling data.")
            parse_cmdline_args = True
        
        if parse_cmdline_args:
            self.logger.debug("Trying to parse command-line arguments.")
        
            cmd_data = vars(parser.parse_args())
            
            if not data["email"]: #It's not there
                data["email"] = cmd_data["email"]
            if not data["room"]:
                data["room"] = cmd_data["room"]
            if not data["site"]:
                data["site"] = cmd_data["site"]
            if not data["email"] or not data["room"] or not data["site"]:
                self.logger.critical("Not all required data found, exiting.")
                sys.exit(1)
                
            with open(self.config_file_name, "wb") as f:
                pickle.dump(data, f)
                self.logger.info("Data pickled and stored in config file.")
                
        self.logger.debug("Data: " + str(data))
        return data

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = ColoredFormatter(
                    " {log_color}{levelname:>4}{reset} {message}",
                    datefmt=None,
                    reset=True,
                    style='{',
                    log_colors = {
                        'DEBUG':    'nbB',
                        'INFO':     'ngB',
                        'WARNING':  'nyB',
                        'ERROR':    'nrB',
                        'CRITICAL': 'bwR',
                        }
                    )
        
        self.fh = logging.FileHandler(self.log_file_name)
        self.ch = logging.StreamHandler()
        
        self.fh.setLevel(logging.DEBUG)
        self.ch.setLevel(logging.DEBUG)         
        
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
                
        self.logger.info("Logging set up successfully.")
        
        
class ConfigError(Exception):
    def __init__(self, message, errors=[], logger=None):
        Exception.__init__(self, message)
        if logger is not None:
            logger.critical(message)
        self.errors = errors
        
        

if __name__ == '__main__':
    bot = Chatbot()
    bot.main()
