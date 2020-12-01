"""Contains the tests for haystack"""
import unittest
from unittest import mock  # pylint: disable=unused-import
from haystack import *


# To run the unit test_files, issue the following command: `python test.py`
# For information on python unit testing, see: https://docs.python.org/3/library/unittest.html
# To check for code coverage:
#   `pip install coverage`
#   `coverage run -m unittest discover`
#   `coverage report`


class HaystackTests(unittest.TestCase):
    def test_find_urls(self):
        urls_file = open("test_files/test_urls.txt", "r")
        urls = find_urls(urls_file.read())

        correct_output = [
            "https://www.google.ca/",
            "https://github.com/Seneca-CDOT/topics-in-open-source-2020/wiki/lab-8",
            "https://docs.python.org/3/library/unittest.html",
        ]

        urls_file.close()

        self.assertEqual(urls, correct_output)

    def test_ignore_urls(self):
        urls_file = open("test_files/test_urls.txt", "r")
        urls_to_ignore_file = open("test_files/test_urls_to_ignore.txt", "r")

        search = find_urls(urls_file.read())
        ignore = find_urls(urls_to_ignore_file.read())

        urls = ignore_urls(search, ignore)

        urls_file.close()
        urls_to_ignore_file.close()

        correct_output = ["https://www.google.ca/"]

        self.assertEqual(urls, correct_output)

    def test_check_url_valid(self):

        urls_file = open("test_files/test_urls.txt", "r")
        search = find_urls(urls_file.read())

        for url in search:
            status_code = self.mock_website_response(url=url, expected_code=200)
            self.assertEqual(200, status_code)

    def test_check_url_invalid(self):
        urls_file = open("test_files/test_urls_invalid.txt", "r")
        search = find_urls(urls_file.read())

        for url in search:
            status_code = self.mock_website_response(url=url, expected_code=404)
            if status_code:
                self.assertEqual(404, status_code)

    def test_check_url_unknown(self):
        urls_file = open("test_files/test_urls_invalid.txt", "r")
        search = find_urls(urls_file.read())

        for url in search:
            status_code = self.mock_website_response(url=url, expected_code=707)
            if status_code:
                self.assertEqual(707, status_code)

    def test_main_with_valid_files(self):
        exit_code = main("test_files/test_urls.txt", "test_files/test_urls_invalid.txt")
        self.assertEqual(0, exit_code)

    def test_main_with_invalid_files(self):
        exit_code = main("asdf/tfffs.txt", "asggdff/fdsa.txt")
        self.assertEqual(1, exit_code)

    @unittest.mock.patch("haystack.requests")
    def mock_website_response(self, mock_request=None, url="", expected_code=None):
        mock_request.head(url).status_code = expected_code
        status = check_url(url)

        return status


if __name__ == "__main__":
    unittest.main()
