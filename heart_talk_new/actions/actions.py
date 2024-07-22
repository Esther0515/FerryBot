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

conn = sqlite3.connect("my.db")
# create table
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT
)
""")


def insert_problem(data):
    cursor.execute('INSERT INTO problems (data) values (?)', (data,))
    conn.commit()
    print(f"data SAVE INTO DB")


class ActionSaveUserIssue(Action):

    def name(self) -> Text:
        return "action_save_user_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_issue = tracker.latest_message.get('text')
        insert_problem(user_issue)
        return []
