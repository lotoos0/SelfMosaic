# its about GUI :) 
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QInputDialog
from database import add_human, get_humans, update_human, initialize_db
from models import Human

class SelfMosaicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SelfMosaic')

        layout = QVBoxLayout()

        self.add_button = QPushButton('Add New Person', self)
        self.add_button.clicked.connect(self.add_new_person)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton('Edit Person', self)
        self.edit_button.clicked.connect(self.edit_person)
        layout.addWidget(self.edit_button)

        self.info_button = QPushButton('Show Information', self)
        self.info_button.clicked.connect(self.show_information)
        layout.addWidget(self.info_button)

        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def add_new_person(self):
        name, ok = QInputDialog.getText(self, 'Input', 'Enter name:')
        if not ok or not name:
            return

        age, ok = QInputDialog.getInt(self, 'Input', 'Enter age:')
        if not ok:
            return

        traits = {}
        while True:
            trait, ok = QInputDialog.getText(self, 'Input', 'Enter trait (Leave empty to finish):')
            if not ok or not trait:
                break
            value, ok = QInputDialog.getText(self, 'Input', f'Enter value for trait "{trait}":')
            if not ok:
                break
            traits[trait] = value

        habits = {}
        while True:
            habit, ok = QInputDialog.getText(self, 'Input', 'Enter habit (Leave empty to finish):')
            if not ok or not habit:
                break
            description, ok = QInputDialog.getText(self, 'Input', f'Enter description for habit "{habit}":')
            if not ok:
                break
            habits[habit] = description

        hobbies, ok = QInputDialog.getText(self, 'Input', 'Enter hobbies (comma separated):')
        hobbies_list = [h.strip() for h in hobbies.split(',')] if ok and hobbies else []

        human = Human(name, age, traits, habits, hobbies_list)
        add_human(human)

        QMessageBox.information(self, 'Success', 'New person added successfully!')

    def edit_person(self):
        humans = get_humans()
        if not humans:
            QMessageBox.information(self, 'Info', 'No persons available to edit.')
            return

        names = [human.name for human in humans]
        name, ok = QInputDialog.getItem(self, 'Select', 'Select person to edit:', names, 0, False)
        if not ok or not name:
            return

        # Fetch the selected person
        selected_human = next((human for human in humans if human.name == name), None)
        if not selected_human:
            QMessageBox.warning(self, 'Error', 'Person not found.')
            return

        # Edit age
        age, ok = QInputDialog.getInt(self, 'Input', f'Enter new age for {name}:', selected_human.age)
        if not ok:
            return

        # Edit traits
        traits = selected_human.traits.copy()
        while True:
            trait, ok = QInputDialog.getText(self, 'Input', 'Enter trait to edit (Leave empty to finish):')
            if not ok or not trait:
                break
            if trait in traits:
                value, ok = QInputDialog.getText(self, 'Input', f'Enter new value for trait "{trait}":', traits[trait])
                if ok:
                    traits[trait] = value
            else:
                QMessageBox.warning(self, 'Warning', f'Trait "{trait}" does not exist.')

        # Edit habits
        habits = selected_human.habits.copy()
        while True:
            habit, ok = QInputDialog.getText(self, 'Input', 'Enter habit to edit (Leave empty to finish):')
            if not ok or not habit:
                break
            if habit in habits:
                description, ok = QInputDialog.getText(self, 'Input', f'Enter new description for habit "{habit}":', habits[habit])
                if ok:
                    habits[habit] = description
            else:
                QMessageBox.warning(self, 'Warning', f'Habit "{habit}" does not exist.')

        # Edit hobbies
        hobbies, ok = QInputDialog.getText(self, 'Input', f'Enter new hobbies for {name} (comma separated):', ', '.join(selected_human.hobbies))
        hobbies_list = [h.strip() for h in hobbies.split(',')] if ok and hobbies else selected_human.hobbies

        # Update the person
        update_human(name, age, traits, habits, hobbies_list)
        QMessageBox.information(self, 'Success', 'Person updated successfully!')

    def show_information(self):
        humans = get_humans()
        if not humans:
            QMessageBox.information(self, 'Info', 'No data available.')
            return

        info = ""
        for human in humans:
            info += human.display_info() + "\n" + "-"*40 + "\n"

        QMessageBox.information(self, 'Information', info)

def main():
    initialize_db()
    app = QApplication(sys.argv)
    ex = SelfMosaicApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

