# app/utils
import json

def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            coordinates.append({
                'latitude': data['x'],
                'longitude': data['y'],
            })
    return coordinates
