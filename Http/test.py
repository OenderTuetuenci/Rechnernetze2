import http.client, zlib, gzip
import urllib.parse
import re
import html.parser

conn = http.client.HTTPSConnection("moodle.htwg-konstanz.de")

class MyHTMLParser(html.parser.HTMLParser):
    TAGS = []
    TABLE = []
    in_td = False
    in_th = False
    def handle_starttag(self, tag, attrs):
        if tag == "input":
            self.TAGS.append(attrs)
        if tag == "td":
            self.in_td = True
        if tag == "th":
            self.in_th = True
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.in_td = False

    def handle_data(self, data):
        if self.in_td:
            print(data)
        if self.in_th:
            print(data)

    def handle_endtag(self, tag):
        self.in_td = False
        self.in_th = False

def login():
    # get first cookie
    conn.request('GET', '/moodle/')
    r1 = conn.getresponse()
    global tempcookie
    tempcookie = r1.getheader('Set-Cookie').split(';')[0]
    r1.read()

    # post password and username
    params = urllib.parse.urlencode({'username': 'rnetin', 'password': 'ntsmobil'})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Content-Length': 33,
              'Connection': 'keep-alive',
              'Cookie': tempcookie}
    conn.request("POST", "/moodle/login/index.php", body=params, headers=header)
    r2 = conn.getresponse()
    print(r2)
    print(r2.status, r2.reason)
    global cookie
    #cookie = r2.getheader('Set-Cookie').split(';')[0]
    # aprove the test
    r2.read()
    params = urllib.parse.urlencode({'testsession': 16509})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': tempcookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/login/index.php?testsession=16509', body=params, headers=header)
    r3 = conn.getresponse()
    r3.read();

    print(r3.status, r3.reason)
    params = urllib.parse.urlencode({'id': 2279})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': tempcookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/course/view.php?id=2279', body=params, headers=header)
    r4 = conn.getresponse()
    r4.read()
    print(r4.status, r4.reason)


def download():
    params = urllib.parse.urlencode({'id': 118815})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': tempcookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/assign/view.php?id=118815', body=params, headers=header)
    r5 = conn.getresponse()
    r5.read()
    print(r5.status, r5.reason)

    # download file
    params = urllib.parse.urlencode({'forcedownload': 1})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/',
              'Connection': 'keep-alive',
              'Cookie': tempcookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET',
                 '/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1',
                 body=params, headers=header)
    r6 = conn.getresponse()
    newfile = open('Rechnernetze.pdf', 'wb')
    newfile.write(r6.read())
    print(newfile)
    print(r6.status, r6.reason)


def chat():
    params = urllib.parse.urlencode({'id': 128994})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Referer': 'https://moodle.htwg-konstanz.de/moodle/course/view.php?id=2279',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/chat/view.php?id=128994', body=params, headers=header)
    r5 = conn.getresponse()
    r5.read()
    print(r5.status, r5.reason)
    params = urllib.parse.urlencode({'id': 183})
    header = {'Host': 'moodle.htwg-konstanz.de',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Upgrade-Insecure-Requests': 1}
    conn.request('GET', '/moodle/mod/chat/gui_basic/index.php?id=183', body=params, headers=header)
    r5 = conn.getresponse()
    data = r5.read()
    print(r5.status, r5.reason)

    #send message
    parser = MyHTMLParser()
    parser.feed(str(data))
    attribute = parser.TAGS

    sesskey = 0
    last = 0

    for a in attribute:
        if a[1][1] == "sesskey":
            sesskey = a[2][1]
        if a[1][1] == "last":
            last = a[2][1]

    while True:
        message = input("Message:")
        params = urllib.parse.urlencode({'message': message, 'id': '183', 'groupid': '0', 'last': last, 'sesskey': sesskey})
        header = {'Host': 'moodle.htwg-konstanz.de',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/64.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                  'Referer': 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Connection': 'keep-alive',
                  'Cookie': cookie,
                  'Upgrade-Insecure-Requests': 1}
        conn.request("POST", "/moodle/mod/chat/gui_basic/index.php", body=params, headers=header)
        r2 = conn.getresponse()
        print(r2.read())
        print(r2.status, r2.reason)
        header = {'Host': 'moodle.htwg-konstanz.de',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/64.0',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Referer': 'https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Connection': 'keep-alive',
                  'Cookie': cookie,
                  'Upgrade-Insecure-Requests': 1}
        params = urllib.parse.urlencode({'message': '', 'id': '183', 'groupid': '0', 'last': last, 'sesskey': sesskey, 'refresh': 'Aktualisieren'})
        conn.request("POST", "/moodle/mod/chat/gui_basic/index.php", params, headers=header)
        res = conn.getresponse()
        data = res.read()
        data = gzip.decompress(data)
        parser.feed(str(data))



if __name__ == '__main__':
    login()
    download()
    #chat()