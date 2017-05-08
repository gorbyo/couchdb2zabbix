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

''' 
####### FOR FUTURE #######
# def group_by_type(active_tasks):
#     grouped_tasks_list = defaultdict(list)
#
#     for task_type in active_tasks:
#         grouped_tasks_list[task_type['type']].append(task_type)
#
#     grouped_tasks = dict(grouped_tasks_list)
#     return grouped_tasks
#
#
# def count_grouped_tasks(grouped_tasks):
#     count = {}
#     for key, values in grouped_tasks.items():
#         count[key] = len(values)
#     return count
'''


def get_tasks(active_tasks):
    tasks = {'data': []}
    count = len(active_tasks)
    for val in range(0, count):
            pid_norm = str(active_tasks[val]['pid']).translate(None, '<>')
            tasks['data'].append({"{#PID}": pid_norm})
    return tasks


def get_status(active_tasks, pid):
    count = len(active_tasks)
    for val in range(0, count):
        pid_norm = str(active_tasks[val]['pid']).translate(None, '<>')
        type_of_task = str(active_tasks[val]['type'])
        if pid == pid_norm:
            if type_of_task == 'indexer' or type_of_task == 'database_compaction':
                status = str(active_tasks[val]['changes_done'])
            else:
                status = str(active_tasks[val]['progress'])
            return status


def get_type(active_tasks, pid):
    count = len(active_tasks)
    for val in range(0, count):
        pid_norm = str(active_tasks[val]['pid']).translate(None, '<>')
        if pid == pid_norm:
            return str(active_tasks[val]['type'])


def main(url):
    tasks = get_active_tasks(url=url)
    if not (arguments().parse_args().pid is None):
        if (arguments().parse_args().type is None) or (arguments().parse_args().type == 'no'):
            pid = arguments().parse_args().pid
            print get_status(tasks, pid)
        elif arguments().parse_args().type == 'yes':
            pid = arguments().parse_args().pid
            print get_type(tasks, pid)
    else:
        print json.dumps(get_tasks(tasks))


if __name__ == '__main__':
    try:
        viewurl = arguments().parse_args().url
        main(viewurl)
    except:
        arguments().print_usage()
        exit(1)
