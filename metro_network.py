#!/usr/bin/env python3
import sys
import time

import station
import line
import train


class MetroNetwork:
    """
    Metro Network Class
    """

    def __init__(self, input_filename):
        # properties
        self.input_filename = input_filename
        self.lines = []
        self.start_station = None
        self.end_station = None
        self.trains = []
        self.print_by_line = False

        # statistics
        self.total_loop = 0
        self.total_train = 0
        self.trains_at_start = 0
        self.trains_at_end = 0
        self.trains_running = 0

        self.read_input_data(input_filename)
        self.update_metro_network_information()


    def __str__(self):
        """
        Print out the the stations that occupied by trains
        The Start and End stations will have special format
        :return: text to print
        """
        return_string = ""
        for line in self.lines:
            if self.print_by_line:
                return_string += line.name + ":\t"
            for station_number in range(0, len(line.stations)):
                current_station = line.stations[station_number]
                if len(current_station.trains) > 0:
                    return_string += current_station.name + "(" + current_station.code + ")-"
                    return_string += current_station.trains[0]
                    if current_station.station_type != "N":
                        return_string += "-" + current_station.station_type + "-" + str(len(current_station.trains))
                    return_string += "\t"
            if self.print_by_line:
                return_string += "\n"
        return_string += "\n"
        return return_string

    def read_input_data(self, input_filename):
        """
        Read the metro network form the file
        :param input_filename: filename contains metro network information with the right format
        :return: None
        """
        for one_line in open(input_filename, "r"):
            one_line = one_line.rstrip('\n')
            if "#" in one_line:
                current_line = line.Line(one_line.split("#")[1].rstrip())
                current_line.stations = []
                self.lines.append(current_line)

            if "START" in one_line:
                current_line = None
                new_start = one_line.split(':')
                self.start_station = station.Station(new_start[0].split("=")[1], int(new_start[1]), "", "S")

            if "END" in one_line:
                current_line = None
                new_end = one_line.split(':')
                self.end_station = station.Station(new_end[0].split("=")[1], int(new_end[1]), "", "E")

            if 'TRAINS' in one_line:
                current_line = None
                train_num = int(one_line.split('=')[1])
                for one_train in range(1, train_num + 1):
                    new_train = train.Train("T." + str(one_train), self.start_station.code)
                    self.trains.append(new_train)

                # update trains statistic value
                self.total_train = len(self.trains)

            if ":" in one_line and current_line is not None:
                station_infos = one_line.split(':')
                if len(station_infos) > 1:
                    new_station = station.Station(current_line.name, int(station_infos[0]), station_infos[1])
                    current_line.stations.append(new_station)

    def get_line(self, line_name):
        """
        Get a line by name
        :param line_name: input line name
        :return: matching line
        """
        for one_line in self.lines:
            if one_line.name == line_name:
                return one_line

    def get_station(self, station_code):
        """
        Get a station by station code
        :param station_code: station code (<line name>:<number>)
        :return: matching station
        """
        one_line = self.get_line(station_code.split(":")[0])
        one_station = one_line.get_station(int(station_code.split(":")[1]))
        return one_station

    def find_stations_by_name(self, name):
        """
        Find stations in metro network with input name
        :param name: station name to find
        :return: list of stations in metro network that match the name
        """
        match_stations = []
        for line in self.lines:
            for station_number in range(0, len(line.stations)):
                current_station = line.stations[station_number]
                if current_station.name == name:
                    match_stations.append(current_station)
        return match_stations

    def update_metro_network_information(self):
        """
        Parse and update the metro network with init infomations like start, end, trains positions
        :return: none
        """
        for line in self.lines:
            for station_number in range(0, len(line.stations)):
                current_station = line.stations[station_number]

                # update start and end station position
                if self.start_station.code == current_station.code:
                    current_station.station_type = "S"
                    for one_train in self.trains:
                        current_station.trains.append(one_train.name)
                if self.end_station.code == current_station.code:
                    current_station.station_type = "E"

                # update the link of stations in one line
                # (one station link to the previous and next one of the same line)
                if station_number - 1 >= 0:
                    current_station.connected_stations.append(line.stations[station_number - 1].code)
                if station_number + 1 < len(line.stations):
                    current_station.connected_stations.append(line.stations[station_number + 1].code)

                # update the link with other lines
                # by scan all stations of the metro system for stations with the same name
                link_stations = self.find_stations_by_name(current_station.name)
                for link_station in link_stations:
                    if link_station.code != current_station.code:
                        current_station.links.append(link_station.code)

        # update statistic
        self.trains_at_start = len(self.get_station(self.start_station.code).trains)
        self.trains_at_end = len(self.get_station(self.end_station.code).trains)
        self.trains_running = len(self.trains)

    def bfs(self, start_position, end_position):
        """
        Breath frist search on the Metro network Graph space (lines and Stations)
        :param start_position: start node (<line name>:<number>)
        :param end_position: end node (<line name>:<number>)
        :return: list of none overlap path from start to end
        """
        queue = [[start_position]]
        checked = [start_position]
        return_paths = []

        while queue:
            current_path = queue.pop(0)
            current_point = current_path[-1]

            station_at_current_point = self.get_station(current_point)

            # expand form current point
            point_to_expand = station_at_current_point.links + station_at_current_point.connected_stations
            for point in point_to_expand:
                # buid path
                if point not in checked:
                    new_path = current_path + [point]
                    if point == end_position:
                        return_paths.append(new_path)
                    else:
                        checked.append(point)
                        queue.append(new_path)
        if len(return_paths) > 0:
            return return_paths
        else:
            return None

    def bfs_initial_path_calculate(self, start_position, end_position, input_trains):
        """
        Calculate all possible none overlap path from start to end using BFS algorithm,
        then assign the shortest path to the trains.
        :param start_position:
        :param end_position:
        :param input_trains:
        :return:
        """
        all_paths = self.bfs(start_position, end_position)
        if len(all_paths):
            path_costs = []
            # calculate path cost
            for path_index in range(0, len(all_paths)):
                all_paths[path_index].pop(0)
                path_cost = {"path": all_paths[path_index], "cost": len(all_paths[path_index])}
                path_costs.append(path_cost)

            min_path = path_costs[0]
            for path in path_costs:
                if path["cost"] < min_path["cost"]:
                    min_path = path

            for train in input_trains:
                train.path = list(min_path["path"])

    def bfs_initial_parallel_path_calculate(self, start_position, end_position, input_trains):
        """
        Calculate all possible none overlap path from start to end using BFS algorithm,
        then assign the shortest path to the trains,
        but after each assign, add a weight value to that path.
        The idea is after a path is assign many time it length + weight become more
        expensive than the next one in the possible path list and the next one will be
        chosen to assign instead of first one.
        :param start_position:
        :param end_position:
        :param input_trains:
        :return:
        """
        all_paths = self.bfs(start_position, end_position)
        if len(all_paths):
            path_costs = []
            # calculate path cost
            for path_index in range(0, len(all_paths)):
                all_paths[path_index].pop(0)
                path_cost = {"path": all_paths[path_index], "cost": len(all_paths[path_index])}
                path_costs.append(path_cost)

            for train in input_trains:
                min_path = path_costs[0]
                for path in path_costs:
                    if path["cost"] < min_path["cost"]:
                        min_path = path
                train.path = list(min_path["path"])
                min_path["cost"] += 1

    def print_step(self, print_each_step, print_statistic):
        """
        Just print out the state of metro network
        :param print_each_step: if true: print the state of each step
        :param print_statistic: if true: print the statistic
        :return:
        """
        # print the metro state
        if print_each_step:
            print(self)
        # print the statistic
        if print_statistic:
            sys.stdout.write("Total loop:" + str(self.total_loop) + "\t" +
                             "Total trains:" + str(self.total_train) + "\t" +
                             "Running trains:" + str(self.trains_running) + "\t" +
                             "Trains at start:" + str(self.trains_at_start) + "\t" +
                             "Trains at end:" + str(self.trains_at_end) + "\n\n")

    def operate(self, max_loop=100, sleep_time=0.2, parallel_path=True, print_each_step=True, print_statistic=True, print_by_line=True):
        """
        Operate the metro network, print it state each loop
        :param parallel_path:
        :param max_loop:
        :param sleep_time:
        :param print_each_step:
        :param print_statistic:
        :param print_by_line:
        :return:
        """
        self.print_by_line = print_by_line

        # calculate initial path for each train
        if parallel_path:
            self.bfs_initial_parallel_path_calculate(self.start_station.code, self.end_station.code, self.trains)
        else:
            self.bfs_initial_path_calculate(self.start_station.code, self.end_station.code, self.trains)

        loop = 0
        # print first time
        self.print_step(print_each_step, print_statistic)

        # main loop
        while loop < max_loop:
            # move each train
            train_index = 0
            while train_index < len(self.trains):
                train = self.trains[train_index]
                train.move_follow_path(self)
                if train.position == self.end_station.code:
                    self.trains.remove(train)
                else:
                    train_index += 1

            loop += 1

            # update statistic value
            self.total_loop = loop
            self.trains_at_start = len(self.get_station(self.start_station.code).trains)
            self.trains_at_end = len(self.get_station(self.end_station.code).trains)
            self.trains_running = len(self.trains)

            # print each loop
            self.print_step(print_each_step, print_statistic)

            if len(self.trains) < 1:
                break

            time.sleep(sleep_time)


