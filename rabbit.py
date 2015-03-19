#!/usr/bin/env python

from bs4 import BeautifulSoup
import jinja2
import os
import shutil


class Rabbit(object):
    """ if it has do dig, it might as well be a rabbit """

    def __init__(self, _fbData):
        self.fb = _fbData


    def prepare(self):
        """ sets up the environemnt """

        if not os.path.exists('msg'):
            os.makedirs('msg')
            shutil.copyfile(os.path.join(self.fb, 'html/style.css'), 'msg/style.css')
        if not os.path.exists('msg_asc'):
            shutil.copytree('msg', 'msg_asc')


    def convert(self, v, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi']:
            if abs(v) < 1024.0:
                return '{0:.1f} {1}{2}'.format(v, unit, suffix)
            v /= 1024.0


    def dig(self, _target='messages.htm'):
        """ splits the target in one <thread> per file """

        s = BeautifulSoup(open(os.path.join(self.fb, 'html/', _target)))

        threads = s.find_all('div', class_ = 'thread')

        for t in threads:
            chatBetween = t.contents[0].strip(' \n')
            if len(chatBetween) > 64:
                chatBetween = chatBetween[:64]

            with open(os.path.join('msg', chatBetween + '.html'), 'w') as newChat:
                newChat.write('<html><head><meta charset="utf-8"></head>'
                              '<link rel="stylesheet" href="style.css" type="text/css"/>')
                newChat.write(t.encode('utf-8') + '</html>')

            self.reverse(t, chatBetween)


    def reverse(self, _t, _chatBetween):
        """ reverses a chat from DESC to ASC order """

        msgDivs = _t.find_all('div', class_ = 'message')
 
        stack = []
        for s in msgDivs:
            stack.append(s.find_next('p'))
            stack.append(s)

        stack.reverse()

        with open(os.path.join('msg_asc', 'rev-' + _chatBetween + '.html'), 'w') as revChat:
            revChat.write('<html><head><meta charset="utf-8"></head>'
                          '<link rel="stylesheet" href="style.css" type="text/css"/>')
            for item in stack:
                revChat.write(item.encode('utf-8'))
            revChat.write('</html>')


    def rank_by_size(self, _dir):
        chatList = os.listdir(unicode(_dir))
        pairs = []
        for chat in chatList:
            if chat.endswith('.html'):
                location = os.path.join(_dir, chat)
                size = os.path.getsize(location)
                pairs.append( (size, chat) )
        pairs.sort(key=lambda s: s[0], reverse=True)

        # creating html report
        top_value = pairs[0][0]
        s = BeautifulSoup(open(os.path.join(self.fb, 'index.htm')))
        generated = s.find('div', class_ = 'footer')

        tempLoader = jinja2.FileSystemLoader('templates')
        env = jinja2.Environment(loader = tempLoader)
        template = env.get_template('index.jinja')

        values = []
        for pos, val in enumerate(pairs):
            relative_value = (100 * val[0]) / top_value
            human_size = self.convert(val[0])
            values.append( (pos+1, val[1], relative_value, human_size) )

        html = template.render(generated = generated.contents[0],
                               values = values)

        with open('report.html', 'w') as f:
            f.write(html.encode('utf-8'))


def main():

    # replace this with your own facebook directory
    r = Rabbit('facebook-oilnam')
    r.prepare()
    r.dig()
    r.rank_by_size('msg')


if __name__== "__main__":
    main()
    
