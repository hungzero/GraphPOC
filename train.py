#!/usr/bin/env python3
import random


class Train:
    """
    Train Class
    """

    def __init__(self, name, position="", path=[]):
        self.name = name
        self.position = position
        self.path = path

    def check_moveable(self, station):
        """
        Check if the input station can be move in
        :param station: input station instance
        :return: True or False
        """
        if len(station.trains) < 1 or station.station_type == "E":
            return True
        return False

    def move(self, current_station, next_station):
        """
        Move the train to the next station,
        remove the train in current station after that
        :param current_station:
        :param next_station:
        :return: none
        """
        self.position = next_station.code
        next_station.trains = [self.name] + next_station.trains
        current_station.trains.pop(0)

    def move_random(self, metro_network):
        """
        Move random to a station in connected and link station list
        if that station is moveable, if all are not moveable, train will wait
        :return:
        """
        current_station = metro_network.get_station(self.position)
        possible_next_stations = current_station.connected_stations + current_station.links
        if len(possible_next_stations) > 0:
            random.shuffle(possible_next_stations)
            for possible_next_station in possible_next_stations:
                next_station = metro_network.get_station(possible_next_station)
                if self.check_moveable(next_station):
                    self.move(current_station, next_station)
                    break

    def move_follow_path(self, metro_network):
        """
        Follow path to the next station in path list
        if that station is moveable, if it are not moveable, train will wait
        :return:
        """
        if len(self.path) > 0:
            current_station = metro_network.get_station(self.position)
            possible_next_station = self.path[0]
            next_station = metro_network.get_station(possible_next_station)
            if self.check_moveable(next_station):
                self.move(current_station, next_station)
                self.path.pop(0)
