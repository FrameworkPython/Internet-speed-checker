import httpx
import speedtest
from tabulate import tabulate
import json
import asyncio

class InternetSpeedChecker:

    def __init__(self):
        self.st = speedtest.Speedtest()
        self.client = httpx.AsyncClient(http2=True)

    async def get_ip(self):
        return await self.get_response_text('https://api.ipify.org')

    async def get_location(self, ip):
        return await self.get_response_json(f'http://ip-api.com/json/{ip}')

    async def get_response_text(self, url):
        response = await self.client.get(url)
        return response.text

    async def get_response_json(self, url):
        response = await self.client.get(url)
        return response.json()

    async def get_ping(self):
        return self.st.results.ping

    async def get_upload_speed(self):
        return await self.get_average_speed(self.st.upload)

    async def get_download_speed(self):
        return await self.get_average_speed(self.st.download)

    async def get_average_speed(self, method):
        total = 0
        for _ in range(3):
            total += method()
        return total / 3

    async def to_string(self, format='json'):
        ip = await self.get_ip()
        location = await self.get_location(ip)
        data = {
            'Ping (ms)': await self.get_ping(),
            'Upload (Mbps)': await self.get_upload_speed() / 1024 / 1024,
            'Download (Mbps)': await self.get_download_speed() / 1024 / 1024,
            'Country': location['country'],
            'City': location['city']
        }
        if format == 'json':
            return json.dumps(data, indent=4)
        elif format == 'table':
            table_data = [[k, v] for k, v in data.items()]
            return tabulate(table_data, headers=['Title', 'Value'], tablefmt='pretty', numalign='right', stralign='right')

    async def close(self):
        await self.client.aclose()

async def main():
    isc = InternetSpeedChecker()
    result = await isc.to_string(format='json') 
    print(result)
    await isc.close()

asyncio.run(main())
