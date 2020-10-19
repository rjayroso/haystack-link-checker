# ---- HAYSTACK ----
# Author: Royce Ayroso-Ong
# Version: 0.3
# Licence: MIT Licence
# Description: Haystack checks through a file for broken links

import argparse  # parsing command line arguments
import sys  # command line arguments
import requests  # url validating
import re  # regex for urls
from termcolor import colored  # colored terminal text
from multiprocessing.dummy import Pool  # support for parallelization
from multiprocessing import cpu_count  # get cpu thread count

# count variables to record the amount of valid/bad/unknown links
valid_urls_count = 0
bad_urls_count = 0
unknown_urls_count = 0

# -f FILE, --file FILE additional flag, default is '--all'
flag = '--all'


def find_urls(filename):
    regex = "(?:(?:https?|ftp)://)[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]"
    urls = re.findall(regex, filename)  # uses regex to search for http(s) links in the file
    urls = list(dict.fromkeys(urls))  # removes duplicate links
    return urls


def ignore_urls(searchurls, ignoreurls):
    # finds the common elements between the two lists and gets rid of them
    finalurls = list(set(searchurls) ^ set(ignoreurls))
    return finalurls


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
        if flag == "--all":
            print(colored("Unknown link: {}".format(url), 'yellow'))
            unknown_urls_count += 1

    else:
        if status in range(200, 299) and (flag == "--good" or flag == "--all"):
            print(colored("Valid link ({}): {} ".format(status, url), 'green'))
            valid_urls_count += 1

        elif status in range(400, 599) and (flag == "--bad" or flag == "--all"):
            print(colored("Bad link ({}): {} ".format(status, url), 'red'))
            bad_urls_count += 1

        elif flag == "--all":
            print(colored("Unknown link: {} ".format(url), 'yellow'))
            unknown_urls_count += 1


def main(searchfile, ignorefile):
    try:  # read from file

        with open(searchfile, 'r') as search:
            searchurls = find_urls(search.read())

        # if user is using the ignore options
        if ignorefile:
            with open(ignorefile, 'r') as ignore:
                ignoreurls = find_urls(ignore.read())
                searchurls = ignore_urls(searchurls, ignoreurls)

    except OSError as err:  # error opening file
        print("Error opening file: {0}".format(err))

    else:  # success opening file
        print("Haystack is processing the file")

        pool = Pool(cpu_count())  # Using 5 Thread pool
        pool.map(check_url, searchurls)  # Returns an iterator that applies function to every item of iterable
        pool.close()
        pool.join()

        # Using '+' operator to connect with each sentence to print
        print("Haystack has finished processing the file\n" +
              colored("# of VALID links: {} | ".format(valid_urls_count), 'green') +
              colored("# of UNKNOWN links: {} | ".format(unknown_urls_count), 'yellow') +
              colored("# of BAD links: {}".format(bad_urls_count), 'red'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Haystack",
                                     description='These are common Haystack commands used in various situations:')
    parser.add_argument('-v', '--version', action='version', help='display installed version',
                        version='%(prog)s version 3.0')
    parser.add_argument('-f', '--file', help='search through a file for broken links', dest='searchfile')

    parser.add_argument('-i', '--ignore', help='file that contains urls to ignore', dest='ignorefile')

    # optional flags for file processing, default is --all, only one flag can be present at a time
    flag_group = parser.add_mutually_exclusive_group()
    flag_group.add_argument('--all', help='displays all links', action='store_const', const='--all', default='--all',
                            dest='flag')
    flag_group.add_argument('--good', help='displays good links', action='store_const', const='--good', dest='flag')
    flag_group.add_argument('--bad', help='displays bad links', action='store_const', const='--bad', dest='flag')

    args = parser.parse_args()

    if args.searchfile:
        flag = args.flag
        main(args.searchfile, args.ignorefile)
        if bad_urls_count > 0 or unknown_urls_count > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        parser.print_help(sys.stderr)
        sys.exit(0)
