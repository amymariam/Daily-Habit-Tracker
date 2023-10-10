from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class LogHabit(Action):
    def name(self) -> Text:
        return "action_create_habit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        habit = tracker.latest_message['text']
        with open("habits.txt", "a") as file:
            while True:
                habit = input("Enter a habit (type 'STOP' to finish): ")
                if habit.upper() == "STOP":
                    break
                file.write(habit + "\n")
        response = "Habits logged."
        dispatcher.utter_message(text=response)
        return []

class ActionRemindHabit(Action):
    def name(self) -> Text:
        return "action_remind_habit"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        habit_to_remind = tracker.latest_message['text']
        with open("habits.txt", "r") as file:
            habits = file.readlines()
            found = False
            for habit in habits:
                if habit.strip() == habit_to_remind:
                    found = True
                    response=f"Reminder: Don't forget to do your '{habit_to_remind}' today!"
                    break
            if not found:
                response=f"No habit named '{habit_to_remind}' found in your list."
            dispatcher.utter_message(text=response)
            return []

class ActionListHabits(Action):
    def name(self) -> Text:
        return "action_list_habits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Your logic to retrieve and list user's habits goes here
        
        response = f"Here are your tracked habits:\n"
        with open("habits.txt", "r") as file:
            habits = file.readlines()
            for habit in habits:
                print("- " + habit.strip())
        dispatcher.utter_message(text=response)
        return []

class ActionProvideHelp(Action):
    def name(self) -> Text:
        return "action_provide_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = "Sure! I can help you with tracking habits, reminding you, and providing a list of habits. If you want to delete a habit, just let me know."
        dispatcher.utter_message(text=response)
        return []

# Define other custom actions here based on your use case
class ActionMarkDone(Action):
    def name(self) -> Text:
        return "action_track_habit"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        habit_to_mark = tracker.latest_message['text']
        with open("habits.txt", "r") as file:
            habits = file.readlines()
        with open("habits.txt", "w") as file:
            for h in habits:
                if h.strip() == habit_to_mark:
                    file.write(h.strip() + " (Done)\n")
                else:
                    file.write(h)
   
        response = f"Habit '{habit_to_mark}' marked as done. Great job!"
        dispatcher.utter_message(text=response)
        return []
        
class ActionDelete(Action):
    def name(self) -> Text:
        return "action_delete_habit"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open("habits.txt", "r") as file:
            habits = file.readlines()
        with open("habits.txt", "w") as file:
            for habit in habits:
                if "(Done)" not in habit:
                    file.write(habit)
        response = "Habit deleted."
        dispatcher.utter_message(text=response)
        return []

