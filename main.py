from SkillTree import *
                                   
UPDATE_DATABASES = True
EXPORT_SKILL_FILES = True
VISUALIZE = False


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
    if UPDATE_DATABASES:
        update_databases()
    if EXPORT_SKILL_FILES:
        export_skill_files("D:/Obsidian/Strixhaven Campaign Planning/Skills/")
        import shutil
        shutil.copyfile("data/Skills.csv", "skill-tree/public/Skills.csv")
    if VISUALIZE:
        visualize()