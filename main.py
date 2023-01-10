from SkillTree import *
import os
import configparser               

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))

def update_databases():
    db = DatabaseHandler()
    db.update_data()
    del db
    
def export_skill_files(directory = None):
    if directory is None:
        se = SkillExporter()
    else:
        se = SkillExporter(directory)
    se.export_skills()

def visualize():
    db = DatabaseHandler()
    db.get_data()
    del db
    
    vm = VisualizationHandler()
    vm.show_tree()
    
if __name__ == "__main__":
    if config["DEFAULT"].getboolean("UPDATE_DATABASES"):
        update_databases()
    if config["DEFAULT"].getboolean("EXPORT_SKILL_FILES"):
        export_skill_files("D:/Obsidian/Strixhaven Campaign Planning/Skills/")
        import shutil
        shutil.copyfile("data/Skills.csv", "D:/Github/SkillRepository/Skills.csv")
    if config["DEFAULT"].getboolean("VISUALIZE"):
        visualize()