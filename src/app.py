from flask import Flask, request, jsonify
import json
import jsonschema
from datetime import datetime
from src.models.message import Message

# import pywhatkit

app = Flask(__name__)


schema = {
    "type": "object",
    "properties": {
        "phone_number": {
            "type": "string"
        },
        "message_body": {
            "type": "string"
        },
        "time_hour": {
            "type": "integer",
            "minimum": 0,
            "maximum": 23
        },
        "time_minute": {
            "type": "integer",
            "minimum": 0,
            "maximum": 59
        },
        "wait_time": {
            "type": "integer",
            "minimum": 0
        },
        "tab_close": {
            "type": "boolean"
        },
        "close_time": {
            "type": "integer",
            "minimum": 0
        },
    },
    "required": ["phone_number", "message_body"]
}


@app.route("/", methods=['POST'])
def send_message():
    model = Message()
    if request.is_json:
        # json_data = request.get_json()
        try:
            data = json.loads(request.data)
            jsonschema.validate(data, schema)
            message = convert_json_into_message(data, model)
            return jsonify({"message": "JSON data is valid", "data": data, "message_to_send": message}), 200
        except json.JSONDecodeError as e:
            return jsonify({"error": "JSON Decode Error", "message": str(e)}), 400
        except jsonschema.exceptions.ValidationError as e:
            return jsonify({"error": "JSON Schema Validation Error", "message": str(e)}), 400
    else:
        return jsonify({"message": "Content type is not supported"}), 400


if __name__ == "__main__":
    app.run()


# pywhatkit.sendwhatmsg("", "", 00, 00, 15, True, 2)
def convert_json_into_message(data, model):
    try:
        model.phone_number = data['phone_number']
        model.message_body = data['message_body']

        if data.get('time_hour') is not None and data.get('time_minute') is not None:
            model.time_hour = data['time_hour']
            model.time_minute = data['time_minute']
        else:
            current_datetime = datetime.now()
            model.time_hour = current_datetime.hour
            model.time_minute = current_datetime.minute + 1

        if data.get('wait_time') is not None and data.get('tab_close') is not None and data.get('close_time') is not None:
            model.wait_time = data['wait_time']
            model.tab_close = data['tab_close']
            model.close_time = data['close_time']

        return vars(model)
    except:
        return {"error": "Error validating the request"}
