# Zendesk-Coding-Challenge - Aashay Motiwala

A web based application that is written using the Flask framework. The app makes an HTTP request to the Zendesk Ticket API, which returns a list of all tickets linked with the account. These tickets are then shown in a tabular style. Users can obtain information about all tickets or specific data about a particular ticket.

## Prerequisite Installations

- [Flask](https://pypi.org/project/Flask/)
- Python 3 or higher.

## Screen Shots
- Landing Page :
![Home_Page](images/Home_Page.png)
![Home_Page](images/Home_Page_2.png)
-
## Live server

- When you run app.py
- Goto http://127.0.0.1:5000

## How to run (MacOS/Windows)

1. Download the repository to your local machine with the following code.

```
$ git clone https://github.com/Aashay12/Zendesk-Coding-Challenge.git
```

2. Navigate to the application folder using the terminal.

3. Make sure you have Flask and python3 installed.

4. Run the program with the following code.

```
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 app.py
```

#### Run Tests

1. Navigate to the 'server' directory in your MacOS Terminal or equivalent command line application.

2. Run the tests with the following code
```
$ python3  test_tickets.py
```

## Architectural Design Overview

### Assumptions

- Users are familar with running a python program.
- Tickets requests and Error responses to the Zendesk API will always return JSON with the same structure.

### Main Component Description

- `app.py` : Program entry point, handles all the routes and passes data between different pages.
- `get_all_tickets.py` : Contains code for making http requests for receiving list of all tickets from the Zendesk Api.
- `get_single_ticket.py` : Contains code for making http requests for receiving data about a single ticket from the Zendesk Api.
- `main.html` : Web-page to display list of all tickets in a tabular format.
- `ticket.html` : Web-page to display data about a single ticket.
- `base.html` : Jinja template to hold the static html and js content.
- `all_tickets.log` : Log file that stores and reports any errors faced by the user while requesting list of tickets.
- `single_ticket.log` : Log file that stores and reports any errors faced by the user while requesting data about a ticket.
- `requirements.txt` : Text file for the required dependecies.

### Design Choices

#### Connecting and requesting tickets from the zendesk API

Data handling is easy python
UI rendering is easy because Jinja



Originally I had used a get request with Basic authentication as my primary method of sending credentials to the API, but after reading further into the Zendesk developer docs, I came to realise that hardcoding the admin username and password into a client application is far too insecure.

The application now uses OAuth 2.0 as the primary method of communicating credentials, using the `Bearer Token` syntax, within the request Authorization header. The token resides in the .env file and is read into the node process object on the attribute `TOKEN` in config.js. The benefit of having used OAuth 2.0 for credential authentical is that:

1. The login username and password are no longer hardcoded in plain text, which would have left them vulnerable to being compomised.
2. OAuth 2.0 allows scope limits to be set that can restrict token access to **_only reading ticket data_** from the Zendesk API.

#### Display tickets in a list & Display individual ticket details

I found that putting all of the string output methods and functionality into the Display class created a ridiculous amount of redundant code
and made readability quite cumbersome. I opted to add toString methods for both summary and full detail outputs onto the Ticket class and relocated the majority of string output into a separate _message.js_ Object. Moving most of the generic string output to the _message.js_ Object helped to:

1. Increase readbility of the Display.js class file.
2. Make all text output follow a more concise naming convention e.g: `display.print(message.goodbye)`.

#### Page through tickets when more than 25 are returned

I had planned to have the TicketFetcher pull down the limit of 100 tickets per requests and display ten tickets per page. Then allow the user to page through until the tickets until they were complete, but I found that this method of logic was unintuitive and tedious as the calculations for something simple such as the current page number grew rather unwieldy. Also, retrieving the limit of tickets per request meant that you would be wasting bandwidth if the user decided to exit after the first page, so for those reasons I decided it would be best to allow the TicketFetch to pull only twenty-five tickets per request then display the entire twenty-five tickets in console, this meant that:

1. Users were only needing to make network requests for the exact number of pages they wanted to viw.
2. The code was cleaner and more readable due as the server handled most of the pagination processing.

## Learning Resources

The following section contains links to resources I found super useful while building this application.

- Zendesk docs quick links

  - [Tickets](https://developer.zendesk.com/rest_api/docs/support/tickets#show-ticket)

  - [Basic Authentication](https://developer.zendesk.com/rest_api/docs/support/introduction#basic-authentication)

- Tips and best practices that helped make my code more clean organised.

  - [Error Logging](https://www.loggly.com/use-cases/6-python-logging-best-practices-you-should-be-aware-of/)

- Reference for following practices to write Readme.md file.

  - [Github MD Files Formatting](https://help.github.com/en/articles/basic-writing-and-formatting-syntax)
