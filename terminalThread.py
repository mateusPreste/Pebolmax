import threading
import os

class terminalThread(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
    
    def interpreter(self, line):
        command = os.system(f'cmd /c "{line}"')
        return command    
    
    def insert(self, command):
        cmd = command
            
        print(cmd)

        if os.name == 'nt':
            self.interpreter(cmd.replace("\'", "\"").replace('&', '^&'))
        else:
            os.system(cmd)
    
    def run(self):
        self.insert(self.cmd)
