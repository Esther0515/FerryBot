# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import openai
from datetime import datetime, timedelta

openai.api_key = ''
def parse_day_to_iso(day):

    prompt = f"Convert '{day} ti tge bext occurrence as an ISO format date and hour (YYYY-MM-DDTHH). Today is{datetime.now().strftime('%Y-%m-%d')}'"
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt,
        max_tokens=60
    )
    date_string = response.choice[0].text.strip()
    date_obj = datetime.fromisoformat(date_string)
    return date_obj.strftime('%Y-%m-%dT%H')

conn = sqlite3.connect("my.db")
# create table
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    name VARCHAR(100) 
)
""")


def insert_problem(data, name):
    cursor.execute('INSERT INTO problems (data, name) values (?, ?)', (data, name))
    conn.commit()
    print(f"data SAVE INTO DB")


class ActionSaveUserIssue(Action):

    def name(self) -> Text:
        return "action_save_user_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_issue = tracker.latest_message.get('text')
        name = tracker.get_slot('name')
        insert_problem(user_issue, name)
        return []
class ActionPareseTime(Action):

    def name(self) -> Text:
        return "action_parse_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        confirm_time = tracker.get_slot("confirm_time")
        print(confirm_time)
        if openai.api_key:
            date = parse_day_to_iso(confirm_time)
        else:
            date = confirm_time
        dispatcher.utter_message(f"We will hold an event on {date} and look forward to meeting you")
        return []
