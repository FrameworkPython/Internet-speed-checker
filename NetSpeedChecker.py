import requests
import speedtest
from tabulate import tabulate
from termcolor import colored

class InternetSpeedChecker:

    def __init__(self):
        self.st = speedtest.Speedtest()
        self.ip = requests.get('https://api.ipify.org').text
        self.location = requests.get(f'http://ip-api.com/json/{self.ip}').json()
        self.server = self.st.get_best_server()

    def get_ping(self):
        return self.st.results.ping

    def get_upload_speed(self):
        total = 0
        for i in range(3):
            total += self.st.upload()
        return total / 3

    def get_download_speed(self):
        total = 0
        for i in range(3):
            total += self.st.download()
        return total / 3

    def get_location(self):
        return {'country': self.location['country'], 'city': self.location['city']}

    def __repr__(self):
        return f'InternetSpeedChecker(ip={self.ip})'

    def __str__(self):
        data = [
            ['Ping (ms)', colored(self.get_ping(), self.get_ping_color(self.get_ping()))],
            ['Upload (Mbps)', colored(self.get_upload_speed() / 1024 / 1024, self.get_upload_color(self.get_upload_speed()))],
            ['Download (Mbps)', colored(self.get_download_speed() / 1024 / 1024, self.get_download_color(self.get_download_speed()))],
            ['Country', self.get_location()['country']],
            ['City', self.get_location()['city']]
        ]
        table = tabulate(data, headers=['Title', 'Value'], tablefmt='pretty', numalign='right', stralign='right')
        return table

    def get_ping_color(self, ping):
        if ping > 100:
            return 'red'
        elif ping > 50:
            return 'yellow'
        else:
            return 'green'

    def get_upload_color(self, upload_speed):
        if upload_speed < 10 * 1024 * 1024:
            return 'red'
        elif upload_speed < 50 * 1024 * 1024:
            return 'yellow'
        else:
            return 'green'

    def get_download_color(self, download_speed):
        if download_speed < 10 * 1024 * 1024:
            return 'red'
        elif download_speed < 50 * 1024 * 1024:
            return 'yellow'
        else:
            return 'green'

if __name__ == '__main__':
    isc = InternetSpeedChecker()
    print(isc)
