import xml.etree.ElementTree as ET
import json


class WorkoutBuilder(object):
    def __init__(self):
        pass

    def parseXMLfile(self, file_path):
        my_workout_json = {"structure": []}
        time_begin = 0
        time_end = 0
        tree = ET.parse(file_path)
        root = tree.getroot()
        for workoutStep in root.find('workout'):
            print(workoutStep.attrib)
            time_end = time_begin + int(workoutStep.get('Duration'))
            my_workout_json['structure'].append({
                'type': 'step',
                'length': {"value": 1,
                           "unit": "repetition"},
                'steps': {
                    "name": "Warm up",
                    "length": {
                        "value": int(workoutStep.get('Duration')),
                        "unit": "second"
                    },
                    "targets": [
                        {
                            "minValue": 40,
                            "maxValue": 50
                        }
                    ],
                    "intensityClass": "warmUp",
                    "openDuration": 'false'
                },
                'begin': time_begin,
                'end': time_end,
            })
            time_begin = time_end
        with open('createdExample.json', 'w') as outfile:
            json.dump(my_workout_json, outfile, indent=4)


if __name__ == '__main__':
    pass
