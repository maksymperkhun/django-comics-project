import requests


class NetworkHelper:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

    def get_list(self):
        response = requests.get(self.base_url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        return []

    def delete_item(self, item_id):
        url = f"{self.base_url}{item_id}/"
        response = requests.delete(url, auth=self.auth)
        return response.status_code == 204
