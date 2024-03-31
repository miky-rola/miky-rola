import re

import tkinter as tk

from tkinter import messagebox, filedialog

import random

from textblob import TextBlob

import json


class TherapyChatbot:
    """A simple chatbot program for providing therapy services."""


    def __init__(self, root):
        """Initialize the TherapyChatbot."""
        self.root = root
        self.root.title("Therapy ChatBot")
        self.root.geometry("670x650")

        # Placeholder for user profile data
        self.user_profile = {}

        # Placeholder for conversation history
        self.previous_conversations = []

        # Create GUI widgets
        self.create_widgets()

    
    def create_widgets(self):
        """Create GUI widgets for the application."""
        # Create label widget for welcome message
        label = tk.Label(self.root, text="Welcome To the Therapy program", font="Arial, 18")
        label.pack(pady=10)

        # Create sections for user input, chat display, and buttons
        self.create_user_input_section()
        self.create_chat_display_section()
        self.create_buttons_section()


    def create_user_input_section(self):
        """Create input section for user details."""
        frame = tk.Frame(self.root)
        frame.pack()

        # Labels and entry fields for username and email
        tk.Label(frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(frame, width=30)
        self.email_entry.grid(row=1, column=1)


    def create_chat_display_section(self):
        """Create chat display section to show conversation history."""
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(pady=10)

        # Text widget for displaying conversation history
        self.chat_display = tk.Text(self.chat_frame, height=20, width=50)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        # Scrollbar for the chat display
        scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar.set)


    def create_buttons_section(self):
        """Create buttons section for actions like sending, saving, loading, and clearing conversations."""
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        # Label and entry field for user message
        tk.Label(self.input_frame, text="Enter your message:").pack(side=tk.LEFT, padx=10)
        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT)

        # Button for sending user message
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10)

        # Buttons for saving, loading, and clearing conversations
        frame = tk.Frame(self.root)
        frame.pack()

        self.save_button = tk.Button(frame, text="Save Conversation", command=self.save_conversation)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.load_button = tk.Button(frame, text="Load Conversation Logs", command=self.load_conversation)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(frame, text="Clear Conversation", command=self.clear_conversation)
        self.clear_button.pack(side=tk.LEFT, padx=10)


    def send_message(self):
        """Send message entered by the user."""
        username = self.username_entry.get().strip().title()
        email = self.email_entry.get().strip()
        user_input = self.input_entry.get().strip().lower()

        if not self.validate_user_inputs(username, email, user_input):
            return

        if self.is_meaningless(user_input):
            self.display_message("Therapist: Please enter a meaningful message.")
            return 

        response = self.generate_response(user_input)

        self.display_message(f"{username}: {user_input}")
        self.display_message(f"Therapist: {response}")

        self.update_conversation_history(username, user_input, "Therapist", response)
        self.clear_input_field()


    def validate_user_inputs(self, username, email, user_input):
        """Validate user inputs.

        Args:
            username (str): The username entered by the user.
            email (str): The email entered by the user.
            user_input (str): The message entered by the user.

        Returns:
            bool: True if all inputs are valid, False otherwise.
        """
        if not username or not email:
            # Display a message if username or email is missing
            messagebox.showinfo("Therapy ChatBot" ,"Please enter both username and email.")
            return False
        elif not user_input:
            # Display a message if no message is entered
            messagebox.showinfo("Therapy ChatBot", "Please enter a message.")
            return False
        else:
            return True


    def is_meaningless(self, user_input):
        """Check if the user input is meaningless.

        Args:
            user_input (str): The message entered by the user.

        Returns:
            bool: True if the input is meaningless, False otherwise.
        """
        meaningless_phrases = ["...", "???", "??", "blah", "hmm", "uh", "um", "idk", "lol", "huh"]
        with open("stopword.txt", "r") as file:
            stopwords = set(word.strip().lower() for word in file)

        cleaned_input = user_input.strip().lower()
        words = cleaned_input.split()
        return not cleaned_input or all(word in stopwords for word in words) or cleaned_input in meaningless_phrases


    def generate_response(self, user_input):
        """Generate a response based on the user input.

        Args:
            user_input (str): The message entered by the user.

        Returns:
            str: The response generated by the chatbot.
        """
        sentiment = TextBlob(user_input).sentiment.polarity

        if "addiction" in user_input:
            return self.handle_addiction()
        elif re.search(r"\b(die|kill|suicide)\b", user_input, re.IGNORECASE):
            return self.handle_suicide()
        elif re.search(r"\b(hi|hello|hey)\b", user_input, re.IGNORECASE):
            return self.greeting()
        else:
            return self.analyze_sentiment(sentiment)
        

    def handle_addiction(self):
        """Handle user input related to addiction."""
        return "Please provide more information about your addiction."
    

    def handle_suicide(self):
        """Handle user input related to suicide."""
        result = messagebox.askquestion("Therapist", "Should I call the suicide control agency?")
        return "I have contacted the suicide control agency. You'll be reached out to very soon." if result == "yes" else "Then be calm on yourself. Everything will surely be fine."


    def greeting(self):
        """Generate a random greeting."""
        with open("greeting.txt", "r") as file:
            greeting_responses = file.readlines()
            return random.choice(greeting_responses)


    def analyze_sentiment(self, sentiment):
        """Analyze sentiment of the user input and generate a response.

        Args:
            sentiment (float): The sentiment polarity of the user input.

        Returns:
            str: The response generated by the chatbot based on sentiment analysis.
        """
        with open("positive.txt", "r") as file:
            positive_responses = file.readlines()

        with open("neutral.txt", "r") as file:
            neutral_responses = file.readlines()

        with open("negative.txt", "r") as file:
            negative_responses = file.readlines()

        if sentiment > 0.2:
            return random.choice(positive_responses)
        elif sentiment < -0.2:
            return random.choice(negative_responses)
        else:
            return random.choice(neutral_responses)


    def save_conversation(self):
        """Save the conversation history to a JSON file."""
        conversation_data = {"conversations": self.previous_conversations}
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w") as file:
                json.dump(conversation_data, file)
            self.display_message(f"Conversation saved to {filename}")


    def load_conversation(self):
        """Load conversation history from a JSON file."""
        username = self.username_entry.get().strip().title()
        email = self.email_entry.get().strip()
        if not username or not email:
            messagebox.showinfo("Therapy ChatBot" ,"Please enter both username and email.")
            return

        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "r") as file:
                    conversation_data = json.load(file)
                saved_conversations = conversation_data.get("conversations", [])
                self.display_saved_conversations(saved_conversations, username, email)
            except FileNotFoundError:
                messagebox.showinfo("Therapy ChatBot", "No saved conversation logs found.")


    def display_saved_conversations(self, saved_conversations, username, email):
        """Display saved conversations in the chat display."""
        self.chat_display.delete(1.0, tk.END)
        for conversation in saved_conversations:
            if conversation[0] == username and conversation[1] == email:
                self.chat_display.insert(tk.END, f"{conversation[0]}: {conversation[1]}\n")
                self.chat_display.insert(tk.END, f"Therapist: {conversation[3]}\n")
            else:
                self.display_message("Therapy ChatBot: No saved conversation logs found for this user.")


    def clear_conversation(self):
        """Clear the conversation history from the chat display."""
        self.chat_display.delete(1.0, tk.END)


    def display_message(self, message):
        """Display a message in the chat display."""
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)


    def update_conversation_history(self, username, user_input, sender, response):
        """Update the conversation history."""
        self.previous_conversations.append((username, user_input, sender, response))


    def clear_input_field(self):
        """Clear the user input field."""
        self.input_entry.delete(0, tk.END)
        

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_app = TherapyChatbot(root)
    root.mainloop()
