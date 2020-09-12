# WG Gesucht Updater
This application is designed to update all active offers on www.wg-gesucht.de/ .

## Function
The application is ready to use on windows as executable .exe file. It is recommended to use the update.sh script. 
The parameters for the .exe file needs to be given correctly.  
``build/exe.win32-3.8/main.exe --mail <your.mail@adresse.com> --pw <your_pw>``  
or shorter  
``build/exe.win32-3.8/main.exe -m <your.mail@adresse.com> -pw <your_pw>``  
A description of the parameters with:  
``build/exe.win32-3.8/main.exe --help``  

If you use Linux or Mac you may need to create a new executable with the commands below. cx_freeze executables
 only work on the os they are created.

For faster use, create a shortlink to the update.sh on your desktop, so one click will be enough to update all offers.
After the script finished a bash shell stays open for 30 seconds and shows the output of the script.

## Development
The application is a python script using selenium to automate a headless firefox browser.
### Requirements
Developed and tested with Python 3.8.5 
It is recommended to create a virtual environment with  
- `` python -m venv wg_gesucht``  

Install requirements with 
- ``pip install -r requirements.txt``

### Executable
To give the user a faster handling an executable gets created out of the python file. The advantage is that the user needs no 
virtual environment running while executing the script. The executable gets created with the shell command (venv has to active !):
- ``python setup.py build``


### Hints
- The script isn't very efficient and takes it time. A faster version as web crawler could probably be realized 
with the requests and the beatifulsoup librarys.
- The script is just tested manually on Windows 10.
- The exit() command in the script is displayed as error in the script inside the bash, when executed as .exe and not .py
