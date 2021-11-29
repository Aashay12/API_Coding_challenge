from flask import Flask, render_template, request
from server.get_all_tickets import get_all_tickets
from server.get_single_ticket import get_single_ticket

app = Flask(__name__, template_folder="./client/templates")

@app.route('/')
def display_all_tickets():
    subjects,error,status_code, = get_all_tickets()
    return render_template('home.html', subjects=subjects, error = error)

@app.route('/ticket/<id>')
def display_single_ticket(id):
    single_ticket,error,status_code = get_single_ticket(id)
    return render_template('ticket_details.html', ticket = single_ticket, error = error)

if __name__ == '__main__':
    app.run(debug=True)
