import requests
import argparse
from bs4 import BeautifulSoup
import json


def get_params():
    parser = argparse.ArgumentParser()

    parser.add_argument("bagid", type=int)
    parser.add_argument("outletid", type=int)
    parser.add_argument("telegram_bot_token")
    parser.add_argument("telegram_user_id")
    args = parser.parse_args()
    return (
        args.bagid,
        args.outletid,
        args.telegram_bot_token,
        args.telegram_user_id,
    )


def make_request(bagid, outletid):
    url = "https://tracking.orwonet.de/tracking/orderdetails.jsp"
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {"bagId": bagid, "outletId": outletid}
    session = requests.Session()
    return session.post(url, headers=headers, data=payload).text


def extractJobStatus(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("td", class_="boxHalf")[1].text


def getOldJobStatus():
    try:
        return json.load(open("current_job_state.json"))["job_state"]
    except FileNotFoundError:
        create_initial_job_state_json_file()
        return getOldJobStatus()


def create_initial_job_state_json_file():
    write_state_to_job_state_json_file("Nicht verfügbar")


def write_state_to_job_state_json_file(state):
    json.dump(
        {"job_state": state}, open("current_job_state.json", "w"), ensure_ascii=False
    )


def send_telegram(message, telegram_bot_token, telegram_user_id):
    request_string = (
        "https://api.telegram.org/bot"
        + telegram_bot_token
        + "/sendMessage?chat_id="
        + telegram_user_id
        + "&parse_mode=Markdown&text="
        + message
    )
    response = requests.get(request_string)
    return response.json()


bagid, outletid, telegram_bot_token, telegram_user_id = get_params()
html = make_request(bagid, outletid)
old_job_status = getOldJobStatus()
new_job_status = extractJobStatus(html)
if old_job_status != new_job_status:
    send_telegram(
        f"🤖 Statechange (bagid:{bagid}) :{new_job_status}",
        telegram_bot_token,
        telegram_user_id,
    )
    write_state_to_job_state_json_file(new_job_status)
