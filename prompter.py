from dotenv import load_dotenv
import os
import google.generativeai as genai
import pandas as pd

def gemini_chat(text):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config={
                                      "temperature": 1,
                                      "top_p": 0.95,
                                      "top_k": 0,
                                      "max_output_tokens": 8192,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                                  ])
    convo = model.start_chat(history=[])
    
    try:
        my_input = f"Provide a prompt for large language models according to the input at {text}. The prompt should be properly outlined according to prompt engineering principles."
        convo.send_message(my_input)
        response = convo.last.text.replace('*', '')
        return response
    except Exception as e:
        print(f"It seems that there's an error: {e}")
        return None

def save_responses_to_csv(inputs, responses, filename='responses.csv'):
    # Create a dataframe from inputs and responses
    df = pd.DataFrame({'Input': inputs, 'Response': responses})
    # Save the dataframe to a CSV file
    df.to_csv(filename, index=False)
    print(f"Responses saved to {filename}")

def main():
    inputs = []
    responses = []

    while True:
        my_prompt = input("Enter your query (type 'exit' to quit): ")
        if my_prompt.lower() == 'exit':
            break
        response = gemini_chat(my_prompt)
        inputs.append(my_prompt)
        responses.append(response)

        print(f"Result: {response}")

    # Save responses to a CSV file
    save_responses_to_csv(inputs, responses)

if __name__ == '__main__':
    main()
