from flask import Flask, request, render_template_string
from ollama import chat
import serial

arduino = serial.Serial("COM9", 9600, timeout=1)

SYSTEM = """
Convert user requests into commands.

Allowed commands only:

ON
OFF
BLINK (and numer which is delay time, f.e. BLINK 200 if user want to blink 200)

Rules:
- blink -> BLINK and appropriate number
- turn on -> ON
- turn off -> OFF
- if user want to do sth else don't send anything -> NONE
- if user want ot blink slow -> BLINK 500
- if user want ot blink medium -> BLINK 300
- if user want ot blink very slow -> BLINK 1000
- if user want ot blink very fast -> BLINK 50

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

    <p class="text-gray-300 mb-4 whitespace-nowrap">
      LED supports ON, OFF and BLINK with adjustable speed
    </p>

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
      Connected to Arduino via USB (COM9)
    </p>

  </div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

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
            print("FINAL:", cmd)

            arduino.write((cmd + "\n").encode())

            response = cmd

        except Exception as e:
            print("ERROR:", e)
            response = "ERROR"

    return render_template_string(HTML, response=response)

app.run(debug=True, use_reloader=False)