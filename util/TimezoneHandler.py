import aiofiles
import json
from datetime import datetime
import pytz

class AsyncTimezoneHandler():
    def __init__(self) -> None:
        self.path = '.secrets/users.json'

    async def add_user(self, user_id: str, timezone: str):
        async with aiofiles.open(self.path, 'r') as file:
            data = json.loads(await file.read())
        
        data[user_id] = timezone
        
        async with aiofiles.open(self.path, 'w') as file:
            await file.write(json.dumps(data))
    
    async def read_user(self, user_id: str):
        async with aiofiles.open(self.path, 'r') as file:
            data = json.loads(await file.read())
        
        try:
            return data[user_id]
        except Exception as e:
            return e
    
    def date_from_string(self, dt_string: str, timezone: str):
        try:
            if len(dt_string) > 16:
                dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
            dt = pytz.timezone(timezone).localize(dt)
        except Exception as e:
            return e
        return dt
    
    async def get_local_datetime_all(self, dt: datetime, user: str):
        async with aiofiles.open(self.path, 'r') as file:
            data = json.loads(await file.read())
        
        try: 
            res = []
            for usr, tz in data.items():
                if usr == user:
                    continue
                res.append({usr: dt.astimezone(pytz.timezone(tz))})
            
            return res
        except Exception as e:
            return e

