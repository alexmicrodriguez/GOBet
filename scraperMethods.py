__author__ = 'Alex'
from lxml import html
import requests
import os
import re


def update_team_list():
    total_teams = get_num_teams()
    num_pages = get_num_pages(total_teams)
    team_list = get_team_list(num_pages)
    team_txt = open('team_list.txt', 'w')
    for item in team_list:
        if isinstance(item, unicode):
            virgin_item = item.decode('windows-1252')
            encoded_item = virgin_item.encode('utf-8')
            
            team_txt.write("%s\n" % encoded_item)
        else:
            team_txt.write("%s\n" % item)
    team_txt.close()


def create_directories():
    path = "C:/GOBet/data"
    if not os.path.exists(path):
        os.makedirs(path)
    path = "C:/GOBet/data/general"
    if not os.path.exists(path):
        os.makedirs(path)


def get_num_teams():
    page = requests.get('http://www.gosugamers.net/counterstrike/rankings#team')
    page_info = html.fromstring(page.text)
    list_findings = page_info.xpath('//div[@class="viewing"]/text()')
    showing_sentence = list_findings[0]
    sentence_nums = re.findall(r'\d+', showing_sentence)
    total_teams = sentence_nums[len(sentence_nums) - 1]
    total_teams = int(total_teams)
    return total_teams


def get_num_pages(total_teams):
    if total_teams % 50 != 0:
        num_pages = total_teams / 50 + 1
    else:
        num_pages = total_teams / 50
    return num_pages


def get_team_list(num_pages):
    os.chdir('C:/GOBet/data/general')
    for counter in range(num_pages+1):
        if counter == 0:
            page = requests.get('http://www.gosugamers.net/counterstrike/rankings#team')
            page_info = html.fromstring(page.text)
            merged_team_list = page_info.xpath('//span[@class="main no-game"]/span/text()')
            counter += 1
        else:
            page = requests.get('http://www.gosugamers.net/counterstrike/rankings?page='+str(counter)+'#team')
            page_info = html.fromstring(page.text)
            merged_team_list = merged_team_list + page_info.xpath('//span[@class="main no-game"]/span/text()')
            print(merged_team_list)
    return merged_team_list