from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
from AppOpener import run
import psutil
import wikipedia
import wolframalpha
import os

#Save file creation
relDirectory = os.getcwd()
if (os.path.exists(relDirectory + "/save.txt")):
    f = open(relDirectory + "/save.txt", "r")
    if (f.read(1) == "1"):
        f.close()
else:
    with open(relDirectory + "/save.txt", "w") as newFile:
        newFile.write("1")

# Speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id) # 0 = male, 1 = female
activationWord = "omni" # Single word

# Configure browser
# Set the path
chrome_path = r"C:/Program Files/Google/Chrome/Application/chrome"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

# Wolfram Alpha client
appId = "R9EU5Q-Q2EU8V3WQG"
wolframClient = wolframalpha.Client(appId)

def search_wikipedia(query = ""):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No wikipedia result")
        return "No result recieved"
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]["plaintext"]
    else:
        return var["plaintext"]

def search_wolframAlpha(query = ""):
    response = wolframClient.query(query)

    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods
    if response["@success"] == "false":
        return "Calculation failed."

    # Query resolved
    else:
        result = ""
        # Question
        pod0 = response["pod"][0]

        pod1 = response["pod"][1]
        # May contain the answer, has the highest confidence value
        # If it's primary, or has the title of result or definition, then it's the official result
        if (("result") in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or ("definition" in pod1["@title"].lower()):
            # Get the result
            result = listOrDict(pod1["subpod"])
            # Remove the bracketed section
            return result.split("(")[0]
        else:
            question = listOrDict(pod0["subpod"])
            # Remove the bracketed section
            return question.split("(")[0]
            # Search wikipedia instead
            speak("Calculation failed. Looking through wikipedia")
            return search_wikipedia(question)

def close_app(app_name):
    running_apps=psutil.process_iter(['pid','name']) #returns names of running processes
    found=False
    for app in running_apps:
        sys_app=app.info.get('name').split('.')[0].lower()

        if sys_app in app_name.split() or app_name in sys_app:
            pid=app.info.get('pid') #returns PID of the given app if found running
            
            try:
                app_pid = psutil.Process(pid)
                app_pid.terminate()
                found=True
            except: pass
            
        else: pass
    if not found:
        speak(app_name + " is not currently running sir")
    else:
        speak(app_name + " has been closed sir")

def speak(text, rate = 180):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        listener.pause_threshold = 1
        print("Listening for a command...")

        try:
            audio = listener.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out, try again.")
            return "None"
    try:
        query = listener.recognize_google(audio, language="en_US")
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return "None"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return "None"

# Main loop
if __name__ == "__main__":
    speak("Systems booting up. All systems online. Good day Sir.")

    while True:
        # Parse as a list
        words = parseCommand().lower().split()
        query = []
        if activationWord in words:
            index = words.index(activationWord)
            for i in range(index, len(words)):
                query.append(words[i])
            query.pop(0)

            # List commands
            if query[0] == "say":
                if "hello" in query:
                    speak("Hello Sir.")
                else:
                    query.pop(0) # Remove say
                    speech = " ".join(query)
                    speak(speech)
            
            # Navigation
            if query[0] == "go" and query[1] == "to":
                speak("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            # Note taking
            if query[0] == "log":
                speak("What would you like this log to be titled?")
                title = parseCommand().lower()
                speak("Ready to log Sir.")
                newNote = parseCommand().lower()
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H-%M-%S")
                # Make sure Logs folder exists
                logs_folder = os.path.join(relDirectory, "Logs")
                os.makedirs(logs_folder, exist_ok=True)  # Creates folder if it doesn't exist
                # Save the log
                log_path = os.path.join(logs_folder, f"{title}---{date}.txt")
                with open(log_path, "w") as newFile:
                    newFile.write(f"{time} - {newNote}")
                speak("Log saved in: " + log_path)

            if query[0] == "that's":
                speak("Goodbye Sir. Have a good day.")
                exit()

            if query[0] == "open":
                speak("Opening...")
                query = " ".join(query[1:]).lower()
                try:
                    run(query)
                except:
                    speak("Sir, please clairfy what you want to open")

            if  query[0] == "close":
                query = " ".join(query[1:]).lower()
                close_app(query)

            # Wikipedia
            if query[0] == "look" and query[1] == "up":
                query = " ".join(query[1:])
                speak("Looking through wikipedia.")
                speak(search_wikipedia(query))

            # Wolfram Alpha
            if query[0] == "calculate":
                query = " ".join(query[1:])
                speak("Calculating...")
                try:
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak("Sir, I am unable to calculate that.")

            if (query[0] == "shutdown") or (query[0] == "shut" and query[1] == "down"):
                speak("Yes sir, shutting down.")
                os.system("shutdown /s /t 1")

            if query[0] == "restart":
                speak("Yes sir, restarting.")
                os.system("restart /s /t 1")