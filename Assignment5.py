#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module describes Algorithms and Data Structures 2/2."""

import urllib2
import argparse
import csv

class Server:
    def __init__(self, secsPross):
        self.page_rate = secsPross
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate


class Request:
    def __init__(self, time, processTime):
        self.timestamp = time
        self.processTime = processTime

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.processTime

    def wait_time(self, current_time):
        return current_time - self.timestamp


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self,item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def simulateOneServer(filename):
    server = Server()
    queue  = Queue()
    wait_time = []
    request_dict = {}

    for request in filename:
        n_time = int(request[0])
        queue.enqueue(request)

        if n_time in request_dict:
            request_dict[n_time].append(request)
        else:
            request_dict[n_time] = [request]

    for time_in_second in request_dict:
        for req in request_dict[time_in_second]:
            Request(req)
            queue.dequeue()

        if (not server.busy()) and (not queue.isEmpty()):
            nextreq = Request(queue.dequeue())
            wait_time.append(nextreq.wait_Time(nextreq))
            server.startNext(nextreq)

        server.tick()

    average = sum(wait_time)/len(wait_time) * 0.001
    print("The average Waiting time is %2.2f secs for %3d requests."%(average,queue.size()))


def main():
    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--file", help=' Please enter a url of csv file', type=str)
    args = url_parser.parse_args()

    if args.file:
        try:
            filename = csv.reader(urllib2.urlopen(args.file))
            simulateOneServer(filename)

        except:
            print "url may not be valid."
    else:
        print "Please enter a valid url csv file --file. "


if __name__ == "__main__":
    main()
