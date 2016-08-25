# Receipt

##Crawler

A Crawler represents as a client side

if you want to run Crawler(clien side)

you need to install beautifulsoup and tesseract

```bash
sudo apt-get install python-bs4
sudo apt-get install tesseract-ocr
```

and you can either use

```bash
python Crawler.py
```

which is the default setting that will connect to a server on localhost:5555

or you can use

```bash
python TaskManager.py 192.168.1.10
```
which will connect to a server on 192.168.1.10:5555(recommend : set it to be the server ip address)

##TaskManager

A TaskManager represents as a server side

if you want to run TaskManager(server side)

all you need to do is run the install.sh, it will set up the database for you

```bash
sh install.sh
```

and you can either use

```bash
python TaskManager.py
```

which is the default setting that will run a server on localhost:5555

or you can use

```bash
python TaskManager.py 192.168.1.10
```

which will run a server on 192.168.1.10:5555(recommend : set it to be your ip address)
