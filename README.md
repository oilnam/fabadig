# fabadig
a Facebook Backup Digger

Overview
--------
Fabadi helps you turn the [copy of your Facebook data](https://www.facebook.com/help/131112897028467/) in something suitable for human beings, by doing three things:

1. It breaks the huge, unreadable `messages.htm` into a distinct file for every chat
2. It makes an ascending copy of all your chats (so that earlier values precede later ones)
3. It plots your chats in an ASCII rank, sorted by chat size, which is a rough yet fairly accurate way to find out who you chat with the most.

Install and Running
-------------------
    $ pip install BeautifulSoup4
    $ git clone https://github.com/oilnam/fabadig.git
    $ cd fabadig
    $ emacs rabbit.py
  
than replace `r = Rabbit('facebook-oilnam’)` with (the path to) your own data directory and run the script with no args. It might take a little while depending on the size of your `message.htm` (still less then a minute on my Macbook Pro).

Authors
-------
manlio <manlio.poltronieri@gmail.com>

License
-------
Beerware

