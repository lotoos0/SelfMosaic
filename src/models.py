# Define model classes

class Human:
    def __init__(self, name, age, traits=None, habits=None, hobbies=None):
        self.name = name
        self.age = age
        self.traits = traits or {}
        self.habits = habits or {}
        self.hobbies = hobbies or []

    def display_info(self):
        info = f"Name: {self.name}\nAge: {self.age}\n"
        info += "Traits:\n"
        for trait, value in self.traits.items():
            info += f" - {trait}: {value}\n"
        info += "Habits:\n"
        for habit, description in self.habits.items():
            info += f" - {habit}: {description}\n"
        info += f"Hobbies: {', '.join(self.hobbies)}\n"
        return info

    def add_trait(self, trait, value):
        self.traits[trait] = value

    def add_habbit(self, habit, description):
        self.habits[habit] = description

    def add_hobby(self, hobby):
        self.hobbies.append(hobby)

