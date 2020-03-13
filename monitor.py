#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib
import sys
import argparse
from bs4 import BeautifulSoup
from baseMonitor import BaseMonitor
import requests

class Monitor(BaseMonitor):
    extensions = ["sql", "pdf", "xls",
                  "xlsx", "doc"]

    search_rule = "site:%(site)s (%(filetype)s)" 
    site = "" 
    debug = False
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

    def __init__(self, site=None, debug=False):
        site = urllib.parse.urlparse(site) 
        self.site = site.path
        self.debug = debug
        self.print_debug("WARNING: debug is ON")
    
    def mount_search(self):
        search_fmt = self.search_rule % {
            "site": self.site,
            "filetype": " OR ".join(["filetype:%s" % x for x in self.extensions])
        }
        return "https://google.com/search?q=%s" % \
                 urllib.parse.quote_plus(search_fmt)

    def perform_search(self):
        url = self.mount_search()
        response = requests.get(url, {"User-Agent": self.ua})
        soup = BeautifulSoup(response.text, "lxml")
        print(soup.find_all("div.kCrYT"))
        for g in soup.find_all(class_='g'):
            print(g)
            print('-----')

    def run(self):
        self.perform_search()

if __name__ == '__main__':
    parser = argparse.\
              ArgumentParser(\
                description='Check google search result by extension')
    parser.add_argument('-s',
                        '--site',
                        type=str,
                        nargs=1,
                        required=True,
                        help="Website URL (without schema)")
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help="Enable debug")
    args = parser.parse_args()
    mon = Monitor(site=args.site[0], debug=args.debug)
    mon.run()
