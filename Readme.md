#  analog_film_notifier (for Rossman FotoWelt)
You brought away your film (@Rossman FotoWelt) and want to be notified when the filmprocessing state changes ? analog_film_notifier is a script that notifies you via telegram.
## usage
```bash
python3 analog_film_notifier.py bagid, outletid, telegram_bot_token, telegram_user_id
```
**arguments**: bagid: there's a jobid on departure slip, outletid: there's a outletid on departure slip, telegram_bot_token: telegrams token to send mails to bot, telegram_user_id: your telegram user id
## cronjob
the script can be installed as a cronjob to notify when jobstate changes.