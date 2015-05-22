# fabadig
a Facebook Backup Digger

Overview
--------
Ever wandered who are the people you chat with the most? Ever felt nostalgic about that conversation you had years ago? I do all the time.
Fabadi helps you turn the [copy of your Facebook data](https://www.facebook.com/help/131112897028467/) in something suitable for human beings, by doing three things:

1. It breaks the huge, unreadable `messages.htm` into a distinct file for every chat
2. It makes an ascending copy of all your chats (so that earlier values precede later ones)
3. It plots an HTML rank of your chats, sorted by chat size.

Screenshot
----------
![](https://github.com/oilnam/fabadig/tree/master/images/screenshot.png)

Install and Running
-------------------
    $ git clone https://github.com/oilnam/fabadig.git
    $ cd fabadig
    $ pip install -r requirements.txt
    $ python rabbit.py <your facebook folder>
  

 It might take a little while depending on the size of your `message.htm` (still less then a minute on my Macbook Pro).

Authors
-------
manlio <manlio.poltronieri@gmail.com>

License
-------
Beerware

