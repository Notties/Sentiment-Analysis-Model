import pickle
from keras.models import Sequential, load_model
from pythainlp.tokenize import word_tokenize, Tokenizer
from pythainlp.corpus.common import thai_words
from keras.utils import pad_sequences
import numpy as np

# Preprocess the text
text = "ควย"
custom_tokenizer = Tokenizer(thai_words())

cleaned_text = custom_tokenizer.word_tokenize(text)  # Assuming `custom_tokenizer` is the tokenizer used during training

def encoding_doc(token, words):
    return(token.texts_to_sequences(words))

def padding_doc(encoded_doc, max_length):
   return(pad_sequences(encoded_doc, maxlen=max_length, padding="post"))

with open('C:/LabPython/cleaned_words.pkl', 'rb') as file:
    cleaned_words = pickle.load(file)
with open('C:/LabPython/output_tokenizer.pkl', 'rb') as file:
    output_tokenizer = pickle.load(file)
with open('C:/LabPython/tokenized_doc.pkl', 'rb') as file:
    tokenized_doc = pickle.load(file)
with open('C:/LabPython/train_word_tokenizer.pkl', 'rb') as file:
    train_word_tokenizer = pickle.load(file)
    
def max_length(words):
    return len(max(words, key=len))

max_length = max_length(tokenized_doc)

encoded_doc = encoding_doc(train_word_tokenizer, cleaned_words)
encoded_text = encoding_doc(train_word_tokenizer, [cleaned_text])
padded_text = padding_doc(encoded_text, max_length)
loaded_model = load_model('C:/LabPython/model2.h5')

# Make prediction
prediction = loaded_model.predict([padded_text, padded_text, padded_text])
predicted_class = np.argmax(prediction, axis=-1)

# Map the predicted class to sentiment label
label_dict = output_tokenizer.word_index

# Add a check to handle unknown sentiment labels
if predicted_class[0] in label_dict.values():
    sentiment_label = [key for key, value in label_dict.items() if value == predicted_class[0]][0]
else:
    sentiment_label = "Unknown"

# Get the prediction probability for the predicted class
predicted_prob = prediction[0][predicted_class[0]] * 100

# Print the predicted sentiment and the corresponding probability
print("Predicted Sentiment: ", sentiment_label)
print("Prediction Probability: {:.2f}%".format(predicted_prob))