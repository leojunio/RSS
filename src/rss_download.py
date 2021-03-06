import feedparser
import time
import data.mongo_setup as mongo_setup
import logging

from services.data_services import add_item, find_item
from data.urls import rss_list
from colorama import Fore

logging.basicConfig(filename='rss.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def busca_rss():
    for rss_list_item in rss_list:
        feed = feedparser.parse(rss_list_item['url'])
        for feed_entry in feed.entries:
            try:
                if find_item(feed_entry, rss_list_item):
                    print(Fore.YELLOW + f" >>> {feed_entry.title}")
                else:
                    rss_item = add_item(feed_entry, rss_list_item)
                    print(Fore.GREEN + f" +++ {rss_item.title} adicionado com o id {rss_item.id}")
            except Exception as e:
                logging.error(f"{e} - {rss_list_item['publisher']} --- {feed_entry.title} -> URL: {rss_list_item['url']}")
                print(e)


def main():
    mongo_setup.global_init()
    while True:
        busca_rss()
        time.sleep(30)


if __name__ == '__main__':
    main()
