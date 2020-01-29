# DSS Project VU

Welcome to the README file for the Decision Support System. Here, all documentation on how to get the System working on your personal computer. 

Firstly, it will be explained what is actually contained inside the project folder. 
Secondly, Instructions are given on getting the DSS running. 
Lastly, Some additional instructions are given about the DSS.


## Project Files

Within the project directory are 2 folders, which are thoroughly explained below.


### Models

The model directory contains all the files that are not used directly within the GUI.
This includes files like the logistic model, convolutional neural network and the transfer learning algorithm. 
Even though these files are not directly used, they are of major importance to the DSS. 
If the user wants to know more about the implemented models, one should look in this directory. 


### GUI

The GUI directory will contain all files that are used directly by the CSS. The folder is divided into two different parts.
The main part of the folder consists of all python files, which includes the main file "app.py". This file is important later on so keep this in mind.
The other python files form a direct connection to the "app.py" file.  These files are divided up to make it easier navigating through the approximately 1300 lines of code. 

The folder assets is also of major importance to the DSS. The main purpose of this folder is to style the GUI with the use of pictures and a CSS file. 
The extra directory inside of the assets folder is the " images" folder. This is also used later on, as it is the standard directory for showing all of the plots and displays within the DSS.
This folder is created by taking various images from the original data set, which means that the GUI predicts on the training data. 
It is encouraged that the user therefore makes use of the file upload function within the DSS in order to truly make use of the system. 


## Installation Guide

Before running any of the files, make sure that the terminal is working in the ANACONDA environment. 
This environment is necessary to import most of the packages that will be used by the DSS. 
To get this environment working, please refer to: https://docs.conda.io/

To start the server and install everything else that is required, there are two options:

### PyCharm Editor

-In PyCharm, create a new project
-Choose as working directory the DSS folder.
-Run appCharm.py
-It should now import all packages and update existing ones to ensure the server works. 

### Command Line / Terminal
- Open Command Line for Windows and Terminal for both Apple and Linux operating systems.
- Go to the directory where the project folder is located using cd
- (Another option: open terminal within the folder itself, so that you do not have to use the cd command)
- When in the correct folder run the following code: python ./appTerminal.py (or in windows: python app.py)
- When running this code, it should install/update all packages and start the program

Once the server is running and no errors have occured (warnings are fine), do the following:
- Open a browser of your choice
- Fill in the following IP-address: http://127.0.0.1:8050

The loading of the server may take a while, it is normal as it needs to process 70 MB of pictures.
After a while, the DSS is loaded and ready for action. 


##Extra information

### Text File Images

Every time a new file is uploaded or the server starts anew, a text file will be generated, where all information is gathered on the prediction of bacterial spots for these images. This includes image names. 
