from settings import *

# Format: [left|right] [command (i.e run_forever, change_rps(0.5)...]
def translate(raw_str):
    _str = raw_str.split()
    
    if 'run_forever' in _str[1]:
        motors[_str[0]].run_forever()
        
    elif 'stop' in _str[1]:
        motors[_str[0]].stop()
        
    elif 'set_rps' in _str[1]:
        args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
        motors[_str[0]].set_rps(float(args))
    
    elif 'change_rps' in _str[1]:
        args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
        motors[_str[0]].change_rps(float(args))        
