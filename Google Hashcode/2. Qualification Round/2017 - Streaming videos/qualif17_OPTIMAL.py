import os
import sys
from collections import defaultdict

from tqdm import tqdm


def video_endpoint_cost(videoID, endpoint):
    if endpoint[1]:  # If there are caches for this endpoint
        for (cacheID, latency) in endpoint[1].items():
            if videoID in CACHES[cacheID]:  # If video is in a cache
                return latency
        else:
            return endpoint[0]  # Datacenter latency
    else:  # No caches available means that there is no reason to care about this endpoint
        return 0


def request_cost(req):  # tuples: (video, endpoint, amount of requests)
    return video_endpoint_cost(req[0], ENDPOINTS[req[1]]) * req[2]  # Cost is mul by the amount of requests


def how_much_can_we_improve(video):
    _video_index = video[0]  # Get info for the selected video
    _video_size = VIDEOS[_video_index]

    # If there is a best cache for this video
    if BEST_CACHE_CACHE[_video_index] is not None:
        best_cache = BEST_CACHE_CACHE[_video_index]
        # If the video still 'fits' in the cache then return.
        if _video_size <= CACHE_CAPACITY[best_cache[0]]:
            return best_cache[1], best_cache[0], video

    requests = video[1][1]
    saved_time = defaultdict(lambda: 0)

    for r in requests:  # REQUESTS: (video,endpoint,requests) , ENDPOINTS: datacenterLatency,{cache:cache_latency}
        caches = ENDPOINTS[r[1]][1]  # Available caches for this request
        latency = ENDPOINTS[r[1]][0]  # Datacenter latency
        # The min latency of all the cache items with this video.Also includes datacenter latency just in case.
        current_cost = min([c[1] for c in caches.items() if video[0] in CACHES[c[0]]] + [latency])

        # For all the available caches in this endpoint for this video
        for _cache in caches.items():  # caches.items(): (id,latency)
            if _video_size < CACHE_CAPACITY[_cache[0]]:  # If this video can fit into this cache
                if current_cost > _cache[1]:  # If we can get lower latency
                    # Add to saved time the latency difference multiplied by the amount of requests
                    saved_time[_cache[0]] += (current_cost - _cache[1]) * r[2]  # r[2] : Number of requests for this vid

    if not saved_time:  # Latency is optimal, cant get better results
        del vids[video[0]]  # Delete video
        pbar.update(1)  # Progress loading bar
        return 0, None, video

    # Pick the cache with the most time saved.
    best_cache = sorted(saved_time.items(), key=lambda x: x[1], reverse=True)[0]
    # Save the best cache for this video
    BEST_CACHE_CACHE[_video_index] = best_cache
    # (time saved, cache, video)
    return best_cache[1], best_cache[0], video


if __name__ == '__main__':
    InputFolder = ''
    OutputFolder = ''

    if len(sys.argv) < 3:
        InputFolder = '..\inputVideos'  # Reads all the files inside this folder
        OutputFolder = 'output'  # Same names as input
    else:
        InputFolder = sys.argv[1]
        OutputFolder = sys.argv[2]

    if not os.path.exists(InputFolder):
        print('The given input folder argument is invalid..')
        sys.exit(-1)

    for video_file_name in os.listdir(InputFolder):
        video_path = os.path.join(InputFolder, video_file_name)
        print('Processing: ' + video_file_name)
        with open(video_path, 'r') as file:
            [Videos, Endpoints, Requests, Caches, CacheSize] = [int(n) for n in file.readline().split()]
            VIDEOS = [int(n) for n in file.readline().split()]
            ENDPOINTS = []
            REQUESTS = []
            CACHES = defaultdict(lambda: set())
            CACHE_CAPACITY = defaultdict(lambda: CacheSize)
            BEST_CACHE_CACHE = defaultdict(lambda: None)  # Best cache for a given video

            for _ in range(Endpoints):  # Read info for each Endpoint
                [datacenterLatency, numOfConCaches] = [int(n) for n in file.readline().split()]
                curEndpoint = (datacenterLatency, dict())  # curEndpoint[0] = datacenterLatency

                for _ in range(numOfConCaches):  # Read info for each cache and its latency
                    [cur_cache, cur_cache_latency] = [int(n) for n in file.readline().split()]
                    # Save on each Endpoint every available cache and its latency
                    curEndpoint[1][cur_cache] = cur_cache_latency

                ENDPOINTS.append(curEndpoint)  # Save every Endpoint in random order (read order)

            for _ in range(Requests):  # For each request save tuple (video endpoint requests)
                REQUESTS.append(tuple([int(n) for n in file.readline().split()]))

            # lambda sets the default value for every new item inserted in the dict. Avoids for-loop for init.
            # vids contains the cost of each video and its requests. (cost,{requests})
            vids = defaultdict(lambda: [0, []])
            for req in tqdm(REQUESTS, desc='Requests'):  # tuples: (videoID, endpoint, amount of requests)
                req_video_id = req[0]  # Video ID of this request
                vids[req_video_id][0] += request_cost(req)  # vids[videoID][0] += cost
                vids[req_video_id][1].append(req)  # vids[videoID][1].append(req)

            pbar = tqdm(total=len(vids))
            pbar.set_description('Videos')
            while vids:
                # The results of applying the function to the items of the argument sequence
                vid_list = map(how_much_can_we_improve, list(vids.items()))  # (time saved, cache, video)
                # Max finds
                time_saved, cache, video = max(vid_list, key=lambda x: VIDEOS[x[2][0]])
                if cache is None:
                    continue

                video_index = video[0]
                video_size = VIDEOS[video_index]

                CACHES[cache].add(video_index)
                CACHE_CAPACITY[cache] -= video_size
                BEST_CACHE_CACHE[video_index] = None
                video[1][0] -= time_saved
            pbar.close()

            output_path = os.path.join(OutputFolder, video_file_name.replace('.in', '.out'))
            if not os.path.exists(OutputFolder):
                os.makedirs(OutputFolder)

            with open(output_path, 'w') as out_file:
                out_file.write('{}\n'.format(CACHES.items().__len__()))
                for cache, videos in CACHES.items():
                    if videos:
                        out_file.write('{0} {1}\n'.format(cache, " ".join(map(str, list(videos)))))

            print('\nDone processing ' + video_file_name + '\n\n')
