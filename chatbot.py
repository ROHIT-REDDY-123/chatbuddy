def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "your name" in user_input:
        return "I'm ChatBuddy, your simple chatbot!"
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a nice day!"
    elif "help" in user_input:
        return "You can ask me about greetings, my name, or say bye to exit."
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"

def main():
    print("🤖 ChatBuddy: Hello! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower() or "exit" in user_input.lower():
            print("🤖 ChatBuddy: Goodbye! 👋")
            break
        response = chatbot_response(user_input)
        print(f"🤖 ChatBuddy: {response}")

if __name__ == "__main__":
    main()


