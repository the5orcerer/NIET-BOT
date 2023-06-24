from flask import Flask, request, request
import datetime
import pytz
app = Flask(__name__)

@app.route('/')
def get_day_name():
    tz = pytz.timezone('Asia/Dhaka')  # Set the desired timezone
    current_time = datetime.datetime.now(tz)
    day_name = current_time.strftime('%A')  # Get the day name in the specified timezone
    return f"{day_name}"

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.form['data']  # Assuming the POST data has a field named 'data'

    # Save the data to a file
    with open('data.txt', 'w') as file:
        file.write(data)

    return 'Data saved successfully'
@app.route('/save_notice', methods=['POST'])
def save_routine():
    data = request.form['data']  # Assuming the POST data has a field named 'data'

    # Save the data to a file
    with open('notice.txt', 'w') as file:
        file.write(data)

    return 'Data saved successfully'

if __name__ == '__main__':
    app.run()
