import sys
import pandas as pd

from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow, QTextEdit, QHBoxLayout, QWidget

parent_module = sys.modules[".".join(__name__.split(".")[:-1]) or "__main__"]
if __name__ == "__main__" or parent_module.__name__ == "__main__":
    from DatabaseHandler import DatabaseHandler
    from CSVHandler import CSVHandler
else:
    from .DatabaseHandler import DatabaseHandler
    from .CSVHandler import CSVHandler
    
class VisualizationHandler:
    def __init__(self) -> None:
        db = DatabaseHandler()
        skills = db.get_data(raw = True)
        headers = db.get_headers()
        del db
        self.skills = pd.DataFrame(skills, columns=headers)
    
    def create_tree_widget(self, headers):
        tree_widget = QTreeWidget()
        
        tree_widget.setHeaderLabels(headers)
        tree_widget.setSortingEnabled(True)
        
        return tree_widget
    
    def create_text_widget(self):
        text_edit = QTextEdit()
        
        text_edit.setReadOnly(True)
        
        return text_edit
        
    def populate_paths(self, path_tree):
        for path in self.skills.archetype.unique():
            item = QTreeWidgetItem([path])
            path_tree.addTopLevelItem(item)
    
    def set_skills(self, path):
        self.skill_tree.clear()
        self.text_edit.clear()
        df = self.skills[self.skills['archetype'] == path]
        for _, skill in df.iterrows():
            item = QTreeWidgetItem([skill["name"], skill["prerequisite"]])
            
            if skill["prerequisite"] != "None":
                prerequisites = skill["prerequisite"].split(",")
                for prerequisite in prerequisites:
                    child = QTreeWidgetItem([prerequisite])
                    item.addChild(child)
            self.skill_tree.addTopLevelItem(item)
    
    def show_tree(self) -> None:
        app = QApplication(sys.argv)

        window = QMainWindow()

        # Create a horizontal layout to hold the tree widget and text edit
        layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        window.setCentralWidget(central_widget)

        # Create tree widget for paths
        self.path_tree = self.create_tree_widget(["Archetypes"])
        layout.addWidget(self.path_tree)

        # Create tree widget for skills
        self.skill_tree = self.create_tree_widget(['Skill', 'Prerequisites'])
        layout.addWidget(self.skill_tree)
        
        # Create a text edit and add it to the layout
        self.text_edit = self.create_text_widget()
        layout.addWidget(self.text_edit)
        
        # Populate paths
        self.populate_paths(self.path_tree)

        # Define a slot function to handle the itemClicked signal
        def on_skill_clicked(item, column):
            # Get the text of the clicked item
            text = item.text(column)
            if text == "Draconic Cry" or text == "None":
                message = f"{text} is not defined."
                self.text_edit.setText(message)
                return
            message = ""
            skill = self.skills[self.skills['name'] == text].iloc[0]
            for key in self.skills.columns:
                value = skill[key]
                if key == 'name':  # Skip the name, which has already been drawn
                    message += f"{value}\n"
                    continue
                message += f'{key.capitalize()}: {value}\n'  # Format the text as "key: value"
                
                self.text_edit.setText(message)
                
        # Define a slot function to handle the itemClicked signal
        def on_path_clicked(item, column):
            # Get the text of the clicked item
            text = item.text(column)
            self.set_skills(text)

        # Connect the itemClicked signal to the on_item_clicked slot
        self.skill_tree.itemClicked.connect(on_skill_clicked)
        self.path_tree.itemClicked.connect(on_path_clicked)   
            
        window.show()
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    visualizer = VisualizationHandler()
    visualizer.show_tree()