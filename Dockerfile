FROM python:3.10

WORKDIR /projects/PungeonBot/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3.10", "./PungeonBot.py" ]

