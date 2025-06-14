import requests
import yaml
from flask import Flask, request, jsonify

class IngredientsAwareness:
    def __init__(self):
        pass

    def chat(self, message: str) -> str:

        self.api_key = "6TPQHX6-K6J4035-N611BBS-NK8ZMYX"
        self.base_url = "http://localhost:3001/api/v1"
        self.workspace_slug = "ingredients_awareness"

        self.chat_url = f"{self.base_url}/workspace/{self.workspace_slug}/chat"

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

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
