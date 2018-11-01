#!/usr/bin/env python3
import sys
import metro_network

if __name__ == "__main__":

    # control variables
    # filename = "input_metro_network_2"
    # filename = "input_metro_network"
    filename = "delhi-metro-stations"
    max_loop = 100
    sleep_time = 0.1
    parallel_path = False
    print_each_step = True
    print_statistic = True
    print_by_line = True

    # init the metro network
    metro = metro_network.MetroNetwork(filename)

    # operate the metro network
    metro.operate(max_loop, sleep_time, parallel_path, print_each_step, print_statistic, print_by_line)

    # print the statistic after operate
    print("Final statistic:")
    sys.stdout.write("Total loop:" + str(metro.total_loop) + "\t" +
                     "Total trains:" + str(metro.total_train) + "\t" +
                     "Running trains:" + str(metro.trains_running) + "\t" +
                     "Trains at start:" + str(metro.trains_at_start) + "\t" +
                     "Trains at end:" + str(metro.trains_at_end) + "\n")


