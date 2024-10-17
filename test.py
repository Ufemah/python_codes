import pandas as pd
import asyncio
import aiohttp
from async_timeout import timeout
import json

data = {'Name': {0: 'Alice', 1: 'Bob', 2: 'Charlie', 3: 'David',
                 4: 'Eve', 5: 'Frank', 6: 'Grace', 7: 'Henry'},

        'Age': {0: 25, 1: 30, 2: 35, 3: 40, 4: 45, 5: 50, 6: 55, 7: 60},

        'Gender': {0: 'Female', 1: 'Male', 2: 'Male', 3: 'Male',
                   4: 'Female', 5: 'Male', 6: 'Female', 7: 'Male'},

        'City': {0: 'New York', 1: 'Los Angeles', 2: 'Chicago',
                 3: 'Houston', 4: 'Phoenix', 5: 'Philadelphia',
                 6: 'San Francisco', 7: 'Seattle'}}

df = pd.DataFrame.from_dict(data)

df = pd.concat([df, df, df, df]).reset_index(drop=True)


class Test:
    def __init__(self, df):
        self.df = df
        self.url = "https://google.com/"

    def create_payload(self, df_row):
        payload = {
            "events": [
                {
                    "name": "test"
                }
            ]
        }

        return payload

    async def gather_requests(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
            tasks = []
            batch_size = 3
            for index, row in self.df.iterrows():
                payload = self.create_payload(row)
                tasks.append(self.send_request(session, payload))
                if index % batch_size == 0:
                    await asyncio.gather(*tasks)
                    tasks = []
                    print(f"sent {index} events")
            if tasks:  # Gather remaining tasks
                await asyncio.gather(*tasks)
                print(f"sent all {self.df.shape[0]} events")

    async def send_request(self, session, payload):
        async with timeout(60):
            async with session.post(self.url, data=json.dumps(payload)) as response:
                await asyncio.sleep(1)

    def main(self):  # Changed to async
        if asyncio.get_running_loop() is None:
            print("attempt to push the audiences")
            task = asyncio.run(self.gather_requests())  # Await gather_requests
            print("executed with .run")
        else:
            task = asyncio.create_task(self.gather_requests())
            print("executed with .create_task")


if __name__ == "__main__":
    Test(df).main()
