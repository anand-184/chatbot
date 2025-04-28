import pyttsx3
import speech_recognition as sr

# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to get chatbot response
def get_response(user_input):
    # Simple rule-based responses (replace with OpenAI or chatbot logic)
    if "hello" in user_input.lower():
     return "Hi there! How can I help you today?"
    elif "your name" in user_input.lower():
     return "I am your AI chatbot with speech. My name is Vision."
    elif "how are you" in user_input.lower():
     return "I'm just code, but I'm doing great! Thanks for asking."
    elif "what can you do" in user_input.lower():
     return "I can chat with you, answer questions, and help with basic tasks."
    elif "who created you" in user_input.lower():
     return "I was created by developer using Python and a bit of AI magic."
    elif "tell me a joke" in user_input.lower():
     return "Why don’t scientists trust atoms? Because they make up everything!"
    elif "what is python" in user_input.lower():
     return "Python is a high-level programming language known for its readability and versatility."
    elif "bye" in user_input.lower():
     return "Goodbye! Have a great day!"
    elif "thank you" in user_input.lower():
     return "You're welcome!"
    elif "what is ai" in user_input.lower():
     return "AI stands for Artificial Intelligence. It's about making machines think and learn like humans."
    elif "what is your purpose" in user_input.lower():
     return "My purpose is to help you by providing quick and helpful responses."
    elif "what's the time" in user_input.lower():
     from datetime import datetime
     return "The current time is " + datetime.now().strftime("%H:%M:%S") 
    elif "open google" in user_input.lower():
     return "Please open your browser and go to https://www.google.com"
    elif "who is elon musk" in user_input.lower():
     return "Elon Musk is a tech entrepreneur known for founding Tesla, SpaceX, and more."
    elif "what is the capital of france" in user_input.lower():
     return "The capital of France is Paris."
    elif "do you speak other languages" in user_input.lower():
     return "Right now, I understand English. More languages may come soon!"
    elif "what's the weather like" in user_input.lower():
     return "I'm not connected to live weather data, but you can check your local weather app."
    elif "can you sing" in user_input.lower():
     return "I can't sing, but I can tell you lyrics or music trivia!"
    elif "who is the president of usa" in user_input.lower():
     return "As of my latest update, it's Joe Biden."
    elif "how old are you" in user_input.lower():
     return "I'm timeless. But I was created recently!"
    elif "are you real" in user_input.lower():
     return "I'm real in the digital world!"
    elif "can you help me with homework" in user_input.lower():
     return "Sure! What subject do you need help with?"
    else:
     return "Sorry, I didn't understand that."


# Function to recognize speech input from the user
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Say something!")
        audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

# Main function to drive the chatbot
def main():
    print("AI Chatbot (Say 'exit' to quit)")
    while True:
        user_input = listen()  # Get speech input
        if user_input and "exit" in user_input.lower():
            print("Exiting the chatbot...")
            break
        elif user_input:
            response = get_response(user_input)
            print("Bot:", response)
            speak(response)

if __name__ == "__main__":
    main()
