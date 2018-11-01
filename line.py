#!/usr/bin/env python3


class Line:
    """
    Line Class
    """

    def __init__(self, name, stations=[]):
        self.name = name
        self.stations = stations

    def get_station(self, station_number):
        """
        Get station by station number
        :param station_number: input station number (int)
        :return:
        """
        return self.stations[station_number - 1]



