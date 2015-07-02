# ev3dev_pymotor
Simple way of controlling motors of NXT Ev3 using ev3dev via python wirelessly

Made for the Jessie release of ev3dev (20 May 2015)

**By default the script checks for motors plugged into ports A and B**

#Usage
## Testing motor on ev3dev
**Make sure one motor is plugged into port A**

```python
import time
from ev3dev_pymotor import *
motor = ev3dev_pymotor('outA') # Or outB, outC, outD ...

# Rotations per second
motor.set_rps(0.5)
motor.run_forever()
time.sleep(5)
motor.stop()
```

### Establishing TCP communication between desired device and ev3

Step 1.
Execute setup_server.py on the ev3

```python
python setup_server.py
```

Step 2.
Execute setup_client.py [ip address] on desired device to communicate with ev3

```python
python setup_client.py xxx.xxx.x.xx # where xxx.xxx.x.xx is the ip address of the ev3
```

Step 3.
Run the list of commands on the desired device:
```python
format: [left|right|None] command_to_execute

# Examples
run_forever # (runs all specified motors forever)
stop # (stops all specified motors)
left run_forever # (runs the left motor forever)
right change_rps(1.0) # (changes the right motor's rotation per second to '1' and runs it)
left change_rps(0.5) # (changes the left motor's rotation per second to '0.5' and runs it)
```

# List of available commands
```python
/quit # terminates connection on both end

run_forever # Runs motor forever
stop # stops motor
change_rps(x) # Changes motor rotation per second to 'x' AND runs it
set_rps(x) # Sets motor rotation per second to 'x' but DOESN'T run it
toggle # Toggles motors direction
```
