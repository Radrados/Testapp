import openai
from flask import Flask, request, Response
import asyncio
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_gpt3_response(prompt):
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

app = Flask(__name__)
SETTINGS = BotFrameworkAdapterSettings("3e266b58-95b1-4304-af09-278948d577cd", "549b3080-5c26-413c-8c6f-503cb533f0f4")  # We'll populate this soon
ADAPTER = BotFrameworkAdapter(SETTINGS)
LOOP = asyncio.get_event_loop()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    try:
        task = LOOP.create_task(
            ADAPTER.process_activity(activity, auth_header, bot_logic)
        )
        LOOP.run_until_complete(task)
        return Response(status=201)
    except Exception as exception:
        raise exception

async def bot_logic(turn_context: TurnContext):
    if turn_context.activity.type == "message":
        user_message = turn_context.activity.text
        gpt3_response = get_gpt3_response(user_message)
        await turn_context.send_activity(gpt3_response)

if __name__ == '__main__':
    app.run(port=3978)
