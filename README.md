# AI-Arduino-Control

### WHAT IS IT?

A web application that allows users to control an Arduino LED using natural language commands.  
The AI model interprets the user's prompt and sends the appropriate command to the Arduino through a Python application.


### AVAILABLE COMMANDS:
- LED ON  
- LED OFF  
- BLINK (with adjustable speed)


### HOW DOES IT WORK?
1. The user enters a command on the website.
2. The AI model interprets the request and converts it into a specific instruction for the Arduino.
3. Python sends the command via serial communication.
4. The Arduino executes the command and controls the LED.


### TECHNOLOGIES:
- Python  
- Arduino  
- AI model (Mistral from Ollama)  
- Flask  


### ARDUINO CONNECTION:
- Communication: Serial (USB)
- Default port: COM9 (change in code if needed)
- Baud rate: 9600

### HOW TO RUN:

1. Install Python dependencies:
   pip install -r requirements.txt
   
3. Install Ollama:
   https://ollama.com

4. Download Mistral model:
   ollama run mistral

5. Connect Arduino via USB

6. Run the project:
   python main.py

7. Open browser:
   http://127.0.0.1:5000
