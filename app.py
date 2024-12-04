from flask import Flask, render_template, request
from requests import get

app = Flask(__name__)
API_ENDPOINT = "https://api2.hackclub.com/v0.1/Sessions/Events"


@app.route('/')
def index():
    res = get(API_ENDPOINT)
    data = res.json()
    events = [event['fields'] for event in data]
    ordered_events = sorted(events, key=lambda x: x['Start Time'])
    ordered_events.reverse()
    for event in ordered_events:
        try:
            event['Avatar'] = event['Avatar'][0]['url']
        except:
            print(event['Title'])
    
    return render_template('index.html', events=ordered_events)

@app.route('/<slug>')
def event(slug: str):
    res = get(f"{API_ENDPOINT}")
    data = res.json()
    for event in data:
        if event['fields']['Title'] == slug:
            event = event['fields']
            break
    event['Avatar'] = event['Avatar'][0]['url']
    return render_template('event.html', event=event)


@app.route('/new')
def new_event():
    return render_template('new.html')


@app.route('/create', methods=['POST'])
def create_event():
    form_data = request.form
    title = form_data['title']
    host = form_data['leader']
    avatar = form_data['avatar']
    description = form_data['description']
    start_time = form_data['start']
    event = {
        "Title": title,
        "Leader": host,
        "Avatar": [{"url": avatar}],
        "Description": description,
        "Start Time": start_time
    }
    
    return event


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
