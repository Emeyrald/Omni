# Omni - Personal Voice Assistant
Omni is a Python-based personal voice assistant that responds to spoken commands, performs web searches, manages applications, and keeps logs. Built with speech_recognition, pyttsx3, wolframalpha, and other Python libraries, Omni provides a flexible and extendable voice interface for your computer.

This is a personal project I worked on around 3 years ago, and then updated it to get it working as of 11/4/2025. I always wanted some sort of Jarvis-like AI, so I came up with something that's similar in function, since it can do different tasks for me, but less difficult than making a full blown AI.  

This project is fully in python.

### Features
* Voice-Activated Commands: Use a single activation word (omni) to trigger commands.
* Text-to-Speech: Omni speaks responses and confirmations using pyttsx3.
* Web Navigation: Open websites directly in Chrome via voice.
* Application Management: Open and close apps using voice commands.
* Note Logging: Take voice notes that are automatically saved with timestamps.
* Information Retrieval: Search Wikipedia or WolframAlpha for answers.
* System Commands: Shutdown or restart the computer via voice.

### Dependencies:
* SpeechRecognition
* PyAudio
* pyttsx3
* wikipedia
* wolframalpha
* AppOpener
* psutil  
  
### Usage  
Run the assistant:  
```python Omni.py```
Omni will announce that it is online. Speak commands starting with the activation word:  

```"Omni, say hello"``` - Repeats what you say back to you  
```"Omni, go to youtube.com"``` - Opens any website in your browser  
```"Omni, log something for me"``` - Asks for the title, and then contents of a log, then saves it as a text file  
```"Omni, open discord"``` - Opens most applications  
```"Omni, calculate 5 + 7"``` - Can calculate anything using WolframAlpha API, including advanced math and distances between locations. 
```"Omni, look up the Pythagorean Theroem"``` - Can look up anything on wikipedia and say the results to you  
```"Omni, shut down"``` - Shuts down your computer  
```"Omni, restart"``` - Restarts your computer  

Logs are saved in the Logs folder with timestamped filenames. The Logs folder is created automatically when you first use the command to log something.

To exit:  
```"Omni, that's all for now"```
