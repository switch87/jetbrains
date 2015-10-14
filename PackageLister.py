from datetime import date
from xxlimited import Null
from termcolor import colored
from lxml import etree
import requests


class Channel(object):
    def __init__(self, package, channel):
        self.channel = channel
        self.id = channel.attrib['id']
        self.package = package
        build = channel.find('build')
        self.build_number = build.attrib['number']
        self.build_version = build.attrib['version']
        try:
            datestring = build.attrib['releaseDate']
            self.release_date = date(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:]))
        except:
            self.release_date = Null

    def print(self):
            print('\t%-18s%-30s%15s' %
                  (self.id,
                   colored(self.build_version+'-'+self.build_number, 'green'),
                   colored(self.get_download_link(), 'red'))
                  )

    def get_download_link(self):
        if self.package.name == 'IntelliJ IDEA':
            if not '_EAP' in self.id:
                return  "https://download.jetbrains.com/idea/ideaIU-" + self.build_version + ".tar.gz"
            else:
                for button in self.channel.iter('button'):
                    if 'Download' in button.attrib['name']:
                        return button.attrib['url']
        else:
            for button in self.channel.iter('button'):
                if 'Download' in button.attrib['name']:
                    return button.attrib['url']



class Package(object):
    def __init__(self, product):
        self.name = product.attrib['name']
        self.channels = []
        for channel in product.iter('channel'):
            new = Channel(self, channel)
            if len(self.channels) > 0:
                if not 'eap' in new.id.lower():
                    del self.channels[-1]
                    if len(self.channels) == 1:
                        self.channels.clear()
                else:
                    if self.channels[-1].build_version == new.build_version:
                        continue
            self.channels.append(new)


    def print_tree(self):
        print(colored(self.name, 'blue'))
        for channel in self.channels:
            channel.print()

    def channel_count(self):
        return len(self.channels)


class PackageList(object):
    def __init__(self, file=None):
        self.packages = []
        if file:
            root = etree.fromstring(requests.get(file).text)
            for package in root.getchildren():
                if package.attrib['name'] != '0xDBE':
                    self.packages.append(Package(package))

    def print_tree(self):

        for package in self.packages:
            package.print_tree()

    def package_count(self):
        return len(self.packages)

    def all_channels_count(self):
        count = 0
        for package in self.packages:
            count += package.channel_count()
        return count