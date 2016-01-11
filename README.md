# fabadig
a Facebook Backup Digger

Overview
--------
Ever wondered who are the people you chat with the most? Ever wanted to read every conversation you ever had on Facebook, since the beginning of time? I do all the time (sadly).

Fabadi helps you turn the [copy of your Facebook data](https://www.facebook.com/help/131112897028467/) in something you can easily ~~be obsessed by~~ read, by doing three things:

1. It breaks the huge, unreadable `messages.htm` into a distinct file for every chat
2. It makes an ascending copy of all your chats
3. It plots an HTML rank of your chats, sorted by chat size.

**TL;DR:** Every conversation you ever had on Facebook nicely sorted, and you can even Cmd+F.

Screenshot
----------
The rank of all the chats:

![ranking chats](https://raw.githubusercontent.com/oilnam/fabadig/master/images/screenshot.png)

A chat:

![a chat](https://raw.githubusercontent.com/oilnam/fabadig/master/images/screenshot2.png)


Install and Running
-------------------
You first need to get a [copy of your Facebook data](https://www.facebook.com/help/131112897028467/). Facebook will send it to you by email within a few hours (and within a few minutes every time after the first time).

Once you have it, unzip the folder and (assuming you're on OSX/Linux) run the following commands:

    $ git clone https://github.com/oilnam/fabadig.git
    $ cd fabadig
    $ sudo pip install -r requirements.txt
    
To generate your report:

    $ python src/rabbit.py <your facebook folder>
  
 It might take a little while depending on how much chat you have; still under a minute on my 2013 Macbook Pro though.

Authors
-------
manlio <manlio.poltronieri@gmail.com>

License
-------
Beerware
