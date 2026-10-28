
import ollama
import csv
import os
from datetime import datetime

# Get the project folder
base_folder = os.path.dirname(os.path.abspath(__file__))
dataset_folder = os.path.join(base_folder, "dataset")

# Create dataset folder if needed
os.makedirs(dataset_folder, exist_ok=True)

# File paths
history_file = os.path.join(dataset_folder, "chat_history.csv")
responses_file = os.path.join(dataset_folder, "responses.csv")
logs_file = os.path.join(dataset_folder, "chatbot_logs.txt")

# Create CSV files with headings
for file_name in [history_file, responses_file]:
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "User_Question", "Chatbot_Response"])

# Select the installed Ollama model
model_name = input("Enter your Ollama model name: ")

# Store conversation history
history = [
    {
        "role": "system",
        "content": (
            "You are an education chatbot. "
            "Explain concepts in simple language, "
            "give examples, and help students learn."
        )
    }
]

print("\nWelcome to the Education Chatbot!")
print("Type 'exit' to stop the conversation.")

while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Chatbot: Goodbye! Your conversation has been saved.")
        break

    if not question:
        print("Chatbot: Please enter a question.")
        continue

    # Add the user's question to history
    history.append({
        "role": "user",
        "content": question
    })

    try:
        # Send the full conversation to Ollama
        response = ollama.chat(
            model=model_name,
            messages=history
        )

        answer = response["message"]["content"]

        # Add chatbot response to history
        history.append({
            "role": "assistant",
            "content": answer
        })

        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save conversation history
        with open(history_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, question, answer])

        # Save responses separately
        with open(responses_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, question, answer])

        # Save a readable text log
        with open(logs_file, "a", encoding="utf-8") as file:
            file.write(f"\n[{timestamp}]\n")
            file.write(f"User: {question}\n")
            file.write(f"Chatbot: {answer}\n")

        print("\nChatbot:", answer)

    except Exception as error:
        print("Error communicating with Ollama:", error)

        # Remove the unanswered question from history
        history.pop()
