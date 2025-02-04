from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionFindTrains(Action):
    def name(self) -> Text:
        return "action_find_trains"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_station = tracker.get_slot("from_station")
        to_station = tracker.get_slot("to_station")

        # Replace with your Railway API key
        api_key = "your_api_key_here"

        # URL for the Railway API to fetch train details
        url = f"http://api.railwayapi.com/v2/arrivals/train/{from_station}/station/{to_station}/apikey/{api_key}/"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx/5xx errors
            data = response.json()

            if data.get('response_code') == 200 and 'train' in data:
                trains = data['train']
                if trains:
                    response_text = f"<div class='train-details'><h3>Trains from {from_station} to {to_station}:</h3><ul>"
                    for train in trains:
                        response_text += f"<li><strong>Train:</strong> {train['train']['name']}<br><strong>Arrival:</strong> {train['train']['arrival_time']}<br><strong>Departure:</strong> {train['train']['departure_time']}</li>"
                    response_text += "</ul></div>"
                else:
                    response_text = f"<div class='train-details'><p>No trains found from {from_station} to {to_station}.</p></div>"
            else:
                response_text = f"<div class='train-details'><p>Error: No train data available.</p></div>"

        except requests.exceptions.RequestException as e:
            response_text = f"<div class='train-details'><p>Error: Unable to fetch train data. Please try again later.</p></div>"
            print(f"Error: {e}")

        dispatcher.utter_message(text=response_text)
        return []
