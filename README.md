DotaInstaller
=============

DotaInstaller is a pytho (2.7.9) applciation that takes custom files and automatically imports them into a users dota 2 folder.


Install
============

Py2exe is used to create an executable for windows machines, to do this run setup.py it will create an executable called installer.py. If you are not on a windows machine or would simply like to run the python script, then run installer.py.

Setup
============

DotaInstaller's custom files are located in the sound folder. Some sound files require additional scripts to accompy them, and these are located in the scripts folder.

In order for DotaInstaller to pick up custom files, settings.txt must be filled in wiht your custom sounds. The format of the file is as follows:
  
    First Column: Name to display to user
    Second Column: Destination of file
    Third Column: Local location of file
    Fourth Column: scripts or sound, representing if ithe file is in the scripts or sound folder
    Repeat column 2-4 as many times as needed for each relevant sound/script file.
    

