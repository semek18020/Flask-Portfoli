from flask import Flask, render_template, request, session, redirect, url_for
import csv

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


# Function to write data to a text file
def write_to_file(data):
    with open('database.txt', 'a') as database_file:
        # Format the data as a string
        formatted_data = f"Email: {data['email']}, Subject: {data['subject']}, Message: {data['message']}"
        database_file.write(formatted_data + '\n')


def write_to_csv(data):
    # Open the CSV file in append mode ('a')
    with open('database.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row if the file is empty
        if csv_file.tell() == 0:  # Check if file is empty
            csv_writer.writerow(['Email', 'Subject', 'Message'])
        # Write the data row
        csv_writer.writerow([data['email'], data['subject'], data['message']])


#
# @app.route('/submit_form', methods=['POST', 'GET'])
# def submit_form():
#     return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Debugging: Print form data to verify
    print(email, subject, message)

    try:
        # Create a dictionary with the form data
        form_data = {'email': email, 'subject': subject, 'message': message}
        write_to_file(form_data)
        write_to_csv(form_data)
        return redirect('thankyou.html')
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while submitting the form."
