import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import random
import numpy as np
import tensorflow as tf

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Initialize lists
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Loop through intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize words in pattern
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # Add documents
        documents.append((word_list, intent['tag']))
        # Add to classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize words and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Remove duplicate classes
classes = sorted(list(set(classes)))

# Print statistics
print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

# Save words and classes to pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Convert training data to numpy arrays
train_x = np.array([i[0] for i in training])
train_y = np.array([i[1] for i in training])

# Define model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(train_y[0]), activation='softmax')
])

# Compile model
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save model
model.save('chatbot_model.h5')

print("Model trained and saved successfully!")
