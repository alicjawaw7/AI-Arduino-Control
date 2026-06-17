from flask import Flask, request, render_template_string
from ollama import chat
import serial

DEMO_MODE = False

arduino = None

if not DEMO_MODE:
    try:
        arduino = serial.Serial("COM9", 9600, timeout=1)
    except Exception as e:
        print("Arduino not connected:", e)
        arduino = None


SYSTEM = """
Convert user requests into commands.

Allowed commands only:

ON
OFF
BLINK <number>

Rules:
- turn on -> ON
- turn off -> OFF
- blink slow -> BLINK 500
- blink medium -> BLINK 300
- blink very slow -> BLINK 1000
- blink very fast -> BLINK 50
- if nothing valid -> NONE

Return ONLY ONE command.
No explanations.
"""


app = Flask(__name__)


HTML = """
<!doctype html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-900 text-white flex items-center justify-center h-screen">

  <div class="bg-gray-800 p-6 rounded-2xl shadow-xl w-[500px]">

    <h1 class="text-xl font-bold mb-4">AI Arduino</h1>

    <form method="POST" class="flex gap-2">
      <input name="text"
             autocomplete="off"
             class="flex-1 p-2 rounded bg-gray-700 text-white"
             placeholder="Write command">

      <button class="bg-blue-600 px-4 rounded">
        Send
      </button>
    </form>

    <p class="mt-4 text-green-400">AI: {{response}}</p>

    <p class="mt-6 text-sm text-gray-500">
      Mode: {{mode}}
    </p>

  </div>

</body>
</html>
"""


def send_to_arduino(cmd):
    if DEMO_MODE:
        print(f"[DEMO] {cmd}")
        return

    if arduino:
        try:
            arduino.write((cmd + "\n").encode())
        except Exception as e:
            print("Arduino write error:", e)
    else:
        print("Arduino not available")


@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    mode = "DEMO" if DEMO_MODE else "LIVE"

    if request.method == "POST":
        try:
            user = request.form["text"]

            res = chat(
                model="mistral",
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user}
                ],
                options={"temperature": 0}
            )

            cmd = res["message"]["content"]
            print("RAW:", cmd)

            cmd = cmd.strip().upper().split("\n")[0]

            if cmd != "NONE":
                send_to_arduino(cmd)

            response = cmd

        except Exception as e:
            print("ERROR:", e)
            response = "ERROR"

    return render_template_string(HTML, response=response, mode=mode)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
