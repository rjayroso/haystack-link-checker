## Getting Started 
Below are instructions for getting Haystack running on your machine. Let's find those needles!
### Prerequisites
You will need [Git](https://git-scm.com/) and [Python 3](https://www.python.org/downloads/) to pull from this repository and run Haystack.
### Installation Using Git
First, fork this repo and copy the clone URL.
- For example, `https://github.com/YOUR_USERNAME/haystack-link-checker.git`  

Next, go to the folder or workspace that you want to clone the repository into:
```bash
cd C:\myprojects
```
Where **myprojects** is where you want to place the repository.
Next, issue the following commands:
```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/haystack-link-checker.git

# Go into the repository
cd haystack-link-checker
```
### Installing Dependencies
 Be sure to upgrade to the latest version of Python because pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4.
```bash
# While still inside your C:\myprojects\haystack-link-checker folder
# Install dependencies using pip 
pip install termcolor
pip install requests
pip install black
pip install pylint
pip install coverage
```
### Committing Changes
Before committing any changes, be sure to format the main `haystack.py` file via Python [Black](https://pypi.org/project/black/) and run [PyLint](https://pylint.pycqa.org/en/latest/user_guide/run.html) like so:
```bash
black haystack.py
pylint haystack.py
```
Be sure to fix any warnings before committing!
To see how Black formats the code, see the [styling documentation](https://github.com/psf/black/blob/master/docs/the_black_code_style.md).
### Unit Testing
Haystack uses the [unittest](https://docs.python.org/3/library/unittest.html) unit testing framework.  
To run the tests, run `python test.py` (unit tests should be run before committing any changes).  
To run code coverage, run `coverage run -m unittest discover` and then run `coverage report` to report on the results.
### Setting up Your Visual Studio Code
To automatically use Black with your VS Code, follow the instructions below:
1. Go to the settins by pressing `Ctrl+` or by pressing the gear icon in the bottom right of your VS Code.
2. Type **"format on save"** at the top search bar and check the box.
3. Search for "**python formatting provider**" and select "black" in the drop down menu (NOTE: you must have Black installed already).
To automatically use PyLint with your VS Code, follow the second set of instructions below:
1. Open VS Code's command pallete by pressing `Ctrl+Shift+P`.
2. Type "**Python: Select Linter**" and choose PyLint (NOTE: you must have PyLint installed already).



