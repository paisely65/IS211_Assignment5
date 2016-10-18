#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module describes Algorithms and Data Structures 2/2."""

import urllib2
import argparse
import csv

class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0
        self.time = 0
        self.requestsProcessed = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None
        self.time += 1

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        if not self.busy():
            self.current_task = new_task
            self.time_remaining = new_task.get_pages()
            self.requestsProcessed += 1
            while self.time_remaining > 0:
                self.tick()

class Request:
    def __init__(self, req):
        self.timestamp = int(req[0])
        self.processTime = int(req[2])
        self.requestName = req[1]

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
        self.items.append(item)

    def dequeue(self):
        if len(self.items) > 0:
            item = self.items[0]
            self.items = self.items[1:]
            return item
        return None

    def size(self):
        return len(self.items)


def simulateOneServer(filename):
    server = Server()
    queue  = Queue()
    wait_time = 0

    for request in filename:
        request = Request(request)
        queue.enqueue(request)

    numRequests = len(queue.items)

    while not queue.is_empty():
        request = queue.dequeue()
        while request.timestamp > server.time:
            server.tick()
        server.start_next(request)
        wait_time += request.wait_time(server.time)

    average = (wait_time+0.0)/(server.requestsProcessed+0.0) 
    print("The average waiting time is %2.2f secs for %3d requests."%(average,server.requestsProcessed))


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
