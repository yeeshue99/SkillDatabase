from __future__ import annotations

class Skill:    
    def __init__(self, data:dict = None) -> Skill:
        if not data:
            return
        self.name = data['name']
        self.archetype = data['archetype']
        self.prerequisite = data['prerequisite']
        self.casting_time = data['casting_time']
        self.range = data['range']
        self.duration = data['duration']
        self.uses = data['uses']
        self.has_active = data['has_active']
        self.has_passive = data['has_passive']
        self.description = data['description']
        
    def import_data(self, data: tuple[str]) -> Skill:
        self.name = data[0]
        self.archetype = data[1]
        self.prerequisite = data[2]
        self.casting_time = data[3]
        self.range = data[4]
        self.duration = data[5]
        self.uses = data[6]
        self.has_active = data[7]
        self.has_passive = data[8]
        self.description = data[9]
        
        return self
        
    def export(self) -> tuple[str]:
        return (self.name, self.archetype, self.prerequisite, self.casting_time, self.range, self.duration, self.uses, self.has_active, self.has_passive, self.description)
    
    def __repr__(self): 
        return self.name
    
    def __str__(self): 
        return self.name