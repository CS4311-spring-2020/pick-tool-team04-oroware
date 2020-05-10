# Installation Instructions
To install this system, you will need to do the following:

1. Download this project from the repository on a machine that runs Kali Linux (2017.1) or Windows 10
2. If you do not already have Python 3.6 installed, install Pytohn 3.6
3. Use pip to install the following libraries: pytesseract version 0.3.3, pymongo version 3.9.0, speech_recognition version 3.8.1, splunklib version 1.0.0, networkx version 2.4.0, PyQt version 5.11.3

Once you have completed these steps the system will be installed on your machine. It is important to note that you must be running both a Splunk and MongoDb instance to run this system.

# Use Instructions
Most of the features of this system are relatively easy to use, and thus in this section we will only review features that are not trivial to use. Those features which are not easy to use are as follows:

1. Editing log entries: To edit log entries in the log entry configuration tab, simply double click on the log entry you would like to edit in the table. Once you have made the necessary modifications, click save changes.
2. Editing significant events: To edit significant events in the edit vector configuration tab, simply double click on the significant event you would like to edit in the table. Once you have made the necessary modifications, click save changes.
3. Editing relationships: To edit relationships in the edit vector configuration tab, simply double click on the relationship you would like to edit in the table. Once you have made the necessary modifications, click save changes.
4. Moving nodes on the graph: To move nodes on the graph, clik and hold on the node you would like to move and move the mouse to the node's new location. Release the mouse.
5. Correlationg nodes into relationships: To correlate nodes in a relationship on the graph, click and hold on a source node and move the mouse to the destination node's location. Release the mouse.
