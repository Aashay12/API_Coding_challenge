import unittest
from unittest.mock import patch
from get_all_tickets import process_ticket_data, get_all_tickets
from get_single_ticket import process_single_ticket, get_single_ticket


class TestApp(unittest.TestCase):

#To check process__ticket_data function
# Test 1: Should preprocess the all the tickets into correct structure for rendering
    def test_all_ticket(self):
        mock_object = [
            {
                "id": "1",
                "priority": "normal",
                "status": "open",
                "subject": "Hi, How are you doing?",
                "created_at": "2021-11-21",
                "requester_id": 1267068056929,
                "submitter_id": 1267068056929,
                "assignee_id": 1267068056929,
                "organization_id": 1260918907890,
                "group_id": 1260815665910,
            }
        ]
        expected_ticket_result = [
            ["1", "normal", "open", "Hi, How are you doing?", "2021-11-21"]]
        result = process_ticket_data(mock_object)
        self.assertEqual(expected_ticket_result, result)

#To check process_single_ticket function
# Test 2: Should preprocess a single ticket into correct structure for rendering
    def test_single_ticket(self):
        mock_object ={
                "id": "1",
                "created_at": "2021-11-21",
                "subject":"Hi, How are you doing?",
                "description": "My name is John. I am having issue with my printer",
                "requester_id": 1267068056929,
                "submitter_id": 1267068056929,
                "assignee_id": 1267068056929,
                "organization_id": 1260918907890,
                "group_id": 1260815665910,
            }
        expected_ticket_result = ["1", '2021-11-21', 'Hi, How are you doing?', "My name is John. I am having issue with my printer"]
        result = process_single_ticket(mock_object)
        self.assertEqual(expected_ticket_result, result)

#Check the entire get_all_ticket function
#Test 3: Check the API response and json data for all tickets
    def test_allticket_api(self):
        mock_response = [1, 'normal', 'open', 'Sample ticket: Meet the ticket', '2021-11-21']

        with patch("get_all_tickets.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
        response = get_all_tickets()
        length_of_response = len(response[0])
        self.assertEqual(response[2], mock_get.return_value.status_code)
        self.assertEqual(length_of_response, 100)
        self.assertEqual(response[0][0], mock_get.return_value.json.return_value)

#Check the entire get_single_ticket function
#Test 4: Check the entire get_single_ticket function works when passed null data
    def test_oneticket_api(self):
        mock_response = [1, '2021-11-21', 'Sample ticket: Meet the ticket', 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n']

        with patch("get_single_ticket.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
        response = get_single_ticket(1)
        self.assertEqual(response[2], mock_get.return_value.status_code)
        self.assertEqual(response[0], mock_get.return_value.json.return_value)
 
#Test 5: Check the whether the process_all_ticket function works as expected when passed empty Json
    def test_all_ticket(self):
        mock_object = [{}]
        expected_ticket_result = [[0, "None", "None", "None", "None"]]
        result = process_ticket_data(mock_object)
        self.assertEqual(expected_ticket_result, result)

#Test 6: Check the whether the process_single_ticket function works as expected when passed empty Json

    def test_single_ticket_1(self):
        mock_object = [{}]
        expected_ticket_result = [[0, "None", "None", "None", "None"]]
        result = process_ticket_data(mock_object)
        self.assertEqual(expected_ticket_result, result)


#Test 6: Check if ticket does not exist, then the get_single_ticket function shows the error
    def test_oneticket_api_error(self):
        mock_response = "RecordNotFound"

        with patch("get_single_ticket.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
        response = get_single_ticket(111)       #Ticket number does not exists
        self.assertNotEqual(response[2], mock_get.return_value.status_code)
        self.assertEqual(response[1]["error"], mock_get.return_value.json.return_value)


if __name__ == '__main__':
    unittest.main()
