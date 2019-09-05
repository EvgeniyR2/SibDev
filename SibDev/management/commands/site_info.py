import requests
from django.core.management.base import BaseCommand
from django.utils.html_parser import HTMLParser

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            pageHtml = requests.get(options['url'][0]).text
            result = MyParser().parse(pageHtml)
            return result
        except:
            return ''

class MyParser(HTMLParser):
    inHeading = False
    result = ''
    currentTag = ''
    def handle_starttag(self, tag, attrs):
        if tag == self.currentTag:
            if tag == 'meta':
                if isinstance(attrs[0], tuple):
                    if attrs[0][0] == 'charset':
                        self.result += '- charset: ' + attrs[0][1] + '\n'
            else:
                self.inHeading = True
    def handle_data(self, data):
        if self.inHeading:
            self.result += '- ' + self.currentTag + ': ' + data + '\n'
    def handle_endtag(self, tag):
        if tag == self.currentTag:
            self.inHeading = False
    def parse(self, html_text):
        self.currentTag = 'title'
        self.feed(html_text)
        self.currentTag = 'h1'
        self.feed(html_text)
        self.currentTag = 'meta'
        self.feed(html_text)
        return self.result
