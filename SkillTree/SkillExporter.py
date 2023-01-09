import sys

parent_module = sys.modules[".".join(__name__.split(".")[:-1]) or "__main__"]
if __name__ == "__main__" or parent_module.__name__ == "__main__":
    from DatabaseHandler import DatabaseHandler
else:
    from .DatabaseHandler import DatabaseHandler
    
class SkillExporter:
    def __init__(self, export: str = "data/export/") -> None:
        self.export = export
    
    def export_skills(self):
        import os
        db = DatabaseHandler()
        skills = db.get_data()
        
        for skill in skills:
            print(f"Writing skill: {skill}")
            message = ""
            with open(os.path.join(self.export, f"{skill.name}.md"), "w+") as file:
                if skill.prerequisite != "None":
                    prerequisites = skill.prerequisite.split(",")
                    prerequisites = [f"[[{prerequisite}]]" for prerequisite in prerequisites]
                    prerequisites = ", ".join(prerequisites)
                    message += f"Prerequisite(s): {prerequisites}\n\n"
                message += f"{skill.description}\n\n#Skill"
                file.write(message)

if __name__ == "__main__":
    se = SkillExporter()
    se.export_skills()