import requests
from bs4 import BeautifulSoup

# urls needed
login_url = 'https://moodle.htwg-konstanz.de/moodle/login/index.php'
download_url = "https://moodle.htwg-konstanz.de/moodle/pluginfile.php/188750/mod_assign/introattachment/0/AIN%20RN%20-%20Laboraufgabe%20-%20HTTP.pdf?forcedownload=1"
chat_url = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php?id=183"
chat_interaction_url = "https://moodle.htwg-konstanz.de/moodle/mod/chat/gui_basic/index.php"

# login data
user = ""
password = ""

session = requests.Session()


def extract_value(req, value):
    soup = BeautifulSoup(req.text, "html.parser")
    form = soup.find('form')
    return form.find('input', {'name': value}).get('value')


def login(session):
    print("try to login ...")
    request_data = {'username': user,
                    'password': password,
                    'logintoken': ''}
    req = session.get(login_url)
    request_data['logintoken'] = extract_value(req, 'logintoken')
    session.post(login_url, data=request_data)
    print("logged in!")


def download(session):
    req = session.get(download_url)
    with open("Rechnernetze.pdf", "wb") as f:
        f.write(req.content)
    print("downloaded file")


def getmsgs(session, sesskey, last):
    message_data = {
        "message": "",
        "id": "183",
        "gruopid": "0",
        "last": last,
        "sesskey": sesskey,
        "refresh": "Aktualisieren"
    }
    req = session.post(chat_interaction_url, message_data)
    with open("msg.html", "wb") as f:
        f.write(req.content)
    print("message refreshed")


def send(session, sesskey, last, message):
    message_data = {
        "message": message,
        "id": "183",
        "gruopid": "0",
        "last": last,
        "sesskey": sesskey
    }
    session.post(chat_interaction_url, message_data)
    print("message send")


def chat(session):
    print("start chat")
    url = chat_url
    req = session.get(url)
    sesskey = extract_value(req, 'sesskey')
    last = extract_value(req, 'last')
    inp = ""
    while inp != "q":
        inp = input(
            "Enter command: a -> Nachrichten aktualisieren, s -> Nachricht senden")
        if inp == "a":
            getmsgs(session, sesskey, last)
        elif inp == "s":
            message = input("Nachricht eingeben:")
            send(session, sesskey, last, message)
    print("end chat")


def get_headers(req):
    header = {}
    header["lastmodified"] = extract_value(req, 'lastmodified')
    header["id"] = extract_value(req, 'id')
    header["userid"] = extract_value(req, 'userid')
    header["action"] = extract_value(req, 'action')
    header["sesskey"] = extract_value(req, 'sesskey')
    header["_qf__mod_assign_submission_form"] = extract_value(
        req, '_qf__mod_assign_submission_form')
    header["files_filemanager"] = extract_value(req, 'files_filemanager')
    header["submitbutton"] = "%C3%84nderungen+sichern"
    return header


def upload(session):
    # req = session.get("https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php?id=118815")
    url = "https://moodle.htwg-konstanz.de/moodle/repository/repository_ajax.php?action=upload"
    files = {'file': open('Rechnernetze.pdf', 'rb')}
    req = session.post(url, files=files)
    print(req.text)
    #headers = get_headers(req)
    #url = "https://moodle.htwg-konstanz.de/moodle/mod/assign/view.php"
    #req = session.post(url,headers)

# excecution
login(session)
download(session)
chat(session)
# upload(session)
