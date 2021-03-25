import email
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.utils import formatdate

import requests
import smtplib, ssl

from config import ITEM_RELISTED_INTERVAL


class TooGoodToGo:
    def __init__(self, url, data, headers):
        self.url = url
        self.data = data
        self.headers = headers
        self.seen = {}

    def get_items_matching(self, queries):
        """
        Finds all items matching keyword.
        Returns an array of items, which might be empty.
        Throws HTTPError if there are network issues.
        """
        items = self.__query_server()
        items = self.__filter_items_by_queries(items, queries)
        items = self.__filter_by_last_time_seen(items, datetime.now())
        return items

    def __query_server(self):
        """
        Queries TooGoodToGo server and gets a list of all available items nearby.
        Returns the response as a dictionary.
        Raises an exception if invalid response.
        """
        response = requests.post(self.url, json=self.data, headers=self.headers)
        response.raise_for_status()
        response_json = response.json()
        return list(map(self.__make_item_from_json, response_json['items']))

    def __make_item_from_json(self, item_json):
        id = item_json['item']['item_id']
        name = item_json['item']['name']
        store = item_json['display_name']
        distance = item_json['distance']
        return Item(int(id), name, store, distance)

    def __filter_items_by_queries(self, items, queries):
        selected = []
        for item in items:
            for query in queries:
                if item in query:
                    selected.append(item)
                    break
        return selected

    def __filter_by_last_time_seen(self, items, now):
        result = []
        for item in items:
            if item.id not in self.seen:
                self.seen[item.id] = now
                result.append(item)
            else:
                last_seen = self.seen[item.id]
                if last_seen + timedelta(seconds=ITEM_RELISTED_INTERVAL) < now:
                    self.seen[item.id] = now
                    result.append(item)
        return result


class Emailer:
    def __init__(self, server, port, sender_email, receiver_emails, password):
        self.server = server
        self.port = port
        self.sender_email = sender_email
        self.receiver_emails = receiver_emails
        self.password = password

    def send_items_found_message(self, item):
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            for receiver_email in self.receiver_emails:
                message = self.__create_message(item, receiver_email)
                server.sendmail(self.sender_email, receiver_email, message.encode('utf8'))

    def __create_message(self, item, receiver_email):
        msg_str = f"""
    {str(item)}

is available for purchase.
    """
        msg = MIMEText(msg_str, 'plain', 'utf8')
        msg['Subject'] = f"[2G2G] {item.store}"
        msg['From'] = self.sender_email
        msg["To"] = receiver_email
        msg["Date"] = formatdate(localtime=True)
        msg["Message-Id"] = email.utils.make_msgid()
        return msg.as_string()


@dataclass
class Item:
    id: int
    name: str
    store: str
    distance: float

    def __str__(self):
        return f"{self.name}\n{self.store}\n({round(self.distance, 2)} km away)"


class Query:
    def __init__(self,
                 keyword_blacklist=None,
                 keyword_whitelist=None,
                 store_blacklist=None,
                 store_whitelist=None,
                 max_distance=None):
        self.keyword_blacklist = keyword_blacklist
        self.keyword_whitelist = keyword_whitelist
        self.store_blacklist = store_blacklist
        self.store_whitelist = store_whitelist
        self.max_distance = max_distance

    def __contains__(self, item):
        result =     self.__is_in_list(self.store_whitelist, item.store) \
                and  self.__is_in_list(self.keyword_whitelist, item.name)
        if self.max_distance != None:
            result = result and item.distance < self.max_distance
        if self.keyword_blacklist != None:
            result = result and not self.__is_in_list(self.keyword_blacklist, item.name)
        if self.store_blacklist != None:
            result = result and not self.__is_in_list(self.store_blacklist, item.store)

        return result

    def __is_in_list(self, arr, val):
        if arr == None:
            return True
        found = False
        for keyword in arr:
            if keyword in val:
                found = True
                break
        return found

