# 3D Audio For Museum Exhibits
3D audio is being utilized within museums and cultural spaces to deliver aural guides and a heightened level of immersion for museum goers, aesthetes, and the general population that visit the enhanced exhibits. Numerous implementations of this technology exist internationally; however, one instance of a model at the University of Florida is constantly being maintained, upgraded, and tested in order to produce a unique museum experience. The current implementation of this system has future goals, challenges, and plans to resolve any potential issues regarding the 3D audio system’s development.

The current implementation of the application allows a user to interactively choose one of three Panamanian food-related sounds (cooking rice, searing steak, and frying plantains) by toggling the desired radio button. Once the desired sound has been chosen, the user can then click on the Play button to hear the 3D audio playback of that sound. The image on the left-hand side of the GUI simply shows the sound sources relative to the user's orientation. The user can listen to all three sounds sequentially, but not at the same time. Since this is a real-time application, when the user clicks on the 'X' in the top right-hand corner, a dialog box will first pop up to ensure the user actually wishes to quit.

## Getting Started
These instructions will guide you in obtaining an up-and-running copy of the project on your local machine for development and testing purposes.
### Prerequisites
3D Audio for Museum Exhibits is being developed with [Python 3.6.4](https://docs.python.org/3/) which can be downloaded by heading to the [Python Software Foundation](https://www.python.org/psf/) and downloading the appropriate package for your local machine.

*Note: If given the option during the installation process, be sure to add the install directory in the PATH environment variable on your local machine. This allows you to run the Python interpreter in any development working directory.*

Next, you will need [PIP](https://pypi.python.org/pypi/pip) (Python Package Index), but luckily PIP comes packaged in all binary installers starting with Python 3.4.

*Note: For ease of use, it is recommended that you also add the directory path that PIP lies in to the PATH environment variable on your local machine for ease of access.*

In order to suitably experience the application, assure that the local machine that the application is running on includes a headphone jack for in-ear listening. Headphones or earphones are required to properly register the 3D audio.
### Installing
Navigate to the directory that holds pip.exe (or if the directory path is included in your local machine's PATH environment variable, navigate anywhere) and install the following required modules:

`$ pip install PyQt5 scipy numpy sounddevice soundfile`
## Deploying
Once all necessary dependencies have been installed, navigate to the root working directory and run:

`$ python gui.py`

The GUI for the application should then immediately pop up, allowing the user to interact with it. To understand the functionality of the program, refer to the second introductory paragraph above.
## Built With
Although any text editor can be used to code Python scripts, [Atom](https://atom.io/) was used as the primary text editor of choice.
## Bugs
As of right now, there aren't any known or documented bugs within the program. The application should function properly on every major platform.
## Repository
The code for 3D Audio for Museum Exhibits can be found in a [GitHub repository](https://github.com/shandysulen/3D-Audio-For-Museum-Exhibits).
## Authors
* [Shandy Sulen](https://github.com/shandysulen)
* [Vasu Jain](https://github.com/vasujain00)
* [Erin Fierce](https://github.com/erinfierce)
* [Paul-Wilson Chang Fatt](https://github.com/kimloy)
## Acknowledgements
Special thanks to Dr. McMullen and Yunhao Wan.
