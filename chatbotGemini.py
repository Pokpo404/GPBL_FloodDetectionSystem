import google.generativeai as genai

# Gemini API key
API_KEY = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

def gemini_chat(model="gemini-1.5-flash"):
    # Configure Gemini client
    genai.configure(api_key=API_KEY)

    # Starting session
    chat = genai.GenerativeModel(model).start_chat(history=[])

    print(f"💬 Chatbot running on {model}. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Exiting chatbot...")
            break

        response = chat.send_message(user_input)
        print(f"{model}: {response.text}\n")


if __name__ == "__main__":
    gemini_chat()

##########################################
# unused code for reference. Ignore for now
##########################################
# import llm_client
# import google.generativeai as genai

# def run_cli_chat(model="gemini-1.5-flash"):
    
#     #starting session
#     chat = genai.GenerativeModel(model).start_chat(history=[])
    
#     print(f"💬 Chatbot running on {model}. Type 'exit' to quit.\n")
    
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("👋 Exiting chatbot...")
#             break

#         response = chat.send_message(user_input)
#         print(f"{model}: {response.text}\n")
    
# def chat_with_bot(user_message, system_prompt="You are a helpful flood assistant trying to assist and provide useful information for people with dangers of flood. You may use the data we provided to incur better responses"):
#     try:
#         response = get_model.generate_content([
#             {"role": "system", "parts": system_prompt},
#             {"role": "user", "parts": user_message}
#         ])
#         return response.text
#     except Exception as e:
#         return f"Error: {e}" 

# def run_cli_chat():
#     print("Flood Chatbot (type 'exit' to quit)\n")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "bye"]:
#             print("Bot: Goodbye! Stay safe.")
#             break
        
#         reply = chat_with_bot(user_input)
#         print(f"Bot: {reply}\n")

# if __name__ == "__main__":
#     run_cli_chat()
