# ev3dev_pymotor
Simple way to control motors of NXT Ev3 using ev3dev via python

## Example

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
