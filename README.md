PyProgress
==========
CLI script progress output library

See code for documentation

Run the library standalone to see the different options in action
``` 
python -m pyprogress
```

ProgressBar
----------

Both non-threaded and threaded versions let you call an increment function and output a progress bar of your program.

Options let you show running time, estimated completion time and counts.

#### Example
```
ProgressBar 0:12:34.123456 300.000 [###########################             ] 130/200
Name        Runtime        ETC      Progress                                  Completed/Total
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
