from settings import *

# Format: [left|right] [command (i.e run_forever, change_rps(0.5)...]
def translate(raw_str):
    _str = raw_str.split()

    # If not specify which motor
    # automatically assumes all motors
    # in list
    if len(_str) <= 1:
        if 'run_forever' in _str[0]:
    	    try:
                for motor in motors:
                    motors[motor].run_forever()
            except:
                pass

        elif 'stop' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].stop()
            except:
                pass

        elif 'toggle' in _str[0]:
            try:
                for motor in motors:
                    motors[motor].toggle()
            except:
                pass

        elif 'set_rps' in _str[0]:
            try:
                args = _str[0][_str[0].find('(')+1:_str[0].find(')')]
                for motor in motors:
                    motors[motor].set_rps(float(args))
            except:
                pass

        elif 'change_rps' in _str[0]:
            try:
                args = _str[0][_str[0].find('(')+1:_str[0].find(')')]
                for motor in motors:
                    motors[motor].change_rps(float(args))
            except:
                pass

    elif len(_str) > 1:

        if 'run_forever' in _str[1]:
            try:
                motors[_str[0]].run_forever()
            except:
                pass

        elif 'stop' in _str[1]:
            try:
                motors[_str[0]].stop()
            except:
                pass

        elif 'toggle' in _str[1]:
            try:
                motors[_str[0]].toggle()
            except:
                pass

        elif 'set_rps' in _str[1]:
            try:
                args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
                motors[_str[0]].set_rps(float(args))
            except:
                pass

        elif 'change_rps' in _str[1]:
            try:
                args = _str[1][_str[1].find('(')+1:_str[1].find(')')]
                motors[_str[0]].change_rps(float(args))
            except:
                pass
