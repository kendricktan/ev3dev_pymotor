# ev3dev_pymotor
Simple way of controlling motors of NXT Ev3 using ev3dev via python wirelessly
Made for the Jessie release of ev3dev (20 May 2015)

## Motors testing example

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
