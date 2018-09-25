import argparse
import re
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

# Input arguments to the program, default values are set as given in the problem statement of task1
parser = argparse.ArgumentParser (description='Provide the input parameters for the webcrawler')
parser.add_argument ("--max_depth", default=2, help='Maximum depth allowed for crawling')
parser.add_argument ("--unique_url_count", default=100, help="Maximum number of unique URLS in a crawl")
parser.add_argument ("--seed1", default="https://en.wikipedia.org/wiki/Time_zone",
                     help="the first seed URL to start crawling")
parser.add_argument ("--seed2", default="https://en.wikipedia.org/wiki/Electric_car",
                     help="the second seed URL to start crawling")
parser.add_argument ("--seed3", default="https://en.wikipedia.org/wiki/Carbon_footprint",
                     help="the third seed URL to start crawling")
parser.add_argument ("--out_filename", default="crawledList", help="the filename to store the unique URL's crawled")
args = parser.parse_args ()

# Global Variables:

# variable to store the index of the files starting from 1 till 1000(at most)
FILE_INDEX = 1
# dictionary to store the file name and the corresponding URL
LINK_FILENAME_MAP = {}
# dictionary to store each unique URL crawled and their depth relative to the seed
URL_DEPTH_MAP_SEED_1 = {}
URL_DEPTH_MAP_SEED_2 = {}
URL_DEPTH_MAP_SEED_3 = {}


# function which crawls the web following BFS
def webspider (seed):
    # Assigning map based on the seed
    if seed == args.seed1:
        map = URL_DEPTH_MAP_SEED_1
    if seed == args.seed2:
        map = URL_DEPTH_MAP_SEED_2
    if seed == args.seed3:
        map = URL_DEPTH_MAP_SEED_3

    links_to_crawl = [seed]
    links_crawled = []
    links_at_nextdepth = []
    current_depth = 1
    while links_to_crawl and len (links_crawled) < args.unique_url_count and current_depth <= args.max_depth:
        current_crawl = links_to_crawl.pop (0)
        if current_crawl not in links_crawled:
            new_fetched_urls = get_all_urls (current_crawl)
            if new_fetched_urls is not None:
                update_to_crawl_list (links_at_nextdepth, new_fetched_urls)
                links_crawled.append (current_crawl)
                # respect politeness policy of the website
                time.sleep (1);
        if current_crawl not in map:
            map.update ({current_crawl: current_depth})
        # if all links at current depth is exhausted go to the next level
        if not links_to_crawl:
            links_to_crawl = links_at_nextdepth
            links_at_nextdepth = []
            current_depth = current_depth + 1
    return links_crawled


# helper function to keep the list updated for the crawler to crawl at the next depth
def update_to_crawl_list (links_at_nextdepth, new_fetched_urls):
    for url in new_fetched_urls:
        if url not in links_at_nextdepth:
            links_at_nextdepth.append (url)


# helper function which support the webspider to retrieve urls based on the crawling policy
def get_all_urls (current_crawl):
    valid_url_list = []
    pattern = re.compile ('^/wiki/')
    base_url = "https://en.wikipedia.org/wiki"
    response = urllib.request.urlopen (current_crawl)
    html_content = BeautifulSoup (response, "html.parser")
    html_content.prettify ()
    # Get the links that obey the pattern
    body = html_content.find ('div', {'id': 'bodyContent'})
    links = body.find_all ('a', href=pattern)
    for link in links:
        if ":" not in link.get ('href'):
            url = urllib.parse.urljoin (base_url, link.get ('href'))
            if "#" in link.get ('href'):
                url = url[: url.index ('#')]
            if url not in valid_url_list:
                valid_url_list.append (url)
    return valid_url_list


# function which generates the file with the final list of unique urls
def crawled_url_list (links_crawled, outfh):
    for link in links_crawled:
        outfh.write (link)
        outfh.write ("\n")


def intermediate_merge (URL_DEPTH_MAP_SEED_1, URL_DEPTH_MAP_SEED_2):
    temp_url_map = {}
    for url, depth in URL_DEPTH_MAP_SEED_1.items ():
        for link, drop in URL_DEPTH_MAP_SEED_2.items ():
            if link == url:
                if drop < depth:
                    temp_url_map.update ({link: drop})
                else:
                    temp_url_map.update ({url: depth})
            else:
                if link not in temp_url_map:
                    temp_url_map.update ({link: drop})
        if url not in temp_url_map:
            temp_url_map.update ({url: depth})

    return temp_url_map


def merge_into_unique_url (URL_DEPTH_MAP_SEED_1, URL_DEPTH_MAP_SEED_2, URL_DEPTH_MAP_SEED_3):
    merged_list = {}
    half_merged = intermediate_merge (URL_DEPTH_MAP_SEED_1, URL_DEPTH_MAP_SEED_2)

    print('Printing the processed URL map from the first merge')
    print(half_merged)

    for url, depth in half_merged.items():
        for link, drop in URL_DEPTH_MAP_SEED_3.items():
            if link == url:
                if drop < depth:
                    merged_list.update({link: drop})
                else:
                    merged_list.update({url: depth})
            else:
                if link not in merged_list:
                    merged_list.update({link: drop})
        if url not in merged_list:
            merged_list.update({url: depth})

    return merged_list


def main ():
    webspider(args.seed1)
    webspider(args.seed2)
    webspider(args.seed3)
    merge_list = merge_into_unique_url(URL_DEPTH_MAP_SEED_1, URL_DEPTH_MAP_SEED_2, URL_DEPTH_MAP_SEED_3)

    print ("Start printing the urls with their depth" + "\n")
    print (len(URL_DEPTH_MAP_SEED_1))
    print ('*******************************' + '\n')
    print (len(URL_DEPTH_MAP_SEED_2))
    print ('*******************************' + '\n')
    print (len(URL_DEPTH_MAP_SEED_3))
    print ('Printing the merged list based on condition check')
    print (merge_list)
    print (len (merge_list))
    print ("Finished priniting")

if __name__ == main ():
    main ()