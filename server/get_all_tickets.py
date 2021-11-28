import requests
import json, os
from requests.sessions import Request
import logging
from dotenv import load_dotenv

load_dotenv()

# Logging errors 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('./all_tickets.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Funtion to return data for all the tickets
def get_all_tickets():
    all_tickets_data = ""
    error = ""
    processed_tickets = []

    # Requesting Api to return all tickets
    url = os.getenv("GETALLTICKETSURL")
    all_tickets_data = requests.get(url, headers={'Content-Type': 'application/json',
                                                  'Authorization': '{}'.format(os.getenv("AUTHTOKEN"))})

    # Error handling
    if all_tickets_data.status_code != 200:
        error = json.loads(all_tickets_data.text)
        error_message ="Error: {} Status_code: {}".format(error["error"],all_tickets_data.status_code)  
        logger.error(error_message)
    else:
        all_ticket = json.loads(all_tickets_data.text)
        if not all_ticket:
            return [0, "None", "None", "None", "None"]
        else:
            processed_tickets = process_ticket_data(all_ticket["tickets"])
    return processed_tickets, error, all_tickets_data.status_code


# Preprocess and store id, priority, status, subject and date of the tickets
def process_ticket_data(ticket_list):
    ticket_subjects = []
    for fields in ticket_list:
        ticket_subjects.append([fields['id'] if "id" in fields else 0, fields["priority"] if "priority" in fields else 'None',
                                    fields["status"] if "status" in fields else 'None', fields["subject"] if "subject" in fields else "None", fields["created_at"][0:10] if "created_at" in fields else "None"])
    logger.info("Successfully logged {} Tickets.".format(len(ticket_subjects)))
    return ticket_subjects