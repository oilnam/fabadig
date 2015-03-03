#!/usr/bin/env python

from bs4 import BeautifulSoup
import os
import shutil

class Rabbit(object):
    ''' if it has do dig, it might as well be a rabbit '''

    def __init__(self, _fbData):
        self.fb = _fbData


    def prepare(self):
        ''' sets up the environemnt '''
        
        if not os.path.exists('msg'):
            os.makedirs('msg')
            shutil.copyfile(self.fb + '/html/style.css', 'msg/style.css')
        if not os.path.exists('msg_asc'):
            shutil.copytree('msg', 'msg_asc')


    def dig(self, _target='messages.htm'):
        ''' splits the target in one <thread> per file '''

        s = BeautifulSoup(open(self.fb + '/html/' + _target))
        threads = s.find_all('div', class_ = 'thread')

        for t in threads:
            chatBetween = t.contents[0].strip(' \n')
            if len(chatBetween) > 64:
                chatBetween = chatBetween[:64]

            with open('msg/' + chatBetween + '.html', 'w') as newChat:
                newChat.write('<link rel="stylesheet" href="style.css" type="text/css"/>')
                newChat.write(t.encode('latin-1'))

            self.reverse(t, chatBetween)


    def reverse(self, _t, _chatBetween):
        ''' reverses a chat from DESC to ASC order '''

        msgDivs = _t.find_all('div', class_ = 'message')
 
        stack = []
        for s in msgDivs:
            stack.append(s.find_next('p').encode('latin-1'))
            stack.append(s.encode('latin-1'))

        stack.reverse()

        with open('msg_asc/rev-' + _chatBetween + '.html', 'w') as revChat:
            revChat.write('<link rel="stylesheet" href="style.css" type="text/css"/>')
            for item in stack:
                revChat.write(item)


    def rank_by_size(self, _dir):
        chatList = os.listdir(_dir)
        pairs = []
        for chat in chatList:
            if chat.endswith('.html'):
                location = os.path.join(_dir, chat)
                size = os.path.getsize(location)
                pairs.append( (size, chat) )
        pairs.sort(key=lambda s: s[0], reverse=True)

        # dumping everything ASCII style
        top_value = pairs[0][0]
        s = BeautifulSoup(open(self.fb + '/index.htm'))
        generated = s.find('div', class_ = 'footer')

        with open('report.txt', 'w') as report:
            report.write('=> Digging into the FB chat hole (100-point grading scale) \n')
            report.write('=> '+ generated.contents[0].encode('latin-1') + '\n\n')

            for pos, val in enumerate(pairs):
                relative_value = (100 * val[0]) / top_value
                report.write('{0} [{3}]\n{1} ({2}%)\n\n'.format(val[1], '#'*relative_value, relative_value, pos+1))


def main():

    # replace this with your own facebook directory
    r = Rabbit('facebook-oilnam')
    r.prepare()
    r.dig()
    r.rank_by_size('msg')


if __name__== "__main__":
    main()
    
