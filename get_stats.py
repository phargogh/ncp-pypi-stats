import json
import os
import urllib2
import time
import datetime

from bs4 import BeautifulSoup

def get_count(string):
    word_list = string.split(' ')
    return int(word_list[0])

def get_stats(project):
    url = 'https://pypi.python.org/pypi/%s' % project

    html_doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'lxml')
    stats = soup.find('ul', class_='nodot').find_all('li')

    stats_dict = {
        'project': project
    }
    for stat in stats:
        stat_text = stat.text

        if stat_text.startswith('Downloads'):
            # This is the title.  No stats.
            continue
        elif 'day' in stat_text:
            stats_dict['day'] = get_count(stat_text)
        elif 'week' in stat_text:
            stats_dict['week'] = get_count(stat_text)
        elif 'month' in stat_text:
            stats_dict['month'] = get_count(stat_text)
        else:
            raise Exception(stat)

    return stats_dict

def timestamped_payload(project):
    timestamp = time.time()
    data = {
        'timestamp': timestamp,
        'date': datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        'data': get_stats(project),
    }

    with open('logfile-%s.txt' % project, 'a') as logfile:
        logfile.write(json.dumps(data) + '\n')

if __name__ == '__main__':
    projects = [
        'pygeoprocessing',
        'natcap.versioner',
        'natcap.rios'
    ]
    for project in projects:
        timestamped_payload(project)
