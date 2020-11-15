# Haystack CLI Link Checker
Do you have valid and broken links that need to be fixed? Haystack will find those needles and report them back to you!
## Features
![Haystack Running](https://github.com/rjayroso/haystack-link-checker/blob/master/resources/haystack-run.gif)
- Version and help section
- Coloured terminal text
- Exception handling for unkown links
- Support for UNIX and Windows style commands
- Support for parallelization, using multiple threads pool
### Running Haystack
```bash
# Once you have successfully installed Python and the dependencies: 
# Type haystack.py to see help section
python haystack.py

# To see the version, use the argument -v or --version
python haystack.py -v

# To run haystack on your own text file
python haystack.py -f <filename>

# To run haystack on your own HTML file
python haystack.py -u <URL>
```
## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/rjayroso/react-vehicle-database-manager/blob/master/LICENSE) file for details.
## Acknowledgments
I would like to thank my colleagues for reviewing my code and issuing suggestions for improvements.
