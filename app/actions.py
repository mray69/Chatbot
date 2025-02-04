import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import date

current_date = date.today()

class ActionFindTrains(Action):
    def name(self) -> Text:
        return "action_find_trains"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_station = tracker.get_slot("from_station")
        to_station = tracker.get_slot("to_station")
        journey_date = current_date

        if not from_station or not to_station:
            dispatcher.utter_message(text="Please provide both departure and arrival station codes.")
            return []

        #dispatcher.utter_message(text=f"Searching for trains from {from_station.upper()} to {to_station.upper()} on {journey_date}...")

        url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
        querystring = {"fromStationCode": from_station.upper(), "toStationCode": to_station.upper(), "dateOfJourney": str(journey_date)}
        headers = {
            "x-rapidapi-key": "69e1ae6593mshb586ed58ba9d655p1a60b2jsn2268ab531e5d",
            "x-rapidapi-host": "irctc1.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            if data.get("data"):
                train_details = f"<div class='train-details'><h3>Trains from {from_station.upper()} to {to_station.upper()} on {journey_date}:</h3><ul>"

                for train in data["data"][:10]:
                    train_details += (
                        f"<li><strong>Train:</strong> {train['train_name']} ({train['train_number']})<br>"
                        f"<strong>Departure:</strong> {train['from_std']}<br>"
                        f"<strong>Arrival:</strong> {train['from_sta']}</li>"
                    )

                train_details += "</ul></div>"
                dispatcher.utter_message(text=train_details)

            else:
                dispatcher.utter_message(
                    text=f"<div class='train-details'><p>No trains found from {from_station.upper()} to {to_station.upper()} on {journey_date}.</p></div>"
                )

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="<div class='error-message'><p>Unable to fetch train data. Please try again later.</p></div>")
            print(f"API Error: {e}")

        return []
