import csv
import sys

parent_module = sys.modules[".".join(__name__.split(".")[:-1]) or "__main__"]
if __name__ == "__main__" or parent_module.__name__ == "__main__":
    from Skill import Skill
else:
    from .Skill import Skill

class CSVHandler:
    def load_skills_from_csv(filename="data/Skills.csv", raw = False) -> list[Skill]:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            skills = []
            for row in reader:
                if raw:
                    skills.append(row)
                else:
                    skills.append(Skill(row))
        return skills

if __name__ == '__main__':
    print(CSVHandler.load_skills_from_csv("data/Skills.csv"))