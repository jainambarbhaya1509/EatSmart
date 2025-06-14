import requests
import yaml
from flask import Flask, request, jsonify

class IngredientsAwareness:
    def __init__(self):
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)

        self.api_key = config["api_key"]
        self.base_url = config["model_server_base_url"]
        self.workspace_slug = config["workspace_slug"]

        self.chat_url = f"{self.base_url}/workspace/{self.workspace_slug}/chat"

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

    def chat(self, message: str) -> str:
        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": []
        }
        chat_response = requests.post(
            self.chat_url,
            headers=self.headers,
            json=data
        )
        try:
            return chat_response.json()["textResponse"]
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"

app = Flask(__name__)
ingredientsAwareness = IngredientsAwareness()

@app.route("/ingredients-awareness", methods=["POST"])
def ingredients_awareness():
    data = request.get_json()
    message = data.get("message", "")
    response = ingredientsAwareness.chat(message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
