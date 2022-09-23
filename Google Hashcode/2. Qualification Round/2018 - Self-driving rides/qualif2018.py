import os
import sys

import numpy as np
from tqdm import tqdm


#   Hashcode 2018 qualification round
#   This is the extended round solution which takes into account more constraints such as bonuses.
#
#   Original score: 24.8M
#   Extended round score: 45.6M
#
#   a_example           10
#   b_should_be_easy    176802
#   c_no_hurry          14765689
#   d_metropolis        10647531
#   e_high_bonus        20011469
#
#
#   Team members:
#       Giorgos Stamatakis
#       Christos Spyridakis
#       Tzanis Fotakis
#       Nikolaos Bampaliaris

class Ride:
    def __init__(self, id, a, b, x, y, s, f):
        self.id = id
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s  # Start time
        self.f = f  # Deadline
        self.vehicle = None
        self.value = 0

    def waiting_time(self, step):
        return 0 if step >= self.s else self.s - step

    def ride_length(self):
        return abs(self.a - self.x) + abs(self.b - self.y)

    def estimated_time(self, target):
        return abs(self.x - target[0]) + abs(self.y - target[1])

    def stay_time(self, vehicle, pick_dist):
        return 0 if self.s - vehicle.step - pick_dist < 0 else self.s - vehicle.step - pick_dist


class Vehicle:
    def __init__(self, id):
        self.id = id
        self.R = 0  # COORDINATES
        self.C = 0
        self.nextRide = -1
        self.schedule = []
        self.step = 0
        self.rides = []

    def get_distance_from_target(self, a, b):
        return abs(self.R - a) + abs(self.C - b)

    def get_steps(self, ride):
        return self.get_distance_from_target(ride.a, ride.b) + \
               ride.waiting_time(self.step) + \
               ride.ride_length()

    def updateCoord(self, x, y):
        self.R = x
        self.C = y

    def can_make_it(self, ride, pick_dist):
        return pick_dist + self.step - ride.s <= 0


class Data:
    def __init__(self, R, C, F, N, B, T, rides):
        self.R = R
        self.C = C
        self.F = F
        self.N = N
        self.B = B
        self.T = T
        self.scheduled = []
        self.vehicles = [Vehicle(k + 1) for k in range(self.F)]
        self.rides = rides

    def compute(self):
        vehiclesBar = tqdm(total=len(self.vehicles))
        vehiclesBar.set_description('Vehicles')
        # Initial assignment
        for curVehicle in self.vehicles:
            self.assign_ride(curVehicle)
            vehiclesBar.update(1)
        vehiclesBar.close()

        schedBar = tqdm()
        schedBar.set_description('Scheduling')
        while len(self.scheduled) > 0:
            vehicle, steps = sorted(self.scheduled, key=lambda i: i[1])[0]
            self.scheduled.remove((vehicle, steps))
            self.assign_ride(vehicle)
            schedBar.update(1)
        schedBar.close()

    def assign_ride(self, vehicle, count=None):
        if count is None:
            count = {}
        original_vehicle = vehicle

        for curRide in self.rides:
            count[curRide.id] = vehicle.get_steps(curRide)

        # Could probably use avg
        median = np.median([r.a for r in self.rides]), np.median([r.b for r in self.rides])

        # PRUNING TIME
        candidates = [r for r in self.rides
                      if r.vehicle is None and  # Be available
                      count[r.id] - self.T - vehicle.step < 0 and  # Be reachable
                      vehicle.step + count[r.id] - r.f <= 0]  # Be successful

        # Select the one with the highest score which considers all the available constraints(distance,bonus,...)
        candidates = sorted(list(candidates), key=lambda r: self.score(vehicle, r, median), reverse=True)

        if len(candidates) > 0:
            selected_ride = candidates[0]
        else:
            return None

        selected_ride.vehicle = original_vehicle
        original_vehicle.rides.append(selected_ride)
        steps = original_vehicle.get_steps(selected_ride)
        original_vehicle.step += steps
        original_vehicle.updateCoord(selected_ride.x, selected_ride.y)
        self.scheduled.append((original_vehicle, steps))

        return selected_ride

    def score(self, vehicle, ride, median):
        drive_dist = ride.ride_length()
        pick_dist = vehicle.get_distance_from_target(ride.a, ride.b)
        wait_time = ride.stay_time(vehicle, pick_dist)
        bonus = self.B if vehicle.can_make_it(ride, pick_dist) else 0
        dest_avg_dist = ride.estimated_time(median)

        return drive_dist - pick_dist - wait_time + bonus - dest_avg_dist

    def writeFile(self, file):
        for vehicle in self.vehicles:
            file.write(str(len(vehicle.rides)) + ' ')
            for r in vehicle.rides:
                file.write(str(r.id) + ' ')
            file.write('\n')


def readFile(file):
    [R, C, F, N, B, T] = [int(n) for n in file.readline().split()]
    rides = []
    for i in range(N):
        [a, b, x, y, s, f] = [int(n) for n in file.readline().split()]
        rides.append(Ride(i, a, b, x, y, s, f))
    return Data(R, C, F, N, B, T, rides)


if __name__ == '__main__':

    # Create a list with the two file_names.
    [InputFolder, OutputFolder] = ['inputRides', 'outputRides'] if len(sys.argv) < 3 else sys.argv[1:3]

    # Does the input folder exists?
    if not os.path.exists(InputFolder):
        print("Invalid input folder specified.")
        exit(-1)

    # Get the test name of each file inside the input folder.
    for testCaseName in os.listdir(InputFolder):
        # Create the full path of the input folder.
        testCasePath = os.path.join(InputFolder, testCaseName)

        # Open the input folder.
        with open(testCasePath, 'r') as inputFile:
            print('Starting ' + testCaseName)
            # Create the data.
            _data = readFile(inputFile)

            # Close The File.
            inputFile.close()

            # Run the algorithm.
            try:
                _data.compute()

            # Abandon the computation (Fuck that shit).
            except KeyboardInterrupt:
                pass

            # Create the full output folder path.
            outputPath = os.path.join(OutputFolder, testCaseName.replace('.in', '.out'))

            # Check if the output folder exists, else create it.
            os.path.exists(OutputFolder) or os.makedirs(OutputFolder)

        # Open the output file.
        with open(outputPath, 'w') as outputFile:
            # Write the data to the file.
            _data.writeFile(outputFile)

            # Close the file.
            outputFile.close()
