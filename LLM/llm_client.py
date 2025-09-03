import google.generativeai as genai

# Gemini API key
GEMINI_API_KEY = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"



# Reusable model instance
model = genai.GenerativeModel("gemini-1.5-pro")

def get_model():
    genai.configure(api_key=GEMINI_API_KEY)
    return "gemini-1.5-pro"