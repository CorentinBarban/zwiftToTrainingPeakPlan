import xml.etree.ElementTree as ET
import json


def adapter_zwo_power_to_tp_power(zwo_power_name):
    adapter = {
        "Warmup": "PowerLow",
        "SteadyState": "Power",
        "FreeRide": "active",
        "Cooldown": "PowerLow",
        "Ramp": "PowerHigh",
    }
    return adapter.get(zwo_power_name)


def adapter_zwo_step_to_tp_step(zwo_step_name):
    adapter = {
        "Warmup": "warmUp",
        "SteadyState": "active",
        "FreeRide": "active",
        "IntervalsT": "active",
        "Cooldown": "coolDown",
        "Ramp": "active",
    }
    return adapter.get(zwo_step_name)


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
            if workoutStep.tag == 'IntervalsT':
                for i in range(int(workoutStep.get('Repeat'))):
                    time_end = time_begin + int(workoutStep.get('OnDuration'))
                    my_workout_json['structure'].append({
                        'type': 'step',
                        'length': {"value": 1,
                                   "unit": "repetition"},
                        'steps': [{
                            "name": 'Active interval',
                            "length": {
                                "value": int(workoutStep.get('OnDuration')),
                                "unit": "second"
                            },
                            "targets": [
                                {
                                    "minValue": round(float(workoutStep.get('OnPower')) * 100, 0),
                                    "maxValue": round(float(workoutStep.get('OnPower')) * 100, 0),
                                }
                            ],
                            "intensityClass": adapter_zwo_step_to_tp_step(workoutStep.tag),
                            "openDuration": bool('false')
                        }],
                        'begin': time_begin,
                        'end': time_end,
                    })
                time_begin = time_end
                time_end = time_begin + int(workoutStep.get('OffDuration'))
                my_workout_json['structure'].append({
                    'type': 'step',
                    'length': {"value": 1,
                               "unit": "repetition"},
                    'steps': [{
                        "name": 'Rest interval',
                        "length": {
                            "value": int(workoutStep.get('OffDuration')),
                            "unit": "second"
                        },
                        "targets": [
                            {
                                "minValue": round(float(workoutStep.get('OffPower')) * 100, 0),
                                "maxValue": round(float(workoutStep.get('OffPower')) * 100, 0),
                            }
                        ],
                        "intensityClass": adapter_zwo_step_to_tp_step(workoutStep.tag),
                        "openDuration": bool('false')
                    }],
                    'begin': time_begin,
                    'end': time_end,
                })
                time_begin = time_end
            else:
                time_end = time_begin + int(workoutStep.get('Duration'))
                my_workout_json['structure'].append({
                    'type': 'step',
                    'length': {"value": 1,
                               "unit": "repetition"},
                    'steps': [{
                        "name": workoutStep.tag,
                        "length": {
                            "value": int(workoutStep.get('Duration')),
                            "unit": "second"
                        },
                        "targets": [
                            {
                                "minValue": 50 if workoutStep.tag == 'FreeRide' else round(float(
                                    workoutStep.get(adapter_zwo_power_to_tp_power(workoutStep.tag))) * 100, 0),
                                "maxValue": 60 if workoutStep.tag == 'FreeRide' else round(float(
                                    workoutStep.get(adapter_zwo_power_to_tp_power(workoutStep.tag))) * 100, 0),
                            }
                        ],
                        "intensityClass": adapter_zwo_step_to_tp_step(workoutStep.tag),
                        "openDuration": bool('false')
                    }],
                    'begin': time_begin,
                    'end': time_end,
                })
                time_begin = time_end
        my_workout_json['primaryLengthMetric'] = "duration"
        my_workout_json['primaryIntensityMetric'] = "percentOfFtp"
        my_workout_json['primaryIntensityTargetOrRange'] = "range"
        with open('createdExample.json', 'w') as outfile:
            json.dump(my_workout_json, outfile, indent=4)
        return json.dumps(my_workout_json)


if __name__ == '__main__':
    pass
