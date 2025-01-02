
try:
    import json
    import tqdm
    import os
    import requests
    import time
    import logging
    import threading
    from datetime import datetime
    from MODS.colors import gradify
    from MODS.colors import *
except Exception as e:
    print(f"[ERROR] > Libs are not installed")
    os.system("pip install -r requirements.txt")




MSS = {
    'sent': 0,
    'failed': 0
}


def SLOG(level="INFO"):
    levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR}
    logging.basicConfig(
        filename='spammer.log',
        level=levels.get(level.upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def VADC(config):
    required_keys = {"webhooks", "payload", "delay", "name", "avatar_url", "message_count"}
    missing_keys = required_keys - config.keys()
    if missing_keys:
        raise ValueError(f"Configuration missing required keys: {missing_keys}")
    if not isinstance(config["webhooks"], list) or not config["webhooks"]:
        raise ValueError("Webhooks should be a non-empty list.")
    if not isinstance(config["payload"], dict):
        raise ValueError("Payload should be a dictionary.")

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            VADC(config)
            return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        print(f"[ALERT] {datetime.now()} Error > {e}")
        return None

def CWV(webhook):
    try:
        response = requests.get(webhook)
        if response.status_code == 200:
            return True
        else:
            logging.warning(f"Webhook {webhook} is not valid. Status code: {response.status_code}")
            print(f"[ {datetime.now()} ] - [{r}ERROR{w}] - Webhook is invalid: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error checking webhook validity for {webhook}: {e}")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - Error checking webhook: {e}")
        return False



def SM(webhook, payload, MSS):
    try:
        response = requests.post(webhook, json=payload)
        if response.status_code == 204:
            logging.info(f"Message sent successfully to {webhook}")
            print(f"[ {datetime.now()} ] - [{gradify('INFO', option='magenta_to_blue')}] - Message Sent to Webhook")
            MSS['sent'] += 1
        else:
            logging.warning(f"Failed to send to {webhook}: {response.status_code}, {response.text}")
            print(f"[ {datetime.now()} ] - [{y}ERROR{w}] - Failed to send, possibly being rate-limited ")
            MSS['failed'] += 1
    except Exception as e:
        logging.error(f"Error sending to {webhook}: {e}")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - {e}")
        MSS['failed'] += 1

def sSWM(webhooks, payload, message_count=40, delay=1):
    threads = []
    MSS = {
        'sent': 0,
        'failed': 0
    }

    for webhook in webhooks:
        if not CWV(webhook):
            continue
        for _ in range(message_count):
            t = threading.Thread(target=SM, args=(webhook, payload, MSS))
            threads.append(t)
            t.start()
            time.sleep(delay)
    for thread in threads:
        thread.join()

    print(f"Sent messages: {MSS['sent']}, Failed messages: {MSS['failed']}")

def UWP(webhook, name, avatar_url):
    try:
        response = requests.patch(webhook, json={"name": name, "avatar": avatar_url})
        if response.status_code == 200:
            logging.info(f"Webhook profile updated Successfully for {webhook}")
            print(f"[ {datetime.now()} ] - [{gradify('INFO', option='magenta_to_blue')}] - Webhook profile updated successfully for {webhook}")
        else:
            logging.warning(f"Failed to update webhook profile for {webhook}: {response.status_code}, {response.text}")
            print(f"[ {datetime.now()} ] - [{y}ERROR{w}] - Failed to update webhook profile for {webhook}")
    except Exception as e:
        logging.error(f"Error updating webhook profile for {webhook}: {e}")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - {e}")

def RIW(webhook, config_path):
    try:
        with open(config_path, 'r+') as file:
            config = json.load(file)
            if webhook in config["webhooks"]:
                config["webhooks"].remove(webhook)
                file.seek(0)
                json.dump(config, file, indent=4)
                file.truncate()
                logging.info(f"Removed invalid webhook: {webhook}")
                print(f"[ {datetime.now()} ] - [{gradify('INFO', option='red_to_yellow')}] - Removed invalid webhook: {webhook}")
    except Exception as e:
        logging.error(f"Failed to remove invalid webhook: {e}")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - Failed to remove invalid webhook.")

def DSY(sent, failed, start_time):
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n[SUMMARY]")
    print(f"Messages Sent: {sent}")
    print(f"Failures: {failed}")
    print(f"Total Time: {duration:.2f} seconds")
    logging.info(f"Summary: Sent={sent}, Failed={failed}, Duration={duration:.2f}s")

if __name__ == "__main__":
    os.system('title Daisy Webhook Spammer > dev : config')
    
    print(purpleblue("""
________         .__                                                                   
\______ \ _____  |__| _________.__.   _________________    _____   _____   ___________ 
 |    |  \\__  \ |  |/  ___<   |  |  /  ___/\____ \__  \  /     \ /     \_/ __ \_  __ \
 |    `   \/ __ \|  |\___ \ \___  |  \___ \ |  |_> > __ \|  Y Y  \  Y Y  \  ___/|  | \/
/_______  (____  /__/____  >/ ____| /____  >|   __(____  /__|_|  /__|_|  /\___  >__|   
        \/     \/        \/ \/           \/ |__|       \/      \/      \/     \/       
                          Dev : config
                          version : 1.0
"""))

    args = {"log_level": "INFO"}
    SLOG(level=args["log_level"])
    config_path = "config/config.json"

    config = load_config(config_path)
    if not config:
        logging.error("Failed to load configuration.")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - Failed to Load Config.json")
        exit(5)

    webhooks = config.get("webhooks", [])
    payload = config.get("payload", {})
    delay = config.get("delay", 1)
    webhook_name = config.get("name", "Webhook")
    avatar_url = config.get("avatar_url", None)
    message_count = config.get("message_count", 40)

    if not webhooks:
        logging.error("No webhooks found in the configuration.")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - No Webhooks Found in Configuration File")
        exit(5)

    if not payload:
        logging.error("No payload found in the configuration.")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - No Payload in Configuration File")
        exit(5)

    valid_webhooks = [webhook for webhook in webhooks if CWV(webhook)]

    if len(valid_webhooks) == 0:
        logging.error("No valid webhooks found.")
        print(f"[ {datetime.now()} ] - [{r}CRITICAL{w}] - No valid webhooks to send messages.")
        exit(5)

    start_time = datetime.now()
    sent, failed = sSWM(valid_webhooks, payload, message_count, delay)

    if webhook_name or avatar_url:
        for webhook in valid_webhooks:
            UWP(webhook, webhook_name, avatar_url)

    DSY(sent, failed, start_time)
    logging.info("Finished sending messages.")
    print(f"[ {datetime.now()} ] - [{y}ALERT{w}] - Finished Spamming <3")
