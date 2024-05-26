#Final app.py 
#import files
from flask import Flask, render_template, request
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from flask import Flask, jsonify
import json
import pdb

app = Flask(__name__)
api_key = "JbM16I0jbrkuzJLfEG0lnFqAsLI1Ffhd"

def flight_recommandation(Departure, Destination):
    user_message = (
        f"""
        Act as a trip advisor and provide me with the most eco-friendly travel plan for a trip from {Departure} to {Destination}. 
        Return the response in JSON format
        Include the cheapest flights available and provide an explanation why you choose these flights in an eco friendly way. Please structure the response as follows in Json:

        The three most eco-friendly airlines for this route are : 
        
        Airline : This field should be a string object containing the name of the AirLine
        departure_date_time :string for departure  date and time in ISO Format like this : "2022-10-02T07:00:00"
        arrival_date_time :string for arrival  date and time in ISO Format like this : "2022-10-02T07:00:00"
        departure_Airport: This should be a string containing the name of the departure Airport.
        arrival_Airport: This should be a string containing the name of the arrival Airport.
        explanation: string containing the explanation about advantages of choosing this flight in ecology
        
        

        """
    )
    return user_message

def run_mistral(user_message, model="mistral-large-latest"):
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="user", content=user_message)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages,

    )
    return (chat_response.choices[0].message.content)

    print(run_mistral(flight_recommandation(
    "Paris", "Lisbon"
)))



def run_mistral(user_message, model="mistral-medium"):
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="user", content=user_message)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages

    )
    return (chat_response.choices[0].message.content)




@app.route("/")
def home():    
    return render_template("index.html")


@app.route("/get")
def get_bot_response():  
    print('aaaa')  
    home = request.args.get('home')
    destination = request.args.get('destination')
    
    # Make the API call to get the response
    response = run_mistral(flight_recommandation(home, destination))
    last_brace_index = response.rfind('}')
    response = response[:last_brace_index + 1] 
    response = response.replace('\\', '') 
    print(response)
    # Check if response is valid JSON
    data = json.loads(response)

    # Extract the list of flights
    flights = data.get('flights', [])

    # Extract each flight as a list of its attributes
    flight_lists = []
    for flight in flights:
        flight_list = [flight[attr] for attr in flight]
        flight_lists.append(flight_list)
    print(flight_lists)

    return jsonify(flight_lists)









if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()