PyProgress
==========
CLI script progress output library

See code for documentation

Run the library standalone to see the different options in action
```shell
python -m pyprogress
```

ProgressBar
----------

Both non-threaded and threaded versions let you call an increment function and output a progress bar of your program.

Options let you show running time, estimated completion time and counts.

#### Example
```
ProgressBar 0:12:34.123456 300.000 [###########################             ] 130/200
Name        Runtime        ETC      Progress                            Completed/Total
```

DoubleProgressBar
-----------------

Similar to the ProgressBar except it has a second sub progress bar for long running scripts with sub tasks

#### Example
```
DoublePB 0:00:07.763144 46.846 [########                                ] 2/10 [######              ] 3/10  total:14 2.000/s
Name     Runtime        ETC      Main Progress                    Completed/Total   Sub progress   Completed/Total Overall count
```

Counter
-------

Simply counts up values!

Spinner
-------

The simplest of the lot, display a waiting spinner

Quick Start
-----------
```python
from pyprogress import *
# create the standard progress bar
pb = ProgressBar(10, name="ProgressBar", timecount=False, completionprediction=True, colored=True)
pb.begin()  # output the "ProgressBar" name 

for x in range(10):  # start your loop of work
    # do some work
    pb.inc()  # increment the bar when you have completed a unit of work

pb.end()  # output the final bar and jump to a new line to keep the output clean
```

Options
-------

#### Progress Bar (inc threaded)

| Option | Type | Desccription | Default |
| ------ | ---- | ------------ | ------- |
| total | int | The total items to complete, the number we are progressing to | |
| width | int | How wide to display the progress bar | 40 |
| showcounter | bool | Show the completed/total counter | True |
| progresschar | str | The character to use in the progress bar | # |
| timecount | bool | Show the runtime counter | False |
| completionprediction | bool | Show the predicted time to completion | False |
| colored | bool | Color the "items per second" count to show increase or decrease | False |

#### Double Progress Bar (inc threaded) 

Same as Progress Bar but adds a second total `total2` as a required parameter


