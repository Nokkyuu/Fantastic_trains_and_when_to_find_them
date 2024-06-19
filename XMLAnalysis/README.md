# Analysing the XML output from the Timetable API
These files were used to analyse the huge output that comes from the timetable API, to break it down into what information is actually needed and sort it accordingly. <br>
After analyzing and testing, the following entries were deemed to be necessary and sufficient.
<br>


## From Timetable planned Output:

From main element ``s``:<br>
``id`` (unique identifier)<br><br>
and from subelements ``ar``(arrival) and ``dp`` (departure) <br>
``pt`` (planned time)<br>
``l`` (name of train)<br>
``ppth`` (path information of the train)

## From Timetable changed Output:

From main element ``s``:<br>
``id`` (unique identifier)<br>
``eva`` (EVA-Nr of train station)<br><br>
and from subelements ``ar``(arrival) and ``dp`` (departure) <br>
``ct`` (changed time)<br>
``l`` (name of train)<br>

## Processing the Data:
The whole process of creating the dataframes from the XML output and calculating the delay can be seen in [train_delay_fromXML.ipynb](XMLAnalysis/train_delay_fromXML.ipynb) 