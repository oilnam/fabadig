#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections import deque
import jinja2
import os
import shutil
import sys
import time


class Rabbit(object):
    """ If it has do dig, it might as well be a rabbit """

    def __init__(self, _fbData):
        self.fb = _fbData
        self.report_path = 'report-' + time.strftime('%d-%m-%Y')


    def env_setup(self):
        """ Sets up the environemnt """

        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
            os.makedirs(os.path.join(self.report_path, 'chats'))
        try:
            shutil.copyfile(os.path.join(self.fb, 'html/style.css'), os.path.join(self.report_path, 'chats/style.css'))
        except IOError:
            print('Invalid directory provided')
            sys.exit(1)


    def dig(self, _target='messages.htm'):
        """ Digs through messages.htm and creates a new html file for every chat """

        try:
            s = BeautifulSoup(open(os.path.join(self.fb, 'html/', _target)))
        except IOError:
            print('Invalid directory provided')
            sys.exit(1)

        threads = s.find_all('div', class_ = 'thread')
        for t in threads:
            chat_between = t.contents[0].strip(' \n')
            if len(chat_between) > 64:
                chat_between = chat_between[:64]

            msg_divs = t.find_all('div', class_ = 'message')
            q = deque([])
            for s in msg_divs:
                q.appendleft(s.find_next('p'))
                q.appendleft(s)

            with open(os.path.join(self.report_path, 'chats', chat_between + '.html'), 'w') as revChat:
                revChat.write('<html><head><meta charset="utf-8"></head>'
                              '<link rel="stylesheet" href="style.css" type="text/css"/>')

                for item in q:
                    revChat.write(item.encode('utf-8'))
                revChat.write('</html>')


    def rank_by_size(self):
        """ Logic for creating a report index with all the chats ranked by size """

        list_of_chats = os.listdir(unicode(os.path.join(self.report_path, 'chats')))
        pairs = []
        for chat in list_of_chats:
            if chat.endswith('.html'):
                chat_size = os.path.getsize(os.path.join(self.report_path, 'chats', chat))
                pairs.append( (chat_size, chat) )
        pairs.sort(key=lambda s: s[0], reverse=True)

        biggest_chat = pairs[0][0]
        chat_entries = []

        for pos, chat in enumerate(pairs):
            adjusted_score = (100 * chat[0]) / biggest_chat
            human_size = human_readable_size(chat[0])
            chat_entries.append( (pos+1, chat[1], adjusted_score, human_size) )

        self.write_report(chat_entries)


    def write_report(self, chat_entries):
        """ Actually writes the report to file """

        s = BeautifulSoup(open(os.path.join(self.fb, 'index.htm')))
        fb_backup_date = s.find('div', class_ = 'footer')

        env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
        template = env.get_template('index.jinja')

        html = template.render(generated = fb_backup_date.contents[0], chats = chat_entries)

        with open(os.path.join(self.report_path, 'report.html'), 'w') as f:
            f.write(html.encode('utf-8'))


def human_readable_size(v, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi']:
        if abs(v) < 1024.0:
            return '{0:.1f} {1}{2}'.format(v, unit, suffix)
        v /= 1024.0


def main():

    if len(sys.argv) != 2:
        print('usage: python {0} <facebook directory>'.format(sys.argv[0]))
        sys.exit(1)

    print('Going through all your chats... this might take a few minutes')
    r = Rabbit(sys.argv[1])
    r.env_setup()
    r.dig()
    r.rank_by_size()
    print('...done! :)')
    print('You can find your chats inside ' + r.report_path)


if __name__== "__main__":
    main()
    
