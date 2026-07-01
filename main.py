import webbrowser
import pyttsx3
import os
import datetime
import yt_dlp
import time
import psutil
import pyautogui
import pywhatkit
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)  



genai.configure(api_key="AIzaSyBaoIgnLCpETz_1LMlKteGexVpJedvschs")  
model = genai.GenerativeModel("gemini-2.5-flash")


engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)

def speak(text):
    print("Jarvis:", text)
    try:
        engine.stop()
        if len(text) > 200:
            text = text[:200]
        engine.say(text)
        engine.runAndWait()
    except:
        pass  


def ask_gemini(question):
    try:
        prompt = f"""
        You are Jarvis, a smart AI assistant.
        Never say you are trained by Google.
        Speak like futuristic AI assistant Jarvis.
        Keep answers short but intelligent.
        Be confident and professional.

        User: {question}
        Jarvis:
        """

        response = model.generate_content(prompt)

        print("RAW RESPONSE:", response)  # DEBUG

        if response and hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text
        else:
            return "No response from AI"

    except Exception as e:
        print(" GEMINI ERROR:", e)
        return "AI not working"


def handleCommand(command):
    command = command.lower()

    # Websites
    if "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook"

    # Play on YouTube
    elif "play" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()

        if song:
            speak(f"Playing {song}")

            try:
                ydl_opts = {
                    "quiet": True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch1:{song}", download=False)
                    video_url = info['entries'][0]['webpage_url']

                webbrowser.open(video_url)

                return f"Playing {song} on YouTube"

            except Exception as e:
                print("YouTube Error:", e)
                return "Sorry, I couldn't find the video"

    # Open any app
    elif command.startswith("open"):
        app_name = command.replace("open", "").strip()

        speak(f"Opening {app_name}")

        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(1)
        pyautogui.press('enter')

        return f"Opening {app_name}"
    
    #Search n Google
    elif "search" in command:
        search_query = command.replace("search", "").strip()

        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return f"Searching {search_query} on Google"
    
    #Opening a Website
    elif "open" in command and ".com" in command:
        site = command.replace("open", "").strip()
        webbrowser.open(f"https://{site}")
        return f"Opening {site}"
  
    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}"

    # Battery
    elif "battery" in command:
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged

        if plugged:
            return f"Battery is {percent} percent and charging"
        else:
            return f"Battery is {percent} percent"
    
    # System controls
    elif "shutdown" in command:
        os.system("shutdown /s /t 5")
        return "Shutting down in 5 seconds"

    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Restarting in 5 seconds"

    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Going to sleep"

    elif "lock" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking the system"

    # Volume
    elif "volume up" in command:
        for _ in range(10):
            pyautogui.press("volumeup")
        return "Increasing volume"

    elif "volume down" in command:
        for _ in range(10):
            pyautogui.press("volumedown")
        return "Decreasing volume"

    elif "mute" in command:
        pyautogui.press("volumemute")
        return "Muting volume"

    # Screenshot
    elif " take screenshot" in command:
        img = pyautogui.screenshot()
        filename = f"screenshot_{int(time.time())}.png"
        img.save(filename)
        return f"Screenshot saved as {filename}"
    
    #Minimize/ Close Window
    elif "minimize window" in command:
        pyautogui.hotkey('win', 'down')
        return "Minimizing window"

    elif "close window" in command:
        pyautogui.hotkey('alt', 'f4')
        return "Closing window"

    #Whatsapp Message
    elif "send whatsapp message" in command:

        try:
        
        # send whatsapp message to rahul saying hello

            text = command.replace(
            "send whatsapp message to",
            ""
            ).strip()

            name, message = text.split("saying")

            name = name.strip()
            message = message.strip()

            speak(f"Sending message to {name}")

            # OPEN WHATSAPP USING WINDOWS SEARCH
            pyautogui.press('win')
            time.sleep(1)

            pyautogui.write('WhatsApp')
            time.sleep(2)

            pyautogui.press('enter')

            # WAIT FOR WHATSAPP TO OPEN
            time.sleep(8)

            # SEARCH CONTACT
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1)

            pyautogui.write(name, interval=0.1)
            time.sleep(2)

            pyautogui.press('enter')
            time.sleep(1)

            # TYPE MESSAGE
            pyautogui.write(message, interval=0.05)

            time.sleep(1)

            # SEND MESSAGE
            pyautogui.press('enter')

            return f"Message sent to {name}"

        except Exception as e:
            print("WHATSAPP ERROR:", e)
            return "Failed to send WhatsApp message"

    # Exit
    elif "exit" in command or "stop" in command:
        return "Goodbye Sir"

    # Gemini AI fallback
    else:
        reply = ask_gemini(command)
        return reply
    


@app.route("/command", methods=["POST"])
def command():
    data = request.json
    user_command = data.get("command")

    print("User:", user_command)

    response_text = handleCommand(user_command)

    
    speak(response_text)

    return jsonify({"reply": response_text})


if __name__ == "__main__":
    print("Jarvis Backend Running on http://127.0.0.1:5000")
    app.run(debug=True)
    speak("Jarvis AI system activated")