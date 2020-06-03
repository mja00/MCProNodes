from . import session
from datetime import datetime as dt
import re


class Location(object):
    def __init__(self, location: str):
        self.location = location
        self.nodes = self.get_all_nodes()

    def get_all_nodes(self):
        nodes = []
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        for node in statusJson[self.location]:
            nodes.append(node)
        return nodes

class Node(object):
    def __init__(self, node: str):
        self.node = f"Node {node}"
        self.location = self.get_node_location()
        self.online = self.get_online()
        self.network_issue = self.get_network_issue()
        self.message = self.get_message()
        self.last_heartbeat = self.get_last_heartbeat()

    def get_node_location(self):
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        for location in statusJson:
            if self.node in statusJson[location]:
                return location

    def get_online(self):
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        return statusJson[self.location][self.node]["online"]

    def get_network_issue(self):
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        network_issue = statusJson[self.location][self.node]["network_issue"]
        if not network_issue:
            return network_issue
        else:
            network_issue = re.sub("<p[^>]*>", "", network_issue)
            network_issue = re.sub("</?p[^>]*>", "", network_issue)
            return network_issue

    def get_message(self):
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        return statusJson[self.location][self.node]["message"]

    def get_last_heartbeat(self):
        path = "https://panel.mcprohosting.com/api/v1/public/nodes/statuses"
        statusJson = session.get(path).json()
        heartbeat = dt.strptime(statusJson[self.location][self.node]["last_heartbeat"], '%Y-%m-%dT%H:%M:%S.%fZ')
        return heartbeat
