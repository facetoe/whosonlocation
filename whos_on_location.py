from collections import OrderedDict

__author__ = 'facetoe'
import requests
from bs4 import BeautifulSoup


class WhosOnLocation():
    email = None
    password = None
    session = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()

    def login(self):
        login_details = {'email_input': self.email,
                         'password_input': self.password,
                         '_redirect_url': '',
                         'continue_submit': 'Login'}
        r = self.session.post('https://login.whosonlocation.com/login', data=login_details)
        return r.url == 'https://au.whosonlocation.com/home?justloggedin=true'

    def get_status(self):
        r = self.session.get('https://au.whosonlocation.com/home?justloggedin=true')
        html = BeautifulSoup(r.content)
        status = html.body.find("span", {"class": "my-status-name"})
        if status:
            return status.text

    def on_site(self):
        return self.__change_status('onsite')

    def off_site(self):
        return self.__change_status('offsite')

    def __change_status(self, status):
        r = self.session.post('https://au.whosonlocation.com/ajax/changestatus', data={'status': status})
        return r.json()

    # _type can be org or location
    def search(self, keyword, _type='location'):
        payload = {'keyword': keyword, 'type': _type}
        r = self.session.get('https://au.whosonlocation.com/home/search', params=payload)
        return self.__parse_results(BeautifulSoup(r.content))

    @staticmethod
    def __parse_results(page):
        titles = ['Name', 'Title', 'Department', 'Current Location', 'Home Location']
        table = page.body.find_all("tr", {"class": "dataRow"})
        results = []
        for row in table:
            values = [v.string for v in row.findAll('td', {'class': 'truncate'})]
            results.append(OrderedDict(zip(titles, values)))
        return results






