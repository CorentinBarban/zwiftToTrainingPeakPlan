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


    # username, password = open("trainingpeaks.key").read().rstrip().split(':')
    # tpconnect = tp.TPconnect(username, password)
    # print("Connected to TrainingPeaks")
    workoutBuilder = workoutBuilder.WorkoutBuilder()
    workoutBuilder.parseXMLfile('Build.Me.Up/Week.01/Build.Me.Up.W01W01.Zone.Benchmarking.zwo')
    # wourkoutBuilder.transformWorkout()