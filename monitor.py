#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib
import sys
import argparse
from bs4 import BeautifulSoup
import requests

class Monitor(object):
    extensions = ["sql", "pdf", "xls",
                  "xlsx", "doc"]

    search_rule = "site:%(site)s (%(filetype)s)" 
    site = "" 
    def __init__(self, site=None):
        if not site: 
            sys.exit(1)

        self.site = site
    
    def mount_search(self):
        search_fmt = self.search_rule % {
            "site": self.site,
            "filetype": " OR ".join(["filetype:%s" % x for x in self.extensions])
        }
        return "https://google.com/search?q=%s" % \
                 urllib.parse.quote_plus(search_fmt)

    def perform_search(self):
        print(self.mount_search())

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
                        help="Website URL")

    args = parser.parse_args()
    mon = Monitor(site=args.site[0])
    mon.run()
