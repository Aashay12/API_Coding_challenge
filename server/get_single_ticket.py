import requests,os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

# Logging errors 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Define logger format
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('./single_ticket.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Function to return data within a single ticket
def get_single_ticket(ticket_id):
    error = ''

    # Requesting Api to return data for a single ticket
    url = '{}{}'.format(os.getenv("GETSINGLETICKETURL"),ticket_id)
    ticket_data = requests.get(url, headers={'Content-Type': 'application/json',
                                             'Authorization': '{}'.format(os.getenv("AUTHTOKEN"))})

    # Error handling
    if ticket_data.status_code != 200:
        error = json.loads(ticket_data.text)
        error_message ="Error: {} Status_code: {}".format(error["error"],ticket_data.status_code)  
        logger.error(error_message)
    else:
        single_ticket = json.loads(ticket_data.text)
        processed_single_ticket_data = process_single_ticket(single_ticket["ticket"])
    return processed_single_ticket_data, error, ticket_data.status_code

#Storing id, created_at, subject, description and tags.
def process_single_ticket(single_ticket_data):
    single_ticket_detail = [single_ticket_data['id'], single_ticket_data["created_at"][0:10],
                                single_ticket_data["subject"], single_ticket_data["description"]]
    logger.info("Tickets logged successfully:  {}".format(single_ticket_detail))
    return single_ticket_detail
