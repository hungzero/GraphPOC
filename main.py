#!/usr/bin/env python3
import sys
import random
import time

lines = []
start_point = {}
end_point = {}
trains = []


def read_input_data(input_filename):
    for line in open(input_filename, "r"):
        line = line.rstrip('\n')
        if "#" in line:
            new_line = {"name": line.split("_")[1], "stations": []}
            lines.append(new_line)
        if ":station" in line:
            station_infos = line.split(':')
            link_stations = []
            if len(station_infos) > 2:
                link_stations.append(station_infos[2].split('_')[1]+":"+station_infos[2].split('_')[2])
            new_station = {"line": station_infos[1].split('_')[1], "number": station_infos[0],
                           "name": station_infos[1].split('_')[1]+":"+station_infos[0],
                           "links": link_stations, "trains": [], "connected_stations": [],
                           "type": "N"}
            if len(lines) > 0:
                lines[len(lines)-1]["stations"].append(new_station)
        if "START" in line:
            new_start = line.split(':')
            global start_point
            start_point = {'line': new_start[1].split("_")[1], 'number': new_start[2],
                           "name": new_start[1].split("_")[1]+":"+new_start[2]}
        if "END" in line:
            new_end = line.split(':')
            global end_point
            end_point = {'line': new_end[1].split("_")[1], 'number': new_end[2],
                           "name": new_end[1].split("_")[1]+":"+new_end[2]}
        if 'TRAINS' in line:
            train_num = int(line.split(':')[1])
            for train in range(1, train_num+1):
                trains.append({"name": "T."+str(train), "position": start_point["name"], "path": []})


def update_metro_network_infomation(metro_lines,start_station , end_station, trains_list):
    for line in metro_lines:
        for station_number in range(0, len(line["stations"])):
            current_station = line["stations"][station_number]
            if start_station["name"] == current_station["name"]:
                current_station["type"] = "S"
                for train in trains_list:
                    current_station["trains"].append(train["name"])
            if end_station["name"] == current_station["name"]:
                current_station["type"] = "E"
            if station_number - 1 >= 0:
                current_station["connected_stations"].append(line["stations"][station_number - 1]["name"])
            if station_number + 1 < len(line["stations"]):
                current_station["connected_stations"].append(line["stations"][station_number + 1]["name"])
    return metro_lines


def search_dictionaries(key, value, list_of_dictionaries):
    return [element for element in list_of_dictionaries if element[key] == value]


def get_station(metro_lines, station_name):
    line = search_dictionaries("name", station_name.split(":")[0], metro_lines)[0]
    stations = search_dictionaries("name", station_name, line["stations"])
    return stations[0]


def get_line(metro_lines, station_name):
    line = search_dictionaries("name", station_name.split(":")[0], metro_lines)[0]
    return line


def print_metro_network(metro_lines, start_station, end_station, start_train_number, trains, color_list, loop):

    end_station_train_number = len(end_station["trains"])
    start_station_train_number = len(start_station["trains"])
    running_train_number = len(trains)

    sys.stdout.write("====== Metro network ======\n")

    for line_num in range(len(metro_lines)):
        line = metro_lines[line_num]
        sys.stdout.write("\033[1;"+str(color_list[line_num])+"m "+"line "+line["name"]+":\t")

        # print line 1
        for station_number in range(0, len(line["stations"])):
            sys.stdout.write(line["stations"][station_number]["name"])
            if station_number + 1 < len(line["stations"]):
                sys.stdout.write("\t")
        sys.stdout.write("\n\t\t")

        # print line 2
        for station_number in range(0, len(line["stations"])):
            current_station = line["stations"][station_number]
            if current_station["trains"]:
                sys.stdout.write(current_station["trains"][0])
            elif len(current_station["links"]) > 0:
                sys.stdout.write("|")
            else:
                sys.stdout.write(" ")
            if station_number + 1 < len(line["stations"]):
                sys.stdout.write("\t")
        sys.stdout.write("\n\t\t")

        # print line 3
        for station_number in range(0, len(line["stations"])):
            current_station = line["stations"][station_number]

            if len(current_station["links"]) > 0:
                sys.stdout.write(current_station["links"][0])
            else:
                sys.stdout.write(" ")
            if current_station["type"] != "N":
                sys.stdout.write("("+current_station["type"]+")")
            if station_number + 1 < len(line["stations"]):
                sys.stdout.write("\t")
        sys.stdout.write("\033[0;0m \n\n")

    sys.stdout.write("Loop: " + str(loop)
                     + "\tTotal Trains: " + str(start_train_number)
                     + "\tRunning trains: " + str(running_train_number)
                     + "\tAt Start(" + start_station["name"] + "): " + str(start_station_train_number)
                     + "\tAt End(" + end_station["name"] + "): " + str(end_station_train_number))
    sys.stdout.write("\n")


def move_train(metro_lines, train, next_station_name):
    line = get_line(metro_lines, train["position"])
    current_station = get_station(metro_lines, train["position"])
    next_station = get_station(metro_lines, next_station_name)
    if int(next_station["number"]) > 0 and int(next_station["number"]) <= len(line["stations"]):
        train["position"] = next_station["name"]
        next_station["trains"] = [train["name"]] + next_station["trains"]
        current_station["trains"].pop(0)


def random_color(number):
    color_code_list = []
    for num in range(number):
        color_code_list.append(31+num)
    random.shuffle(color_code_list)
    return color_code_list


def bfs(metro_lines, start_position, end_position):
    queue = [[start_position]]
    checked = [start_position]
    return_paths = []

    while queue:
        current_path = queue.pop(0)
        current_point = current_path[-1]

        station_at_current_point = get_station(metro_lines, current_point)

        # expand form current point
        point_to_expand = station_at_current_point["links"] + station_at_current_point["connected_stations"]
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


def bfs_innitial_path_calculate(metro_lines, start_position, end_position, input_trains):
    all_paths = bfs(metro_lines, start_position, end_position)
    if len(all_paths):
        path_costs = []
        # calculate path cost
        for path_index in range(0, len(all_paths)):
            all_paths[path_index].pop(0)
            path_cost = {"path": all_paths[path_index], "cost" :len(all_paths[path_index])}
            path_costs.append(path_cost)

        for train in input_trains:
            min_path = path_costs[0]
            for path in path_costs:
                if path["cost"] < min_path["cost"]:
                    min_path = path
            train["path"] = min_path["path"].copy()
            min_path["cost"] += 1



def bfs_move(metro_lines, train, end_station):
    current_station = get_station(metro_lines, train["position"])
    paths = bfs(metro_lines, current_station["name"], end_station)
    if paths is not None:
        paths[0].pop(0)
        possible_next_station = paths[0].pop(0)
        next_station = get_station(metro_lines, possible_next_station)
        if len(next_station["trains"]) < 1 or next_station["type"] == "E":
            next_station_position = next_station["name"]
            return next_station_position
    return None

def path_move(metro_lines, train, end_station):
    paths = train["path"]
    if len(paths) > 0:
        possible_next_station = paths[0]
        next_station = get_station(metro_lines, possible_next_station)
        if len(next_station["trains"]) < 1 or next_station["type"] == "E":
            next_station_position = next_station["name"]
            paths.pop(0)
            return next_station_position
    return None


def wandering_move(metro_lines, train):
    current_station = get_station(metro_lines, train["position"])
    possible_next_stations = current_station["connected_stations"] + current_station["links"]
    if len(possible_next_stations) > 0:
        random.shuffle(possible_next_stations)
        for possible_next_station in possible_next_stations:
            next_station = get_station(metro_lines, possible_next_station)
            if len(next_station["trains"]) < 1 or next_station["type"] == "E":
                next_station_position = next_station["name"]
                return next_station_position
    return None


def main():
    read_input_data("input_metro_network")
    update_metro_network_infomation(lines, start_point, end_point, trains)

    color_list = random_color(len(lines))

    start_train_number = len(trains)

    # put the train in start
    start_station = get_station(lines, start_point["name"])
    end_station = get_station(lines, end_point["name"])

    bfs_innitial_path_calculate(lines, start_point["name"], end_point["name"], trains)

    max_loop = 100
    loop = 1

    # main loop
    while loop <= max_loop:

        print_metro_network(lines, start_station, end_station, start_train_number, trains, color_list, loop)

        if len(trains) < 1:
            break

        for train in trains:
            # next_move = wandering_move(lines, train)
            next_move = path_move(lines, train, end_point["name"])
            if next_move is not None:
                move_train(lines, train, next_move)
                if next_move == end_point["name"]:
                    trains.remove(train)

        time.sleep(0.8)
        loop += 1


if __name__ == "__main__":
    main()

