import json

class ConfigHandler():
    def __init__(self) -> None:
        self.path = '.secrets/config.json'
        self.load()
    
    def load(self):
        with open(self.path, 'r') as f:
            self.config = json.load(f)
    
    def get_token(self):
        try:
            return self.config['token']
        except Exception as e:
            return e
    
    def get_guild_id(self):
        try:
            return self.config['guild']
        except Exception as e:
            return e
        