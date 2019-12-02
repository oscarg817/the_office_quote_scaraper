#!/usr/bin/env python3
# %%
import requests
import re
import uuid
import csv
import sqlite3
from bs4 import BeautifulSoup
from tqdm import tqdm


# %%
base_url = 'http://officequotes.net/'
episode_urls = []
season_regex = "^Season [0-9]+"
table_name = "all_office_quotes"
insert_row_query = f""" insert into {table_name}(quote_uuid, season, episode, episode_title, character, quote) values(?,?,?,?,?,?)"""
create_table_query = f"create table {table_name}(quote_uuid varchar(32) primary key, season varchar(10), episode varchar(10), episode_title varchar(50), character varchar(50), quote text);"
quote_db = sqlite3.connect("the_office_db.db")
cursor = quote_db.cursor()
cursor.execute(create_table_query)
response = requests.get(base_url)
html = BeautifulSoup(response.text, "html.parser")

#get all the episode URLs
for div in html.find_all("div", class_= "navEp"):
    for a  in div.find_all("a", href=True):
        if re.match("^no[0-9]+-[0-9]+\.php$", a["href"]):
            episode_urls.append(f"{base_url}{a['href']}")



for url in episode_urls: 
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")

    for td in html.find_all("td", bgcolor = "#FFF8DC"):
        attr_episode_title = td.find_all("b")[1].text.strip()
        #get season and episode
        for b in td.find_all("b"):
            if re.match(season_regex, b.text):
                attr_season = b.text.split("-")[0].strip().lower().replace(" ", "_")
                attr_episode = b.text.split("-")[1].strip().lower().replace(" ", "_")

        #get quote and character names
        for div in td.find_all("div"):
            for b in tqdm(div.find_all("b")):
                deleted_scene_regex = ".*Deleted.*"
                try:
                    attr_quote = b.next_sibling.strip()
                    attr_character = b.text[:-1].strip()
                except AttributeError:
                    pass
                # exclude deleted scenes 
                if re.match(deleted_scene_regex, b.text):
                    pass
                else:
                    attr_quote_uuid = uuid.uuid4().hex
                    cursor.executemany(insert_row_query, ((attr_quote_uuid,attr_season, attr_episode,attr_episode_title,attr_character,attr_quote),))
                    quote_db.commit()

quote_db.commit()
cursor.close()
