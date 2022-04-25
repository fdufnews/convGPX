Procedure for generating a GPX file that can be downloaded into a GARMIN Edge 800 GPS
=========================

The procedure described here uses [Viking](https://sourceforge.net/projects/viking/) to draw the track but any other application that export GPX tracks can also be used. In that case start at step 7.  
In order for the file to be correctly used by the GPS one must create a track (trk and trkpt in the GPX file) not a route (rte and rtept in the GPX file). Both work but the route one will not contain time an height information.  
The utility works in both cases adding the time information to the points. Even if the time informations are not used (or misused, I don't know why) in the case of a route they are necessary otherwise the file is rejected by the GPS.  

1. In Viking, Right click in left panel  
*Master Layer --> New Layer --> TrackWaypoint Layer*  
2. Right click on TrackWaypoint  
*New --> New Track*  
3. Give the track a name. This will be the name used in the GPS
4. Draw the track
5. To add height informations. Right click on the track in the left panel  
*Transform --> Apply DEM data --> Overwrite*
6. Right click on the track in the left panel  
*Export the track as GPX*
7. In a terminal window  
`$ ./convGPX filename.gpx newfFilename.gpx --speed=6`  
--speed (optionnal), default value is 5 km/h  
This utility adds time information to the GPX file in order for the file to be interpreted by the GPS.
8. Connect the GPS to the computer.
9. Open the GARMIN drive
10. Copy the file into the Garmin/NewFiles/ directory
11. The next time the GPS will be powered on, the file will be interpreted and copied into the Garmin/Courses directory and deleted from the NewFiles one.
