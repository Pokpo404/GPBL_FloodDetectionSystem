import google.generativeai as genai

class Summarizer:
    
    # LLM initialization
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    # Summarization helper function
    def summarize(self, text: str, style: str = "concise") -> str:
        """
        Summarize input text.
        :param text: Raw text to summarize
        :param style: 'concise', 'detailed', or 'bullet points'
        :return: Summary string
        """
        prompt = f"Summarize the following text in a {style} way:\n\n{text}"
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    #summarizer with json input
    def summarize_json(self, data: dict, style="concise"):
        """
        Summarize flood sensor data from JSON format.

        Expected JSON format:
        {
            "records": [
                {
                    "timestamp": "2025-08-30T14:00:00",
                    "sensor_1": 2.3,
                    "sensor_2": 2.1
                },
                {
                    "timestamp": "2025-08-30T15:00:00",
                    "sensor_1": 2.7,
                    "sensor_2": 2.5
                },
                ...
            ]
        }

        Parameters:
        - data (dict): JSON-like dictionary containing multiple flood sensor readings.
        - style (str): Summary style (e.g., "concise", "detailed", "alert-focused").

        Returns:
        - str: A summarized report of water level trends and risks.
        """
        prompt = f"""
        Summarize this flood report in a {style} way:

        {data}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()


#testing with hardcoded text
if __name__ == "__main__":
    summarizer = Summarizer()

    sample_text = """
    Water levels in the river rose by 2.3 meters in the last 12 hours,
    affecting three nearby villages. Evacuation centers have been set up,
    but heavy rainfall is expected to continue for the next 24 hours.
    """

    print("Concise Summary:")
    print(summarizer.summarize(sample_text, style="concise"))

    print("\nBullet Points Summary:")
    print(summarizer.summarize(sample_text, style="bullet points"))

##########################################
# unused code for reference. Ignore for now
##########################################

# import google.generativeai as genai

# # Gemini API key
# API_KEY = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

# def summarize_text(text, system_prompt="You are a summarization assistant. Summarize clearly and concisely."):
#     try:
#         # Put system prompt inline with user content
#         response = get_model.generate_content(
#             f"{system_prompt}\n\nSummarize this:\n{text}"
#         )
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
#     long_text = """
#     Heavy rainfall in the northern region has caused rivers to overflow. 
#     Authorities reported that water levels rose by 3 meters in 12 hours, 
#     forcing the evacuation of more than 500 families. Rescue operations 
#     are ongoing, and temporary shelters have been set up in schools and 
#     community centers. Meteorological departments have issued warnings 
#     of continued rainfall over the next 48 hours.
#     """
    
#     summary = summarize_text(long_text)
#     print("Summary:\n", summary)
