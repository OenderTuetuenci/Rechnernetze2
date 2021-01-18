import requests
from bs4 import BeautifulSoup

url = 'https://moodle.htwg-konstanz.de/moodle/login/index.php'
user = "oe391tue"
password = "61trabzon61"
request_data = {'username': user,
                'password': password,
                'logintoken': ''}

session = requests.Session()


def login(session):
    req = session.get(url)
    request_data['logintoken'] = getLoginToken(req)
    response = session.post(url, data=request_data)

def getLoginToken(req):
    soup = BeautifulSoup(req.text, "html.parser")
    form = soup.find('form')
    logintoken = form.find('input', {'name': 'logintoken'}).get('value')
    return logintoken

def getSesskey(req):
    soup = BeautifulSoup(req.text, "html.parser")
    form = soup.find('form')
    sesskey = form.find('input', {'name': 'sesskey'}).get('value')
    return sesskey

def getLast(req):
    soup = BeautifulSoup(req.text, "html.parser")
    form = soup.find('form')
    last = form.find('input', {'name': 'last'}).get('value')
    return last

def download(session):
    url = "https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1"
    req = session.get(url)
    with open("Rechnernetze1.pdf","wb") as f:
        f.write(req.content)

def getmsgs(session,sesskey,last):
    message_data = {
        "message": "",
        "id": "183",
        "gruopid": "0",
        "last": last,
        "sesskey": sesskey,
        "refresh": "Aktualisieren"
    }
    req = session.post("https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php", message_data)

def send(session,sesskey,last,message):
    message_data = {
        "message": message,
        "id": "183",
        "gruopid": "0",
        "last": last,
        "sesskey": sesskey
    }
    req = session.post("https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php", message_data)
    with open("nachrichten.html","wb") as f:
        f.write(req.text)


def chat(session):
    url = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183"
    req = session.get(url)
    sesskey = getSesskey(req)
    last = getLast(req)
    inp = ""
    while inp != "q":
        inp = input()
        if inp == "a":
            getmsgs(session,sesskey,last)
        elif inp =="s":
            message = input("Nachricht:")
            send(session,sesskey,last,message)

def getHeaders(req):
    soup = BeautifulSoup(req.text, "html.parser")
    form = soup.find('form')
    print(req.text)
    header = {}
    header["lastmodified"] = form.find('input', {'name': 'lastmodified'}).get('value')
    header["id"] = form.find('input', {'name': 'id'}).get('value')
    header["userid"] = form.find('input', {'name': 'userid'}).get('value')
    header["action"] = form.find('input', {'name': 'action'}).get('value')
    header["sesskey"] = form.find('input', {'name': 'sesskey'}).get('value')
    header["_qf__mod_assign_submission_form"] = form.find('input', {'name': '_qf__mod_assign_submission_form'}).get('value')
    header["files_filemanager"] = form.find('input', {'name': 'files_filemanager'}).get('value')
    header["submitbutton"] = "%C3%84nderungen+sichern"
    return header

def upload(session):
    req = session.get("https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php?id=118815")
    url = "https://moodle.htwg-konstanz.de/moodle/repository/repository_ajax.php?action=upload"
    files = {'file': open('Rechnernetze.pdf', 'rb')}
    req = session.post(url,files=files)
    print(req.text)
    #headers = getHeaders(req)
    #url = "https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php"
    #req = session.post(url,headers)

login(session)
#download(session)
#chat(session)
upload(session)



