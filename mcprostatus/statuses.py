from . import session
from datetime import datetime as dt
import re


class Location(object):
    def __init__(self, location: str):
        self.statusjson = session.get("https://panel.mcprohosting.com/api/v1/public/nodes/statuses").json()
        self.location = location
        self.nodes = self.get_all_nodes()
        self.total_nodes = len(self.get_all_nodes())
        self.percentage_online = int((self.num_online() / self.total_nodes)*100)
        self.percentage_offline = int(100 - self.percentage_online)
        self.offline_nodes = self.get_all_offline_nodes()


    def get_all_nodes(self):
        nodes = []
        for node in self.statusjson[self.location]:
            nodes.append(node)
        return nodes

    def num_offline(self):
        offlineNodes = 0
        for node in self.statusjson[self.location]:
            status = self.statusjson[self.location][node]["online"]
            if not status:
                offlineNodes = offlineNodes + 1
        return offlineNodes

    def num_online(self):
        onlineNodes = 0
        for node in self.statusjson[self.location]:
            status = self.statusjson[self.location][node]["online"]
            if status:
                onlineNodes = onlineNodes + 1
        return onlineNodes

    def get_all_offline_nodes(self):
        offlineNodes = []
        for node in self.statusjson[self.location]:
            if not self.statusjson[self.location][node]["online"]:
                offlineNodes.append(node)
        return offlineNodes


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
        return self.statusjson[self.location][self.node]["online"]

    def get_network_issue(self):
        network_issue = self.statusjson[self.location][self.node]["network_issue"]
        if not network_issue:
            return network_issue
        else:
            network_issue = re.sub("<p[^>]*>", "", network_issue)
            network_issue = re.sub("</?p[^>]*>", "", network_issue)
            return network_issue

    def get_message(self):
        return self.statusjson[self.location][self.node]["message"]

    def get_last_heartbeat(self):
        heartbeat = dt.strptime(self.statusjson[self.location][self.node]["last_heartbeat"], '%Y-%m-%dT%H:%M:%S.%fZ')
        return heartbeat
