import os
import asyncio
from flask import Flask, request, jsonify
from pymongo import MongoClient
from groq import Groq
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


client = MongoClient(
    host="localhost",
    port=27017,
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    authSource="admin"
)
db         = client["ai_project"]

prompts_col = db["prompts"]
history_col = db["history"]


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-8b-instant"


#  Helpers 

def get_prompt_template(prompt_id: str = "Education_Prompt") -> str:
    """Fetch a prompt template from MongoDB by _id."""
    doc = prompts_col.find_one({"_id": prompt_id})
    if not doc:
        raise ValueError(f"Prompt template '{prompt_id}' not found in DB.")
    return doc["template"]


def call_groq(final_prompt: str) -> str:
    """Send a single prompt to the Groq API and return the text response."""
    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": final_prompt}],
    )
    return completion.choices[0].message.content


def save_history(user_input: str, ai_response: str) -> None:
    """Persist a request/response pair to the history collection."""
    history_col.insert_one({
        "userInput":  user_input,
        "response":   ai_response,
        "created_at": datetime.now(timezone.utc),
    })


@app.route("/")
def home():
    return "AI Prompt Management System Running Successfully"

@app.route("/seed")
def seed():

    doc = {
        "_id": "Education_Prompt",
        "template": "You are an expert in education domain. Answer the following: {{userInput}}"
    }

    prompts_col.replace_one(
        {"_id": "Education_Prompt"},
        doc,
        upsert=True
    )

    return "Prompt got Seeded Successfully"

@app.route("/test")
def test():

    template = get_prompt_template()

    final_prompt = template.replace(
        "{{userInput}}",
        "What is DBMS?"
    )

    response = call_groq(final_prompt)

    return response


#  Route 1 – single userInput

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data or "userInput" not in data:
        return jsonify({"error": "'userInput' field is required."}), 400

    user_input = data["userInput"].strip()
    if not user_input:
        return jsonify({"error": "'userInput' cannot be empty."}), 400

    try:
        template     = get_prompt_template("Education_Prompt")
        final_prompt = template.replace("{{userInput}}", user_input)
        ai_response  = call_groq(final_prompt)
        save_history(user_input, ai_response)
        return jsonify({"response": ai_response}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


#  Route 2 – list of userInputs (async) 

async def process_single(user_input: str, template: str) -> str:
    """Async wrapper: build prompt and call Groq for one input string."""
    final_prompt = template.replace("{{userInput}}", user_input)
    loop         = asyncio.get_event_loop()
    ai_response  = await loop.run_in_executor(None, call_groq, final_prompt)
    save_history(user_input, ai_response)
    return ai_response


async def process_all(inputs: list[str], template: str) -> list[str]:
    """Process all inputs concurrently while keep the order."""
    tasks = [process_single(inp, template) for inp in inputs]
    return await asyncio.gather(*tasks)


@app.route("/ask-batch", methods=["POST"])
def ask_batch():
    """
    POST /ask-batch
    Body: { "userInputs": ["question 1", "question 2", ...] }
    Returns: { "responses": ["answer 1", "answer 2", ...] }
    """
    data = request.get_json(silent=True)
    if not data or "userInputs" not in data:
        return jsonify({"error": "'userInputs' field is required."}), 400

    user_inputs = data["userInputs"]
    if not isinstance(user_inputs, list) or len(user_inputs) == 0:
        return jsonify({"error": "'userInputs' must be a non-empty list of strings."}), 400

    cleaned = [s.strip() for s in user_inputs if isinstance(s, str) and s.strip()]
    if not cleaned:
        return jsonify({"error": "No valid strings found in 'userInputs'."}), 400

    try:
        template  = get_prompt_template("Education_Prompt")
        responses = asyncio.run(process_all(cleaned, template))
        return jsonify({"responses": responses}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


#  Seed endpoint (for convenience)

@app.route("/seed-prompt", methods=["POST"])
def seed_prompt():
    """
    POST /seed-prompt
    Inserts (or updates) the Education_Prompt document in the prompts collection.
    """
    doc = {
        "_id":      "Education_Prompt",
        "template": "You are an expert in education domain. Answer the following: {{userInput}}",
    }
    prompts_col.replace_one({"_id": "Education_Prompt"}, doc, upsert=True)
    return jsonify({"message": "Education_Prompt seeded successfully.", "document": doc}), 201

# run

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)
