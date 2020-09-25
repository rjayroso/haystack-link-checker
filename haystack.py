# ---- HAYSTACK ----
# Author: Royce Ayroso-Ong
# Version: 0.1
# Licence: MIT Licence
# Description: Haystack checks through a file for broken links and reports the status code


import sys                      # command line arguments
import requests                 # url validating
import codecs                   # file handling
import re                       # regex for urls
from termcolor import colored   # colored terminal text


# count variables to record the amount of valid/bad/unknown links
valid_urls_count = 0
bad_urls_count = 0
unknown_urls_count = 0


def find_urls(filename):
    regex = "(?:(?:https?|ftp)://)[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]"
    urls = re.findall(regex, filename)  # uses regex to search for http(s) links in the file
    urls = list(dict.fromkeys(urls))  # removes duplicate links
    return urls


def check_url(url):
    global valid_urls_count
    global bad_urls_count
    global unknown_urls_count

    try:  # get status code
        request = requests.get(url, timeout=3)
        status = request.status_code
    except:
        print(colored("Unknown link: {}".format(url), 'grey'))
        unknown_urls_count += 1
    else:
        if status == 200:
            print(colored("Valid link ({}): {}".format(status, url), 'green'))
            valid_urls_count += 1
        elif status == 400 or status == 404:
            print(colored("Bad link ({}): {}".format(status, url), 'red'))
            bad_urls_count += 1
        else:
            print(colored("Unknown link: {}".format(url), 'grey'))
            unknown_urls_count += 1


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':  # -h|--help argument to display help
        print('usage: python haystack.py [-v | --version] [-h | --help] [<filename>]\n\n',
              'These are common Haystack commands used in various situations:\n\n',
              '    {:<30}{}'.format('-v, --version', 'Show current version\n'),
              '    {:<30}{}'.format('-h, --help', 'Show commands and how to use them'))
    elif sys.argv[1] == '-v' or sys.argv[1] == '--version':  # -v|--version argument to display the version
        print("Haystack Version 0.1")
    elif len(sys.argv) == 2:  # file name argument
        try:  # read from file
            file = codecs.open(sys.argv[1], 'r', 'utf-8')
        except OSError as err:  # error opening file
            print("Error opening file: {0}".format(err))
        else:  # success opening file
            urls = find_urls(file.read())
            for url in urls:
                check_url(url)
            print("Haystack has finished processing the file.\n",
                  colored("# of VALID links: {} | ".format(valid_urls_count), 'green'),
                  colored("# of UNKOWN links: {} | ".format(unknown_urls_count), 'grey'),
                  colored("# of BAD links: {}".format(bad_urls_count), 'red'))
    else:  # too many command arguments
        print("Error: too many command arguments")
