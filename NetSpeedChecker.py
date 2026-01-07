import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict

import httpx


class InternetSpeedChecker:
    def __init__(self):
        self.client = httpx.AsyncClient(http2=True, timeout=15.0)
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._speedtest_instance = None

    async def prepare_speedtest(self):
        loop = asyncio.get_running_loop()
        self._speedtest_instance = await loop.run_in_executor(
            self.executor, self._create_speedtest
        )

    def _create_speedtest(self):
        from speedtest import Speedtest
        st = Speedtest()
        st.get_best_server()
        return st

    async def get_ip(self):
        r = await self.client.get("https://api.ipify.org")
        return r.text.strip()

    async def get_location(self, ip: str):
        r = await self.client.get(f"http://ip-api.com/json/{ip}")
        return r.json()

    def _sync_measure(self):
        st = self._speedtest_instance
        dl = st.download()
        ul = st.upload()
        return st.results.ping, dl, ul

    async def measure_speed(self):
        loop = asyncio.get_running_loop()
        ping, dl, ul = await loop.run_in_executor(self.executor, self._sync_measure)
        return ping, dl, ul

    async def to_string(self, fmt: str = "json") -> str:
        await self.prepare_speedtest()
        ip_task = self.get_ip()
        speed_task = self.measure_speed()
        ip, (ping, dl, ul) = await asyncio.gather(ip_task, speed_task)
        loc = await self.get_location(ip)

        data = {
            "Ping (ms)": round(ping, 2),
            "Upload (Mbps)": round(ul / 1_000_000, 2),
            "Download (Mbps)": round(dl / 1_000_000, 2),
            "Country": loc.get("country", "N/A"),
            "City": loc.get("city", "N/A"),
        }

        if fmt == "json":
            return json.dumps(data, indent=4, ensure_ascii=False)
        else:
            from tabulate import tabulate
            rows = [[k, v] for k, v in data.items()]
            return tabulate(rows, headers=["Title", "Value"], tablefmt="plain", numalign="right")

    async def close(self):
        await self.client.aclose()
        self.executor.shutdown(wait=False)


async def main():
    checker = InternetSpeedChecker()
    result = await checker.to_string("json")
    print(result)
    await checker.close()


asyncio.run(main())
