import pyttsx3
import speech_recognition as sr
from datetime import datetime
import random
import webbrowser
from difflib import get_close_matches
from rapidfuzz import fuzz


# 🔥 Updated CT College Data (Directly Inside Code)
qa_data = {
    "your name": "I am Vision, your college assistant.",
    "yourself": "I am Vision, your college assistant.",
    "introduce": "I am Vision, here to answer your queries of CT",
    "full form": "full form of CT is Career Transformation",
    "developed":"I am developed by B tech 6th semester students as a part of there academic project.",
    "college location": "CT Group of Institutions, North Campus, Maqsudan, Jalandhar.",
    "chairman": "Mr. Charanjit Singh Channi.",
    "md": "Dr. Manbir Singh.",
    "director": "The director of CT North Campus is Dr. Anurag Sharma.",
    "placement head": "Mr. Sandeep Sharma and Ms. Jasdeep.",
    "courses provided": "B.Tech in CSE, AI, CS, ECE, BTTM, BCA, BSc, BCom, Multimedia and Animation.",
    "number of departments": "There are four major departments - CSE, AI, CS, and ECE.",
    "class timing": "Classes run from 9 AM to 4 PM.",
    "hod of cse": "E R. Inderpal Singh",
    "hod of ai": "E R. Inderpal Singh",
    "hod of cs": "E R. Inderpal Singh",
    "hod of ece": "Handled by E R. Karuna",
    "hod of multimedia": "Ms. Diksha.",
    "hod of business": "Dr. Raman Gautam.",
    "hod of tourism and hotel": "Mr. Ratan.",
    "cse faculty members": "Er. Karuna, Er. Inderpal Singh, Er. Ramandeep Kaur.",
    "math": "Ms. Nisha.",
    "coding club": "The Coding Club is TechFusion, headed by Student President Suleman.",
    "fest details": "CT Group organizes 'Colors' (Intercollege Fest), 'Kshitij' (Interdepartmental Fest), and 'Technovanza' (CTITR event).",
    "crs of btech cse 4th year": "Anandita and Suleman are the CRs of B.Tech CSE 4th Year.",
    "crs of btech cse 3rd year": "Mehak and Raghav are the CRs of B.Tech CSE 3rd Year.",
    "crs of btech cse 2nd year": "Vanisha and Shyam are the CRs of B.Tech CSE 2nd Year.",
    "crs of btech cse 1st year": "Yet to be decided.",
    "available clubs": "TechFusion (Coding Club), Arts Club, Sports Club, Cultural Club.",
    "hostel facility": "Yes, CT Group provides hostel facilities for boys and girls separately.",
    "canteen facility": "Yes, there is a canteen available with hygienic food at reasonable prices.",
    "transport facility": "Yes, CT Group provides transportation facilities from different locations.",
    "library timings": "The library remains open from 8:30 AM to 5:30 PM on working days.",
    "sports facilities": "CT Group offers sports facilities like cricket, basketball, volleyball, badminton, and indoor games.",
    "internship opportunities": "Yes, CT Group helps students with internship opportunities through placement cell and tie-ups.",
    "placement companies": "Major recruiters include Infosys, Wipro, TCS, Tech Mahindra, Amazon, Cognizant, etc.",
    "uniform requirement": "Yes, students must wear the prescribed college uniform on designated days.",
    "attendance criteria": "A minimum of 75% attendance is required to be eligible for exams.",
    "scholarships available": "Yes, CT Group provides merit-based and need-based scholarships.",
    "college website": "Visit the official website: https://www.ctgroup.in/",
    "contact number": "You can contact CT Group at +91-12345678.",
    "admission office": "The admission cell is located in the main building, ground floor.",
    "events organized": "Colours, Technovenza, kshitij, diwali Fest, Blood Donation Camps, and various Workshops.",
    "industrial visits": "Yes, regular industrial visits are organized for practical exposure."
}

def get_best_match(user_input):
    best_match = None
    highest_score = 0

    for question in qa_data.keys():
        score = fuzz.partial_ratio(user_input.lower(), question.lower())
        if score > highest_score:
            highest_score = score
            best_match = question

    if highest_score >= 60:  # threshold (you can adjust)
        return qa_data[best_match]
    else:
        return None

# 🔊 Text-to-speech
def speak(text, rate=150):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

# 🌐 Web search
def web_search(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"I found these results for {query}"
    except Exception as e:
        return f"Sorry, I couldn't perform the search: {str(e)}"

# 💬 Smart response
def get_response(user_input):
    user_input = user_input.lower().strip("?.,!")

    

    # Handle special commands like adding questions
    if user_input.startswith("add question"):
        try:
            parts = user_input.split("answer")
            if len(parts) == 2:
                question = parts[0].replace("add question", "").strip()
                answer = parts[1].strip()
                update_qa_data(question, answer)
                return "I've saved the new question and answer!"
            else:
                return "Please provide both a question and an answer."
        except Exception as e:
            return f"Error processing your request: {str(e)}"

    # Dynamic responses
    if not user_input:
        return "I didn't hear that. Could you please repeat?"

    time_triggers = ["time", "what time is it", "current time"]
    if any(trigger in user_input for trigger in time_triggers):
        return "The current time is " + datetime.now().strftime("%I:%M %p on %A, %B %d")

    date_triggers = ["date", "today's date", "what day is it"]
    if any(trigger in user_input for trigger in date_triggers):
        return "Today is " + datetime.now().strftime("%A, %B %d, %Y")

    greeting_triggers = ["hi", "hello", "hey", "greetings"]
    if any(trigger in user_input for trigger in greeting_triggers):
        return random.choice(["Hello there!", "Hi! How can I help?", "Greetings!"])

    if "thank you" in user_input:
        return random.choice(["You're welcome!", "My pleasure!", "Happy to help!"])

    if any(word in user_input for word in ["bye", "exit", "goodbye"]):
        return random.choice(["Goodbye! Have a great day!", "See you later!", "Bye! Come back soon!"])

    if "search for" in user_input or "look up" in user_input:
        query = user_input.replace("search for", "").replace("look up", "").strip()
        return web_search(query)

    # --- SMARTER fuzzy matching ---
    user_words = set(user_input.split())

    best_match = None
    highest_score = 0

    for question in qa_data.keys():
        question_words = set(question.split())
        common_words = user_words.intersection(question_words)
        score = len(common_words)

        if score > highest_score:
            highest_score = score
            best_match = question

    if highest_score >= 1:  # minimum 1 common word
        return qa_data[best_match]

    # If no good match, fallback
    return "I'm not sure about that. Could you try asking differently or ask me to search the web?"

# 🎙️ Voice recognition
def correct_text(user_text):
    # Try to correct common important keywords
    words = user_text.lower().split()
    corrected_words = []
    for word in words:
        close = get_close_matches(word, [w for q in qa_data.keys() for w in q.split()], n=1, cutoff=0.8)
        corrected_words.append(close[0] if close else word)
    return ' '.join(corrected_words)

def listen_and_respond():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now or say 'exit' to quit)")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            user_text = r.recognize_google(audio)
            user_text = correct_text(user_text)  # ✨ Correct minor speech errors
            print(f"You: {user_text}")
            
            reply = get_response(user_text)
            print(f"Vision: {reply}")
            speak(reply)
            
            if any(word in user_text.lower() for word in ["bye", "exit", "goodbye", "bye bye", "dhanaywad"]):
                return False
            return True
        except sr.WaitTimeoutError:
            print("⌛ Listening timed out. Try again.")
            return True
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            speak("Sorry, I didn't catch that. Could you repeat?")
            return True
        except sr.RequestError as e:
            print(f"⚠️ Speech service error: {e}")
            speak("I'm having trouble with the speech service. Let's try again.")
            return True
        except Exception as e:
            print(f"Unexpected error: {e}")
            return True
# 📝 Text input
def text_input_mode():
    print("\n📝 Text input mode activated. Type your questions or 'exit' to quit.")
    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
            
        reply = get_response(user_text)
        print(f"Vision: {reply}")
        speak(reply)
        
        if any(word in user_text.lower() for word in ["bye", "exit", "goodbye"]):
            break

# 🏁 Main
def main():
    print("""
    🤖 Vision College Assistant
    ---------------------------
    Choose interaction mode:
    1. Voice mode
    2. Text mode
    3. Exit
    """)
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🔊 Voice mode activated. Say 'exit' to return to menu.")
            speak("Voice mode activated. How can I help you?")
            while listen_and_respond():
                pass
        elif choice == "2":
            text_input_mode()
        elif choice == "3":
            print("Goodbye!")
            speak("Goodbye! Have a wonderful day!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
