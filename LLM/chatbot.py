# import ollama

# def initialize_chatbot(model_name="mistral"):
#     client = ollama.Client()
#     if model_name not in client.list_models():
#         print(f"Model '{model_name}' not found. Pulling model...")
#         client.pull_model(model_name)
#     print(f"Chatbot initialized with model: {model_name}")
#     return client, model_name

# if __name__ == "__main__":
#     client, model = initialize_chatbot()
#     # Example interaction
#     prompt = "Hello, how can you help me?"
#     response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
#     print("Bot:", response["message"]["content"])

import subprocess

def ollama_chat(model="llama3.1"):
    print(f"💬 Chatbot running on {model}. Type 'exit' to quit.\n")
    
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,              # decode to str automatically
        encoding="utf-8",       # force UTF-8
        errors="replace"        # replace invalid chars instead of crashing
    )
        
        # Define system prompt once at the start
    system_prompt = (
        "You are a helpful flood detection assistant. "
        "Answer concisely, use simple language, and when possible, "
        "relate your answers to water levels, danger prediction, "
        "and evacuation guidance."
    )
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Exiting chatbot...")
            break
        
         # Combine system prompt + user input
        full_prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"
        
        # Call ollama via subprocess
        result = subprocess.run(
            ["ollama", "run", model],
            input=user_input,
            capture_output=True,
            text=True
        )
        
        # Print response
        print(f"{model}: {result.stdout.strip()}\n")

if __name__ == "__main__":
    ollama_chat()
