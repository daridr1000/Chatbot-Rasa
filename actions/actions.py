# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


EXAMPLE_SCORING_SCHEME = {
    'introduction': 0.5,
    'concerns': 0.5,
    'injury_context': 0.5
}

MAX_SCORE = sum(EXAMPLE_SCORING_SCHEME.values())


class PrintScore(Action):

    def name(self) -> Text:
        return "action_print_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # TODO: unclutter this method
        # TODO: load scoring scheme dynamically (json)

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
                current_score = EXAMPLE_SCORING_SCHEME[intent]
                total_score += current_score
                output.append(f"{intent}\t\t{current_score}/{current_score}")

        # loop over intents that the user did not trigger
        for intent in missed_intents:
            output.append(f"{intent}\t\t0.0/{EXAMPLE_SCORING_SCHEME[intent]}")

        # Separator and total score
        output.append('-' * 15)
        output.append(f"Total score: \t\t{total_score}/{MAX_SCORE}")

        msg = "\n".join(output)
        dispatcher.utter_message(text=msg)
        return []
