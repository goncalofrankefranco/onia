import os
import json
import random
import nltk
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm

# MODEL: Setup
class ChatbotModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(ChatbotModel, self).__init__()

        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5) # Regularization

    # Actual functioning
    def forward(self, x):
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.fc3(x)

        return x

class ChatbotAssistant:
    def __init__(self, intents_path, function_mappings = None):
        self.model = None
        self.intents_path = intents_path

        self.documents = []
        self.vocabulary = [] # Embedding Layer
        self.intents = []
        self.intents_responses = []

        self.function_mappings = function_mappings
        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(text):
        lemmatizer = nltk.WordNetLemmatizer() # Finds the root word (runs, run = run)
        tokens = nltk.word_tokenize(text) # Tokenization
        tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
        return tokens

    def bag_of_words(self, tokens):
        # FIX: Loop over vocabulary to maintain a fixed feature vector size for the neural network
        return [ 1 if word in tokens else 0 for word in self.vocabulary ]

    def parse_intents(self):
        if os.path.exists(self.intents_path):
            with open(self.intents_path, "r") as f:
                intents_data = json.load(f)

        # Adds tags in intents list
        for intent in intents_data['intents']:
            if intent['tag'] not in self.intents:
                self.intents.append(intent['tag'])
                self.intents_responses.append(intent['responses']) # Adds respective responses

            for pattern in intent['patterns']:
                pattern_token = self.tokenize_and_lemmatize(pattern)
                self.vocabulary.extend(pattern_token) # FIX: Use extend to add elements individually, not append
                self.documents.append((pattern_token, intent['tag']))

        # FIX: Moved outside the loops for massive efficiency gains and to avoid the TypeError
        self.vocabulary = sorted(set(self.vocabulary))

    def prepare_data(self):
        bags = []
        indices = []

        for document in self.documents:
            token = document[0]
            bag = self.bag_of_words(token)
            bags.append(bag)
            intent_index = self.intents.index(document[1])
            indices.append(intent_index)

        self.X = np.array(bags)
        self.y = np.array(indices)

    def train_model(self, batch_size, lr, epochs):
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        y_tensor = torch.tensor(self.y, dtype=torch.long)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = ChatbotModel(X_tensor.shape[1], len(self.intents))

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        for epoch in tqdm(range(epochs), desc="Epoch"): # FIX: Wrap epochs in range()
            running_loss = 0.0

            for batch_X, batch_y in loader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            print(f"Epoch {epoch+1}/{epochs}: Loss: {running_loss/len(loader):.4f}")

    def save_model(self, model_path, dimensions_path):
        torch.save(self.model.state_dict(), model_path)

        with open(dimensions_path, "w") as f:
            json.dump({ 'input_size': self.X.shape[1], 'output_size': len(self.intents)}, f)

    def load_model(self, model_path, dimensions_path):
        with open(dimensions_path, "r") as f:
            dimensions = json.load(f)

        self.model = ChatbotModel(dimensions['input_size'], dimensions['output_size'])
        self.model.load_state_dict(torch.load(model_path, weights_only=True))

    def process_message(self, input_message):
        tokens = self.tokenize_and_lemmatize(input_message)
        bag = self.bag_of_words(tokens)

        bag_tensor = torch.tensor([bag], dtype=torch.float32)

        self.model.eval()
        with torch.no_grad():
            predictions = self.model.forward(bag_tensor)

        predicted_class_index = torch.argmax(predictions, dim=1).item()
        predicted_intent = self.intents[predicted_class_index]

        if self.function_mappings:
            if predicted_intent in self.function_mappings:
                self.function_mappings[predicted_intent]()

        # FIX: Use the integer index instead of trying to pass a string tag to the list
        if self.intents_responses[predicted_class_index]:
            return random.choice(self.intents_responses[predicted_class_index])
        else:
            return None

def get_stocks():
    stocks = ["AAPL", "META", "NVDA", "GS", "MSFT"]

    return random.sample(stocks, 3)

if __name__ == "__main__":
    # FIX: Pass the function reference itself, not its evaluated result
    assistant = ChatbotAssistant('intents.json', {"stocks": get_stocks})
    assistant.parse_intents()
    assistant.prepare_data()
    assistant.train_model(batch_size=8, lr=0.001, epochs=1000)

    assistant.save_model(model_path="model.pth", dimensions_path="dimensions.json")

    while True:
        message = input("Enter a message: ")
        if message == "exit":
            break
        else:
            print(assistant.process_message(message))