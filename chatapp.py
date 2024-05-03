import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import pickle
import numpy as np
import json
import random
import tkinter
from tkinter import *

# Load the model and necessary data
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl','rb'))

# Define functions for cleaning up sentences, generating bag of words, and predicting classes
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res





# best
from tkinter import *
import random

# Creating GUI with tkinter
base = Tk()
base.title("BitBuddy")
base.minsize(400, 300)  # Set minimum resolution
base.geometry("1000x700")  # Adjusted resolution to 640x480
base.resizable(width=True, height=True)  # Allowing resizing in both directions

# Function to send a message
def send(event=None):  # Modified to accept an event argument
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#3C6478", font=("Verdana", 12 ))
        # Call the chatbot_response function to get the bot's response
        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

# Function to change the theme
def change_theme():
    theme = f"#{random.randint(0, 0xFFFFFF):06x}"
    base.config(bg=theme)
    ChatLog.config(bg="white")
    scrollbar.config(bg=theme)
    SendButton.config(bg="#32de97", activebackground="#3c9d9b")
    EntryBox.config(bg="white")

# Function to clear the chat
def clear_chat():
    ChatLog.config(state=NORMAL)
    ChatLog.delete(1.0, END)
    ChatLog.config(state=DISABLED)

# # FUntion to remove bg image
# def remove_background():
#     bg_label.place_forget()


# # Background image
# bg_image = PhotoImage(file="assets/bit_logo.png")
# bg_label = Label(base, image=bg_image)
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# # Action button
# action_button = Button(base, text="Remove Background", command=remove_background)
# action_button.pack()



# Text widget to display the chat log
ChatLog = Text(base, bd=0, bg="lightgray", height=20, width=70, font="Arial")
ChatLog.config(state=DISABLED)

# Scrollbar for the chat log
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Entry widget for user input
EntryBox = Text(base, bd=0, bg="white", height=5, width=47, font="Arial")

# Button to send the message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command=send)

# Button to clear the chat
ClearButton = Button(base, font=("Verdana",12,'bold'), text="Clear Chat", bd=0, bg="#FF5733", activebackground="#FF5733",fg='#ffffff', command=clear_chat)

# Button to change the theme to a random color
ThemeButton = Button(base, font=("Verdana",12,'bold'), text="Change Theme", bd=0, bg="#3371FF", activebackground="#3371FF",fg='#ffffff', command=change_theme)

# Bind the Return key to the send function
base.bind('<Return>', send)

# Place widgets on the window
ChatLog.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
# Place the scrollbar on the right side of the ChatLog and span it across all rows
scrollbar.grid(row=0, column=3, rowspan=3, sticky="ns", pady=5)
EntryBox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
SendButton.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
ClearButton.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
ThemeButton.grid(row=1, column=2, padx=(0,10), pady=5)


# Configure grid weights to make the chat log and entry box stretchable
base.grid_rowconfigure(0, weight=1)
base.grid_rowconfigure(1, weight=1)
base.grid_columnconfigure(0, weight=1)
base.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
base.mainloop()
