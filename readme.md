convGPX.py
==========

#What it is
This is a small Python application that adds time information to a GPX file in order for it to be accepted by a GARMIN Edge 800 GPS.  
With the time informations missing the GPX files are rejected by the Edge 800.  
The time informations are computed based on the distance between 2 consecutive points. The height is currently not taken in to account so this is just a rough estimate. However, speed information can be added to the command line to make the time information more representative.  

#Dependencies
The application uses:
- [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) to manipulate de GPX data
- [argparse](https://docs.python.org/3/library/argparse.html) to parse the argument given in the command line

#Usage
```bash
>$ ./convGPX.py -h
usage: convGPX.py [-h] [--speed SPEED] inputfile outputfile  

Convert a GPX file without time information to a GPX understandable by Garmin GPS  

positional arguments:  
  inputfile      name of the input file  
  outputfile     name of the output file  

optional arguments:  
  -h, --help     show this help message and exit  
  --speed SPEED  Speed in km/h (default: 5.0)  
```
During the operation, the application displays for each point
- a number (starting from 0)
- the distance to the previous point
- the time to travel from the previous point
- the cumulated distance from point 0
- the time value that will be inserted in the GPX file (the application gives point 0 the current time)

