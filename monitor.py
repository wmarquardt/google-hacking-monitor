#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib
import sys
import argparse
from bs4 import BeautifulSoup
from baseMonitor import BaseMonitor
import requests
import re

class Monitor(BaseMonitor):
    extensions = ["sql", "pdf", "xls",
                  "xlsx", "doc"]

    search_rule = "site:%(site)s (%(filetype)s)" 
    site = "" 
    debug = False
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

    def __init__(self, site=None, debug=False):
        super(Monitor, self).__init__(debug=debug)
        site = urllib.parse.urlparse(site) 
        self.site = site.path
        self.logger.debug("debug is ON")
    
    def mount_search(self):
        # mount any possibility to get sensible data
        mounted = []
        search_url = "https://google.com/search?q=%s"

        # file extension
        search_fmt = self.search_rule % {
            "site": self.site,
            "filetype": " OR ".join(["filetype:%s" % x for x in self.extensions])
        }

        mounted.append(search_url %
                       urllib.parse.quote_plus(search_fmt))

        # directory listing
        # @TODO
        
        self.logger.warning("Search mounted: %s " % mounted)
        return mounted

    def perform_search(self):
        result = []
        url = self.mount_search()[0]  # just for a while
        self.logger.debug("Search URL: %s" % url)
        response = requests.get(url, {"User-Agent": self.ua})
        soup = BeautifulSoup(response.text, "lxml")
        for g in soup.find_all("div", class_='kCrYT'):
            link = g.find('a',attrs={'href': re.compile("^/url?")})
            name = g.find('div', class_="vvjwJb")
            if not link: continue

            # get content
            link = link.get('href')[7:]
            name = name.getText()

            result.append([name, link])

        self.print_result(result)

    def print_result(self, result):
        # @TODO separate in groups and print
        if not result:
            # This does not mean that your website is secure xD
            print("Any sensitive results found.")
            return

        print("Potential sentitive data were found\n\n")
        for res in result:
            print("%s!%s%s\n%s\n\n" % (
                self.OKCYAN, res[0], self.ENDC, res[1]))

    def run(self):
        self.perform_search()

if __name__ == '__main__':
    parser = argparse.\
        ArgumentParser(description='Check potential dangerous information\
                                    about your site in Google Search page\
                                    like directory listing and indexed files by extension.')
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
