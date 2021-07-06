import requests
import argparse
from bs4 import BeautifulSoup
import json


def get_credentials(credential_name):
    return json.loads(open(get_config_name(), "r").read())[credential_name]


def get_config_name():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_name", nargs="?")
    config_name = parser.parse_args().config_name
    if not config_name:
        config_name = "config.json"
    return config_name


def get_html():
    url = "https://tracking.orwonet.de/tracking/orderdetails.jsp"
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {
        "bagId": get_credentials("bagid"),
        "outletId": get_credentials("outletid"),
    }
    session = requests.Session()
    return session.post(url, headers=headers, data=payload).text


def extractJobStatus(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("td", class_="boxHalf")[-1].text


def getOldJobStatus():
    try:
        return json.load(
            open("current_job_state_" + get_credentials("bagid") + ".json")
        )["job_state"]
    except FileNotFoundError:
        create_initial_job_state_json_file()
        return getOldJobStatus()


def create_initial_job_state_json_file():
    write_state_to_job_state_json_file("Nicht verfügbar")


def write_state_to_job_state_json_file(state):

    json.dump(
        {"job_state": state},
        open("current_job_state_" + get_credentials("bagid") + ".json", "w"),
        ensure_ascii=False,
    )


def send_telegram(message):
    request_string = (
        "https://api.telegram.org/bot"
        + get_credentials("telegram_bot_token")
        + "/sendMessage?chat_id="
        + get_credentials("telegram_user_id")
        + "&parse_mode=Markdown&text="
        + message
    )
    response = requests.get(request_string)
    return response.json()


html = get_html()
old_job_status = getOldJobStatus()
new_job_status = extractJobStatus(html)


if old_job_status != new_job_status:
    send_telegram("🤖 Änderung '" + get_credentials("title") + "': " + new_job_status)
    write_state_to_job_state_json_file(new_job_status)
