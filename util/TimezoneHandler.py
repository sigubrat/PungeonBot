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
        
        print(f"Read: {data[user_id]} from {data}")
        try:
            return data[user_id]
        except Exception as e:
            print("Shit's fucked on line 27")
            return e
    
    def date_from_string(dt_string: str, timezone: str):
        print(f"date_from_time({dt_string}, {timezone})")
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            dt = pytz.timezone(timezone).localize(dt)
        except Exception as e:
            print("Shit's fucked on line 36")
            return e
        return dt
    
    async def get_local_datetime_all(self, dt: datetime):
        async with aiofiles.open(self.path, 'r') as file:
            data = json.loads(await file.read())
        
        try: 
            res = []
            for key, value in data.items():
                res.append({key: pytz.timezone(value).localize(dt)})
            
            return res
        except Exception as e:
            return e

