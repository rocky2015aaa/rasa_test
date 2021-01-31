# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Text, Dict, Any, List

from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.events import (
    SlotSet,
    AllSlotsReset,
    ConversationPaused,
    ConversationResumed,
    FollowupAction,
    UserUtteranceReverted,
)
import requests
import json
from random import randint
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

class ActionTalkToUser(Action):
    def name(self) -> Text:
        return "action_talk_to_user"

    def run(self, dispatcher, tracker: Tracker, domain):
        message = ""
        while message == "":
            url = "http://127.0.0.1:5000/handoff/123"
            req = requests.get(url)
            resp = json.loads(req.text)
            if "error" in resp:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            message = resp["message"]
        dispatcher.utter_message("Human agent: {}".format(message))
        return [FollowupAction('livechat_form')]


class ActionToHumanAgent(Action):
    def name(self) -> Text:
        return "action_talk_to_human_agent"

    def run(self, dispatcher, tracker: Tracker, domain):
        message = ""
        while message == "":
            message = tracker.latest_message['text']
            if message == "/exit":
                return [SlotSet("user_message", None), FollowupAction("utter_goodbye")]
            url = "http://127.0.0.1:5000/handoff/456"
            data = {'message': message}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            req = requests.post(url, data=json.dumps(data), headers=headers)
            resp = json.loads(req.text)
            if "error" in resp:
                raise Exception("Error fetching message: " + repr(resp["error"]))
        return [SlotSet("user_message", None), FollowupAction("action_talk_to_user")]
