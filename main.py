#!/usr/bin/env python3

lines = []
start_point = {}
end_point = {}
trains = []


def read_input_data(input_filename):
    for line in open(input_filename, "r"):
        line = line.rstrip('\n')
        if "#" in line:
            new_line = {"name": line[1:len(line)], "stations": []}
            lines.append(new_line)
        if ":station" in line:
            station_infos = line.split(':')
            link_stations = []
            if len(station_infos) > 2:
                link_stations.append(station_infos[2])
            new_station = {"line": "line_" + station_infos[1].split('_')[1], "number": station_infos[0],
                           "name": station_infos[1], "links": link_stations, "trains": []}
            if len(lines) > 0:
                lines[len(lines)-1]["stations"].append(new_station)
        if "START" in line:
            new_start = line.split(':')
            global start_point

            start_point = {'line': new_start[1], 'number': new_start[2]}
        if "END" in line:
            new_end = line.split(':')
            global end_point
            end_point = {'line': new_end[1], 'number': new_end[2]}
        if 'TRAINS' in line:
            train_num = int(line.split(':')[1])
            for train in range(1, train_num+1):
                trains.append("T."+str(train))




def main():
    read_input_data("input_metro_network")
    print ("Metro network:" + str(lines))
    print ("START:" + str(start_point))
    print ("END:" + str(end_point))
    print ("TRAINS:" + str(trains))

main()

