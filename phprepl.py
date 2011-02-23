#!/usr/bin/env python

"""
         _          _       _    _          _           _            _          _     
        /\ \       / /\    / /\ /\ \       /\ \        /\ \         /\ \       _\ \   
       /  \ \     / / /   / / //  \ \     /  \ \      /  \ \       /  \ \     /\__ \  
      / /\ \ \   / /_/   / / // /\ \ \   / /\ \ \    / /\ \ \     / /\ \ \   / /_ \_\ 
     / / /\ \_\ / /\ \__/ / // / /\ \_\ / / /\ \_\  / / /\ \_\   / / /\ \_\ / / /\/_/ 
    / / /_/ / // /\ \___\/ // / /_/ / // / /_/ / / / /_/_ \/_/  / / /_/ / // / /      
   / / /__\/ // / /\/___/ // / /__\/ // / /__\/ / / /____/\    / / /__\/ // / /       
  / / /_____// / /   / / // / /_____// / /_____/ / /\____\/   / / /_____// / / ____   
 / / /      / / /   / / // / /      / / /\ \ \  / / /______  / / /      / /_/_/ ___/\ 
/ / /      / / /   / / // / /      / / /  \ \ \/ / /_______\/ / /      /_______/\__\/ 
\/_/       \/_/    \/_/ \/_/       \/_/    \_\/\/__________/\/_/       \_______\/     

Simplistic PHP repl.                                                                                
"""

from __future__ import print_function

import readline
import rlcompleter
import threading
import sys
import tempfile
import subprocess
import os
import re
import atexit
import logging
import funs

historyPath = os.path.expanduser("~/.phpreplhist")

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)
del atexit

class SimpleCompleter(object):
    """ http://www.doughellmann.com/PyMOTW/readline/index.html """
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

readline.set_completer(SimpleCompleter(funs.FUNS).complete)
readline.parse_and_bind('set show-all-if-ambiguous on')
readline.parse_and_bind("tab: complete")
# Shipped python on OS X?
# readline.parse_and_bind ("bind ^I rl_complete")



class Colors(object):
    """ http://stackoverflow.com/q/287871/89391 
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def runphp(filename):
    print("{0}==> Running {1} {2}".format(Colors.HEADER, filename, Colors.OKGREEN))
    
    p = subprocess.Popen("php {0}".format(filename), 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        print('{0}{1}{2}'.format(Colors.FAIL, stderr.strip(), Colors.ENDC))
        return False
    else:
        print(stdout.strip(), Colors.ENDC)
        return True

class Repl(object):

    def __init__(self, prompt='php [{0}] >> '):
        self.snippet = ''
        self.counter = 0
        self.prompt = prompt
        self.loop()
    
    def execute_snippet(self, cli):
        self.snippet += '\n{0}'.format(cli)

        runnable = '<?php\n {0} ?>'.format(self.snippet.strip())
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(runnable)
        f.close()
        success = runphp(f.name)
        if not success:
            self.snippet = '\n'.join(self.snippet.split('\n')[:-1])
        return success
        
    def save_snippet(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(self.snippet)
        f.close()
        print('==> Saved snippet to {0}'.format(f.name))

    def loop(self):
        while True:
            try:
                cli = raw_input(self.prompt.format(self.counter))
                if cli.startswith('.h'):
                    print(__doc__)
                    print(".    show current snippet")
                    print(".c   clear last line")
                    print(".ca  clear all")
                    print(".r   run current snippet")
                    print(".s   save snippet to a temporary file")
                    print()
                    print("Note: - Failed lines won't be saved in the snippet")
                    print("      - Use <tab> to autocomplete function names")
                    
                elif cli == '.':
                    print(self.snippet)
                elif cli.startswith('.ca'):
                    print('{0}==> Cleared snippet {1}'.format(Colors.HEADER, Colors.ENDC))
                    self.snippet = ''
                elif cli == '.c':
                    print('{0}==> Cleared last line {1}'.format(Colors.HEADER, Colors.ENDC))
                    self.snippet = '\n'.join(self.snippet.split('\n')[:-1])
                elif cli.startswith('.r'):
                    self.execute_snippet(cli)
                elif cli.startswith('.s'):
                    self.save_snippet()
                else:
                    self.execute_snippet(cli)
                    
                self.counter += 1
            except EOFError, eofe:
                print()
                sys.exit(0)

if __name__ == '__main__':
    threading.Thread(target=Repl).start()
