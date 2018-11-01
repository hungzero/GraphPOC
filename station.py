#!/usr/bin/env python3


class Station:
    """
    Station Class
    """

    def __init__(self, line, number, name="", station_type="N"):
        self.line = line
        self.number = number
        self.name = name
        self.station_type = station_type
        self.code = line + ":" + str(number)
        self.links = []
        self.trains = []
        self.connected_stations = []
