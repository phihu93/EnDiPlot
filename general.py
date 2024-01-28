#!/usr/bin/env python3

def read_options(opf):
    option_data = {}
    option_data['files'] = []
    option_data['offset'] = []
    option_data['colors'] = []
    option_data['titles'] = []
    option_data['nfiles'] = -1
    option_data['plot_titles'] = False
    option_data['plot_titles'] = False
    with open(opf) as fil:
        for line in fil:
            if line[0] == '<':
                key = line.split('<')[1].split()[0]
                continue
            elif line[0] == ' ':
                key_input = line.split()[0]
            if key == "files":
                option_data[key].append(key_input)
            elif key == "offset":
                option_data[key].append(int(key_input))
            elif key == "colors":
                option_data[key].append(key_input)
            elif key == "nfiles":
                option_data[key] = int(key_input)
            elif key == "plot_titles":
                option_data[key] = bool(key_input)
            elif key == "titles":
                option_data[key].append(key_input)
            elif key == "plot_labels":
                option_data[key] = bool(key_input)

    return option_data
