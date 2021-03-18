#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tp
import workoutBuilder
import json
from pathlib import Path

TP_DOMAIN = 'https://tpapi.trainingpeaks.com/'
WORKOUT_URL = TP_DOMAIN + 'fitness/v5/athletes/{}/workouts'
RECALC_TSS = TP_DOMAIN + 'fitness/v1/athletes/{}/commands/workouts/{}/recalctss'
DIRECTORY_WORKOUT = './Build.Me.Up'

if __name__ == '__main__':
    username, password = open("trainingpeaks.key").read().rstrip().split(':')
    tpconnect = tp.TPconnect(username, password)
    # print("Connected to TrainingPeaks")
    workoutBuilder = workoutBuilder.WorkoutBuilder()
    workout = workoutBuilder.parseXMLfile('Build.Me.Up/Week.02/Build.Me.Up.W02W03.Orange.Unicorn.zwo')
    tpconnect.upload_workout('Test', workout)
    # wourkoutBuilder.transformWorkout()
