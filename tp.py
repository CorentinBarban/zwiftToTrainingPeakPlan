# -*- coding: utf-8 -*-
# import fcntl
from urllib.request import Request

import requests
import tempfile
import time
import datetime
import json
from bs4 import BeautifulSoup


class TPconnect(object):
    _obligatory_headers = {
        "Referer": "https://home.trainingpeaks.com/login"
    }
    _reauthAttempts = 1

    def __init__(self, username, password):
        self.username = username
        self.password = password
        rate_lock_path = tempfile.gettempdir() + "/tp_rate.localhost.lock"
        # Ensure the rate lock file exists (...the easy way)
        open(rate_lock_path, "a").close()
        self._rate_lock = open(rate_lock_path, "r+")

        self.session = None
        self.athlete_id = None

    def init(self):
        if self.session is None:
            self._get_session()
        if self.athlete_id is None:
            self.get_athlete()

    def get_athlete(self):
        """
            Get information from user
        """
        s = self.session.get('https://tpapi.trainingpeaks.com/users/v3/user')
        if s.status_code != 200:
            raise Exception("Cannot get user")
        athlete = s.json()
        self.athlete_id = athlete['user']['athletes'][0]['athleteId']

    def _request_with_reauth(self, req_lambda, email=None, password=None):
        for i in range(self._reauthAttempts + 1):
            session = self._get_session(email=email, password=password)
            self._rate_limit()
            result = req_lambda(session)
            if result.status_code not in (403, 500):
                return result
        return result

    def _rate_limit(self):
        min_period = 1
        self._rate_lock.seek(0)
        last_req_start = self._rate_lock.read()
        if not last_req_start:
            last_req_start = 0
        else:
            last_req_start = float(last_req_start)

        wait_time = max(0, min_period - (time.time() - last_req_start))
        time.sleep(wait_time)

        self._rate_lock.seek(0)
        self._rate_lock.write(str(time.time()))
        self._rate_lock.flush()

    def _get_session(self):
        """
            Get authentification session
        """
        session = requests.Session()
        params = {}
        preResp = session.get("https://home.trainingpeaks.com/login",
                              params=params)
        if preResp.status_code != 200:
            raise Exception("SSO prestart error %s %s" %
                            (preResp.status_code, preResp.text))

        soup = BeautifulSoup(preResp.text, features="html.parser")
        hidden_tag = soup.find_all("input", type="hidden")[0].attrs
        data = {
            "Username": self.username,
            "Password": self.password,
            hidden_tag['name']: hidden_tag['value']
        }
        ssoResp = session.post("https://home.trainingpeaks.com/login",
                               params=params,
                               data=data, allow_redirects=False)
        if ssoResp.status_code != 302 or "temporarily unavailable" \
                in ssoResp.text:
            raise Exception("TPLogin error %s %s" % (
                ssoResp.status_code, ssoResp.text))
        session.headers.update(self._obligatory_headers)

        self.session = session

    def upload_workout(self, workout_name, workout_structure, workout_time, date):
        """
            Upload workout

            workout_name : str
                name of the workout
            workout_structure : json
                structure of the workout
            workout_time : number
                duration of the workout
            date : str
                date of the workout
        """
        self.init()
        url = 'https://tpapi.trainingpeaks.com/fitness/v3/athletes/' + str(self.athlete_id) + '/workouts'
        payload = {"athleteId": str(self.athlete_id),
                   "structure": workout_structure,
                   "workoutId": 0,
                   "workoutTypeValueId": 2,
                   "title": str(workout_name),
                   "totalTimePlanned":  workout_time/3600,
                   "workoutDay": date
                   }
        resp = self.session.post(url, data=payload)
        if resp.status_code != 200:
            print(resp)


if __name__ == '__main__':
    pass
