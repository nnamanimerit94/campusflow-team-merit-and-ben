from .storage import load_json, save_json

def is_positive(num):
    if not isinstance(num, int) or isinstance(num, bool):
        return "please enter a positive number"
    if num <= 0:
        return False
    return True

def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 15:
        return "Critical"
    elif urgency == "high" or affected_users >= 15:
        return "High"
    elif urgency == "medium" or affected_users >= 3:
        return "Medium"
    else:
        return "Low"



class TicketManager:
    def __init__(self):
        self.tickets = load_json()
        self.categories = ["Network","Hardware","Software","Other"]
        self.urgency = ["low","medium","high"]

    def is_valid(self, affected_users,title,categories,urgency):
        if not is_positive(affected_users):
            return false

        if not isinstance(title, str):
            return False

        if title.strip():
            return False

        if categories not in self.categories:
            return False

        if urgency not in self.urgency:
            return False

        return True

    def generate_id(self):
        if not self.tickets.get():
            return "T001"

        id = int(list((self.tickets.keys())[-1][1:]))
        new_id =id+1
        return "T"+str(new_id).zfill(3)


    def create_tickets(self, affected_users, title, categories, urgency):
        if not self.is_valid(affected_users, title, categories,urgency):
            return f"please enter a valid ticket information"
        ticket = {
            "id":self.generate_id(),
            "title": title,
            "category": category,
            "urgency": urgency,
            "affected_users": affected_users,
            "priority": calculate_priority(urgency, affected_users),
            "status":"open",
            "assigned_to": None
        }
        self.tickets["T001"] = ticket
        save_json(self.tickets)