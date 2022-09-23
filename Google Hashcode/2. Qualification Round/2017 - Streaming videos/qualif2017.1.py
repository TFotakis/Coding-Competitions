import sys


class Video(object):
    def __init__(self, id, size, caches):
        self.id = id
        self.size = size
        self.caches = caches


class Cache(object):
    def __init__(self, capacity, latency, id):
        self.capacity = capacity
        self.latency = latency
        self.id = id
        self.videoIDs = []
        self.flag1 = 0


class Endpoint(object):
    def __init__(self, id, latency, caches):
        self.id = id
        self.latency = latency  ##Datacenter Latency
        self.caches = caches


class Request(object):
    def __init__(self, Rv, Re, Rn):
        self.rv = Rv
        self.re = Re
        self.rn = Rn
        self.timeSaved = 0
        self.cacheServed = -1

    def get_cache_latency(self):
        if self.cacheServed == -1:
            return 0
        else:
            return 1  # TODO return actual Latency


class Data(object):
    def __init__(self, videos, caches, endpoints, requests):
        self.videos = videos
        self.caches = caches
        self.endpoints = endpoints
        self.requests = requests
        self.usedCaches = 0
        self.score = 0
        self.wholeRequests = 0

    def compute(self):
        all_reqs = [req for req in self.requests]
        self.requests = sorted(all_reqs, key=lambda req: req.rn, reverse=True)  # Sorting requests

        for i in range(len(self.requests)):
            endp_id = self.requests[i].re
            for j in range(len(self.endpoints[endp_id].caches)):
                if (self.caches[self.endpoints[endp_id].caches[j].id].capacity - self.videos[
                    self.requests[i].rv].size) >= 0:
                    if self.requests[i].rv not in self.caches[self.endpoints[endp_id].caches[j].id].videoIDs:
                        self.caches[self.endpoints[endp_id].caches[j].id].videoIDs.append(self.requests[i].rv)
                        self.caches[self.endpoints[endp_id].caches[j].id].capacity -= self.videos[
                            self.requests[i].rv].size
                        if self.caches[self.endpoints[endp_id].caches[j].id].flag1 == 0:
                            self.caches[self.endpoints[endp_id].caches[j].id].flag1 = 1
                            self.usedCaches += 1

    def print_score(self):
        self.wholeRequests = 0
        for i in range(len(self.requests)):
            self.score += (self.endpoints[self.requests[i].re].latency - self.requests[
                i].get_cache_latency) * self.requests.rn
            self.wholeRequests += self.requests.rn
        self.score /= self.wholeRequests


def read_file(filename):
    """Read the input file."""
    data = None
    with open(filename, 'r') as fin:
        line = fin.readline()

        videoNum, endpointNum, requestDescriptions, cacheNum, cacheCapacity = [
            int(num) for num in line.split()]
        videoSizes = [int(num) for num in fin.readline().split()]
        videos = []
        for i in range(videoNum):
            videos.append(Video(i, videoSizes[i], []))

        endpoints = []
        # endpoints = [Endpoint() for count in range(endpointNum)]
        for i in range(0, endpointNum):
            endpointLatency, cachesConnected = [int(num) for num in fin.readline().split()]
            caches = []
            # caches = [Cache(count) for count in range(int(cachesConnected))]
            for j in range(0, cachesConnected):
                cacheId, cacheLatency = [int(num) for num in fin.readline().split()]
                caches.append(Cache(cacheCapacity, cacheLatency, cacheId))
            endpoints.append(Endpoint(i, endpointLatency, caches))

        requests = []
        for i in range(0, requestDescriptions):
            videoId, endpointId, requestNum = [int(num) for num in fin.readline().split()]
            requests.append(Request(videoId, endpointId, requestNum))

        caches = []
        for i in range(cacheNum):
            caches.append(Cache(cacheCapacity, 0, i))

        data = Data(videos, caches, endpoints, requests)
    return data


def write_file(data, filename):
    """Write output file."""
    with open(filename, 'w') as fout:
        fout.write('%d\n' % data.usedCaches)
        for i in range(data.usedCaches):
            fout.write('%d ' % data.caches[i].id)
            for j in range(len(data.caches[i].videoIDs)):
                fout.write('%d ' % data.caches[i].videoIDs[j])
            fout.write('\n')


def main():
    """Main function."""

    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])

    print('Running on file: %s' % sys.argv[1])

    # read input file
    _data = read_file(sys.argv[1])
    # print(grid)

    try:
        _data.compute()
        # _data.print_score()
    except KeyboardInterrupt:
        pass

    # write output file
    write_file(_data, sys.argv[2])


if __name__ == '__main__':
    main()
