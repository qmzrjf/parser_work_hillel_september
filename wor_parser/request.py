from time import sleep

import requests
from fake_useragent import UserAgent


class RequestEngine:

    def get_response(self, url: str, params: dict | None = None) -> requests.Response:
        user_agent = UserAgent()
        response = requests.get(url, params=params, headers={"User-Agent": user_agent.random})
        sleep(0.5)
        return response
