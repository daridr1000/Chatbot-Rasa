from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import csv
import os


EXAMPLE_SCORING_SCHEME = {
    'introduction': 0.5,
    'concerns': 0.5,
    'injury_context': 0.5
}

print(os.getcwd())
with open('./personas/1_score.csv') as file:
    EXAMPLE_SCORING_SCHEME = {}
    for row in csv.reader(file, delimiter=','):
        EXAMPLE_SCORING_SCHEME[row[0]] = (float(row[1]), row[2])


print(EXAMPLE_SCORING_SCHEME)

MAX_SCORE = sum(map(lambda x: x[0], EXAMPLE_SCORING_SCHEME.values()))
SPACING = ' '

class PrintScore(Action):

    def name(self) -> Text:
        return "action_print_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # TODO: unclutter this method

        def filter_events(e):
            return e['event'] == 'user'

        def extract_intent(e):
            return e['parse_data']['intent']['name']

        intents = set(map(extract_intent, filter(
            filter_events, tracker.events)))

        # See what intents were missed by the user
        missed_intents = set(EXAMPLE_SCORING_SCHEME.keys()).difference(intents)

        output = []
        total_score = 0
        # loop over user intents and add the responses accordingly
        for intent in intents:
            if intent in EXAMPLE_SCORING_SCHEME:
                current_score, explanation = EXAMPLE_SCORING_SCHEME[intent]
                total_score += current_score
                output.append(
                    f"{explanation}{SPACING}({current_score}/{current_score})")

        # loop over intents that the user did not trigger

        for intent in missed_intents:
            score, explanation = EXAMPLE_SCORING_SCHEME[intent]
            output.append(f"{explanation}{SPACING}(0.0/{score})")

        # Separator and total score
        output.append('-' * 15)
        output.append(f"Total score:{SPACING}({float(total_score)}/{MAX_SCORE})")

        msg = "\n".join(output)
        dispatcher.utter_message(text=msg)
        return []
