# ---- HAYSTACK ----
# Author: Royce Ayroso-Ong
# Version: 0.3
# Licence: MIT Licence
# Description: Haystack checks through a file for broken links


import argparse                         # parsing command line arguments 
import sys                              # command line arguments
import requests                         # url validating
import codecs                           # file handling
import re                               # regex for urls
from termcolor import colored           # colored terminal text
from multiprocessing.dummy import Pool  # support for parallelization


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
        request = requests.head(url, timeout=3)
        status = request.status_code

    except KeyboardInterrupt:  # must include to be able to stop the program while it is running
        sys.exit()

    except:
        print(colored("Unknown link: {}".format(url), 'yellow'))
        unknown_urls_count += 1

    else:
        if status in range(200,299):
            print(colored("Valid link ({}): {}".format(status, url), 'green'))
            valid_urls_count += 1

        elif status in range(400,599):
            print(colored("Bad link ({}): {}".format(status, url), 'red'))
            bad_urls_count += 1

        elif status in range(300,399):
            print(colored("Redirected link ({}): {}".format(status, url), 'green'))

        else:
            print(colored("Unknown link: {}".format(url), 'yellow'))
            unknown_urls_count += 1


def version():
    print("Haystack Version 0.3")


def main(file):
    try:  # read from file
        file = codecs.open(file, 'r', 'utf-8')
    except OSError as err:  # error opening file
        print("Error opening file: {0}".format(err))
    else:  # success opening file
        urls = find_urls(file.read())
        pool = Pool(10)              # Using 5 Thread pool
        pool.map(check_url, urls)    # Return an iterator that applies function to every item of iterable, yielding the results
        pool.close()
        pool.join()

        # Using '+' operator to connect with each sentence to print
        print("Haystack has finished processing the file.\n" + colored("# of VALID links: {} | ".format(valid_urls_count), 'green') + colored("# of UNKNOWN links: {} | ".format(unknown_urls_count), 'yellow') + colored("# of BAD links: {}".format(bad_urls_count), 'red'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="These are common Haystack commands used in various situations:",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-v', '--version', help="display installed version", action="store_true")
    parser.add_argument('-f', '--file',  help="search through a file for broken links", dest="file")
    args = parser.parse_args()

    if args.version:
        version()

    elif args.file:
        main(args.file)

    else:
        parser.print_help(sys.stderr)
        sys.exit(1)
        