#   Hashcode 2017 qualification round youtube streaming problem solution by Team: Voskoi.
#   This is a better version of our uploaded solution.
#
#   Original score: ~1M
#   Extended round score: 1.77M
#
#   kittens Score:                          495538
#   me_at_the_zoo Score:                    484699
#   trending_today Score:                   335960
#   videos_worth_spreading Score:           462598
#   Total Score:                           1778795
#
#   Team members:
#       Giorgos Stamatakis
#       Christos Spyridakis
#       Tzanis Fotakis
import queue
import sys
from functools import total_ordering

import null


class Cache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.videoIDs = []

    def addVideo(self, videoID, size):
        if videoID not in self.videoIDs:
            self.videoIDs.append(videoID)
            self.capacity -= size


class Endpoint(object):
    def __init__(self, latency, cachesID, cachesLatency):
        self.latency = latency
        self.cachesID = cachesID
        self.cachesLatency = cachesLatency


@total_ordering  # Comparator interface
class Request(object):
    def __init__(self, Rv, Re, Rn, gain=-1):
        self.rv = Rv
        self.re = Re
        self.rn = Rn
        self.gain = gain

    def __lt__(self, other):
        if self.gain < other.gain:
            return 1
        elif self.gain == other.gain:
            return 0
        else:
            return -1


class Data(object):
    def __init__(self, filename, outname):
        self.filename = filename
        self.outname = outname

        self.numVideos = 0
        self.numEndpoints = 0
        self.numRequests = 0
        self.numCaches = 0
        self.capacity = 0

        self.videos = []  # IDs
        self.caches = []
        self.endpoints = []
        self.requests = queue.PriorityQueue()

        self.ratio = 0
        self.notServed = 0

        self.ratio = 0

    def read_file(self):
        with open(self.filename, 'r') as fin:
            line = fin.readline()

            self.numVideos, self.numEndpoints, self.numRequests, self.numCaches, self.capacity = [int(num) for num in line.split()]

            self.ratio = (self.numCaches * self.capacity) / self.numVideos

            ###Caches
            for i in range(0, self.numCaches):
                self.caches.append(Cache(self.capacity))

            ###Videos
            videoSizes = [int(num) for num in fin.readline().split()]
            for i in range(self.numVideos):
                self.videos.append(videoSizes[i])

            ###Endpoints
            for i in range(0, self.numEndpoints):
                lat, caches = [int(num) for num in fin.readline().split()]
                obj = Endpoint(lat, [], [])
                for j in range(0, caches):
                    cacheId, cacheLatency = [int(num) for num in fin.readline().split()]
                    obj.cachesID.append(cacheId)
                    obj.cachesLatency.append(cacheLatency)
                self.endpoints.append(obj)

            ###Requests
            for i in range(0, self.numRequests):
                rv, re, rn = [int(num) for num in fin.readline().split()]
                gain = self.endpoints[re].latency
                for j in range(len(self.endpoints[re].cachesLatency)):
                    itm = self.endpoints[re].cachesLatency[j]
                    if itm < gain:
                        gain = itm
                gain = (self.endpoints[re].latency - gain) * rn
                self.requests.put(Request(rv, re, rn, gain))

    def write_file(self):
        with open(self.outname, 'w') as fout:
            fout.write('%d\n' % self.numCaches)
            for i in range(self.numCaches):
                if self.caches[i].capacity == self.capacity:
                    continue
                fout.write('%d ' % i)
                for j in range(len(self.caches[i].videoIDs)):
                    fout.write('%d ' % self.caches[i].videoIDs[j])
                fout.write('\n')

    def process_request(self, req, deg=-1, cacheResult=-1, turns=1):
        ###Increase the number of rounds for a better score (possibly).
        for _ in range(0, turns):
            cacheResult = -1
            if len(self.endpoints[req.re].cachesID) == 0:
                return

            for i in range(len(self.endpoints[req.re].cachesID)):
                if self.caches[self.endpoints[req.re].cachesID[i]].capacity - self.videos[req.rv] > 0:
                    cacheResult = i
                    break

            if cacheResult == -1:
                self.notServed += 1
                return

            for i in range(cacheResult, len(self.endpoints[req.re].cachesID)):
                if self.caches[self.endpoints[req.re].cachesID[i]].capacity - self.videos[req.rv] > 0:
                    diff = self.endpoints[req.re].cachesID[cacheResult] - self.endpoints[req.re].cachesLatency[i]
                    if diff > 0 and diff > deg:
                        deg = self.endpoints[req.re].cachesID[cacheResult] - self.endpoints[req.re].cachesLatency[i]
                        cacheResult = i
        self.caches[self.endpoints[req.re].cachesID[cacheResult]].addVideo(req.rv, self.videos[req.rv])

    def compute(self):
        rs = []
        while self.requests.qsize() > 0:
            rs.append(self.requests.get())

        counter = self.requests.qsize()
        for j in range(len(rs)):
            if rs[j] == null:
                continue

            if counter < 0:
                break
            else:
                counter -= 1

            if self.videos[rs[j].rv] < self.ratio:
                self.process_request(rs[j])
                rs[j] = null

        for i in range(len(rs)):
            if rs[i] == null:
                continue
            self.process_request(rs[i])
            rs[i] = null


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])

    _data = Data(sys.argv[1], sys.argv[2])

    try:
        _data.read_file()
        _data.compute()
        _data.write_file()
    except KeyboardInterrupt:
        print("Salvage successful!")
        pass
