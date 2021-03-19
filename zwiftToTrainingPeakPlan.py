#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tp
import workoutBuilder
import datetime
from pathlib import Path

TP_DOMAIN = 'https://tpapi.trainingpeaks.com/'
WORKOUT_URL = TP_DOMAIN + 'fitness/v5/athletes/{}/workouts'
RECALC_TSS = TP_DOMAIN + 'fitness/v1/athletes/{}/commands/workouts/{}/recalctss'
DIRECTORY_WORKOUT = 'Build.Me.Up/'


def get_next_monday(date):
    return date + datetime.timedelta(days=-date.weekday(), weeks=1)


def upload_workout_from_directory(file_path, date):
    my_workout_builder = workoutBuilder.WorkoutBuilder(file_path)
    my_workout_builder.parse_xml_file()
    my_workout_builder.define_workout_name_from_filename()
    tpconnect.upload_workout('Zwift - Build Me Up -' + my_workout_builder.get_workout_name(),
                             my_workout_builder.get_workout_structure(),
                             my_workout_builder.get_workout_time(), date.strftime("%Y-%m-%dT%H:%M:%S"))


def upload_all_workout_from_directory(directory_path, ):
    day = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday(), weeks=1)
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            print(f)
            upload_workout_from_directory(os.path.relpath(os.path.join(root, f), "."), get_next_monday(day))
        day = get_next_monday(day)


def recalculate_tss_if_running():

    workout_id = 1350870442
    payload = {"value": "bikePace"}
    url = RECALC_TSS.format(tpconnect.athlete_id, workout_id)
    res = tpconnect.session.post(url, payload)
    if res.status_code != 200:
        print("[{}] Error when recalculating tss".format(workout_id))
        return

if __name__ == '__main__':
    username, password = open("trainingpeaks.key").read().rstrip().split(':')
    tpconnect = tp.TPconnect(username, password)
    tpconnect.init()
    # upload_all_workout_from_directory(DIRECTORY_WORKOUT)
    # print("Connected to TrainingPeaks")
    recalculate_tss_if_running()
    # wourkoutBuilder.transformWorkout()
