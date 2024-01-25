import requests

nifi_url = "https://nifi.erg.kz/nifi-api"
username = "yessil.adilzhanov"
password = "1qaz2wsX"

#Get token
def get_token() -> str:
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(nifi_url + "/access/token", headers=headers, data=data, verify=False)
    return response.text

# Get current version of processor
def get_cur_ver(processor_id: str) -> int:
    get_processor_info_url = f"{nifi_url}/processors/{processor_id}"
    response = requests.get(get_processor_info_url, headers={"Authorization": f"Bearer {get_token()}"}, verify=False)
    processor_info = response.json()
    current_version = processor_info["revision"]["version"]
    return int(current_version)

# Set run status of processor(STOPPED, RUNNING, DISABLED, RUN_ONCE)
def set_run_proc(processor_id: str, state: str) -> str:
    update_run_status_url = f"{nifi_url}/processors/{processor_id}/run-status"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token()}"
    }
    request_body = {
        "revision": {
            "clientId": username,
            "version": get_cur_ver(processor_id),
            "lastModifier": username
        },
        "state": state,
        "disconnectedNodeAcknowledged": "true"
    }

    response = requests.put(update_run_status_url, json=request_body, headers=headers, verify=False)
    return response.text

# Get queue size
def get_queue_size(queue_id: str) -> int:
    queue_url = f"{nifi_url}/flowfile-queues/{queue_id}/listing-requests"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_token()}"
    }
    response = requests.post(queue_url, headers=headers, verify=False)
    data = response.json()
    objectCount = data["listingRequest"]["queueSize"]["objectCount"]
    return int(objectCount)


