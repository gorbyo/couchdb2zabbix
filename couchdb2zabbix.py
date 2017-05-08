#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import urllib
from collections import defaultdict
import argparse
from argparse import RawTextHelpFormatter

def arguments():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='Checking Progress of Tasks')
    parser.add_argument('--url', default='http://localhost:5984/_active_tasks',
                                 help='Define URL for Active Tasks. Default is: http://localhost:5984/_active_tasks')
    parser.add_argument('--pid', help='Get PID')
    parser.add_argument('--type', help='Get TYPE (\'yes\' or \'no\'). PID required')
    return parser


def get_active_tasks(url):
    try:
        response = urllib.urlopen(url)
    except:
        exit(1)
    active_tasks = json.load(response)
    return active_tasks


def group_by_tasks(active_tasks):
    grouped_tasks_list = defaultdict(list)

    for task_type in active_tasks:
        grouped_tasks_list[task_type['type']].append(task_type)

    grouped_tasks = dict(grouped_tasks_list)
    return grouped_tasks


def count_tasks(grouped_tasks):
    count = {}
    for key, values in grouped_tasks.items():
        count[key] = len(values)
    return count


def get_tasks(grouped_tasks):
    count_dict = count_tasks(grouped_tasks)
    tasks = {'data': []}
    for key in grouped_tasks:
        count = count_dict[key]
        for val in range(0, count):
            pid_norm = str(grouped_tasks[key][val]['pid']).translate(None, '<>')
            tasks['data'].append({"{#PID}": pid_norm})
    print json.dumps(tasks)


def get_status(grouped_tasks, pid):
    count_dict = count_tasks(grouped_tasks)
    for key in grouped_tasks:
        count = count_dict[key]
        for val in range(0, count):
            pid_str = str(grouped_tasks[key][val]['pid'])
            if pid == pid_str.translate(None, '<>'):
                if key == 'indexer' or key == 'database_compaction':
                   status = grouped_tasks[key][val]['changes_done']
                else:
                   status = grouped_tasks[key][val]['progress']
                print status


def get_type(grouped_tasks, pid):
    count_dict = count_tasks(grouped_tasks)
    for key in grouped_tasks:
        count = count_dict[key]
        for val in range(0, count):
            pid_str = str(grouped_tasks[key][val]['pid'])
            if pid == pid_str.translate(None, '<>'):
                print grouped_tasks[key][val]['type']


def main(viewurl):
    tasks_json = get_active_tasks(url=viewurl)
    tasks_dict = group_by_tasks(tasks_json)
    if not (arguments().parse_args().pid is None):
        if (arguments().parse_args().type is None) or (arguments().parse_args().type == 'no'):
            pid = arguments().parse_args().pid
            get_status(tasks_dict, pid)
        elif arguments().parse_args().type == 'yes':
            pid = arguments().parse_args().pid
            get_type(tasks_dict, pid)
    else:
        get_tasks(tasks_dict)


if __name__ == '__main__':
    try:
        viewurl = arguments().parse_args().url
        main(viewurl)
    except:
        arguments().print_usage()
        exit(1)
