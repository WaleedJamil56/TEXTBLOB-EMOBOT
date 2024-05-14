from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from textblob import TextBlob

class AnalyzeSentimentAction(Action):
    def name(self) -> Text:
        return "action_analyze_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        descriptions = ""
        for slot_name in ["first_description", "second_description", "third_description", "fourth_description", "fifth_description", "sixth_description"]:
            description = tracker.get_slot(slot_name)
            if description:
                descriptions += description + " "

        if descriptions:
            # Analyze sentiment using TextBlob
            sentiment = TextBlob(descriptions).sentiment

            # Get polarity score
            polarity = sentiment.polarity

            # Categorize sentiment as positive or negative based on polarity
            if polarity > 0:
                emotion = "POSITIVE"
            elif polarity < 0:
                emotion = "NEGATIVE"
            else:
                emotion = "NEUTRAL"

            if emotion == "POSITIVE":
                dispatcher.utter_message(
                    text="Your child's responses indicate a positive outlook. They seem to be in good spirits and engaging positively with the content."
                )
            elif emotion == "NEGATIVE":
                dispatcher.utter_message(
                    text="It may be helpful to pay attention to your child's emotional state. Their responses suggest they might be feeling a bit down or troubled. Offering support and attention could be beneficial."
                )
            else:
                dispatcher.utter_message(
                    text="The overall sentiment for the given descriptions could not be determined."
                )

        else:
            dispatcher.utter_message(text="No descriptions provided.")

        return []

class ResetSlotsAction(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Reset the values of the six description slots to None
        slots_to_reset = ["first_description", "second_description", "third_description", "fourth_description", "fifth_description", "sixth_description"]
        reset_events = [SlotSet(slot, None) for slot in slots_to_reset]

        return reset_events