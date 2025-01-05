from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import json

class ActionFindTrains(Action):
    def name(self) -> Text:
        return "action_find_trains"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from_station = tracker.get_slot("from_station")
        to_station = tracker.get_slot("to_station")

        # Update the path to the train_data.json file
        file_path = r'C:\Users\svkur\Desktop\Newchatbot\rasa_backend\actions\train_data.json'

        try:
            with open(file_path) as f:
                train_data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: train_data.json file not found.")
            return []

        trains = train_data.get(from_station, {}).get(to_station, [])

        if trains:
            response = f"<div class='train-details'><h3>Trains from {from_station} to {to_station}:</h3><ul>"
            for train in trains:
                response += f"<li><strong>Train:</strong> {train['name']}<br><strong>Arrival:</strong> {train['arrival']}<br><strong>Departure:</strong> {train['departure']}</li>"
            response += "</ul></div>"
        else:
            response = f"<div class='train-details'><p>No trains found from {from_station} to {to_station}.</p></div>"

        dispatcher.utter_message(text=response)
        return []
