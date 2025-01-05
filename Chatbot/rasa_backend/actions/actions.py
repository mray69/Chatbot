# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import json

# Load train and bus data from JSON file
with open('train_data.json', 'r') as f:
    transport_data = json.load(f)

class ActionProvideTrainDetails(Action):
    def name(self) -> str:
        return "action_provide_train_details"

    def run(self, dispatcher, tracker, domain):
        from_station = tracker.get_slot("from_station")
        to_station = tracker.get_slot("to_station")

        # Check if the slots are provided
        if not from_station or not to_station:
            dispatcher.utter_message("Please provide both departure and arrival stations.")
            return []

        # Find matching train details
        for station in transport_data['stations']:
            if station['station_name'].lower() == from_station.lower():
                for train in station['train_details']:
                    if to_station.lower() in train['route'].lower():
                        dispatcher.utter_message(
                            f"Train {train['train_no']} departs from {from_station} at {train['departure_time']} and arrives at {train['arrival_time']}."
                        )
                        return []

        dispatcher.utter_message(f"No trains found from {from_station} to {to_station}.")
        return []
