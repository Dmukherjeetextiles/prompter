import streamlit as st
import pandas as pd
from prompter import save_responses_to_csv
import google.generativeai as genai

def gemini_chat(text):
    api_key = st.secrets["API_KEY"]
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

# Function to process the input and get the response
def process_input(user_input):
    response = gemini_chat(user_input)
    return response

# Function to update the dataframe with new input and response
def update_dataframe(df, user_input, response):
    new_row = pd.DataFrame({'Input': [user_input], 'Response': [response]})
    df = pd.concat([df, new_row], ignore_index=True)
    return df

# Main function to run the Streamlit app
def main():
    st.title("Generative AI Prompter")
    
    # Initialize an empty dataframe to store inputs and responses
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = pd.DataFrame(columns=['Input', 'Response'])
    
    # Text input for the user prompt
    user_input = st.text_input("Enter your query:")

    # Button to submit the query
    if st.button("Submit"):
        if user_input:
            response = process_input(user_input)
            st.session_state.dataframe = update_dataframe(st.session_state.dataframe, user_input, response)
            st.session_state.last_response = response
            st.session_state.show_response = True
        else:
            st.error("Please enter a query.")

    # Display the response if available
    if 'show_response' in st.session_state and st.session_state.show_response:
        st.success(f"{st.session_state.last_response}")
        
        # Display the dataframe with inputs and responses
        st.dataframe(st.session_state.dataframe)

        # Button to save the dataframe to CSV
        if st.button("Save to CSV"):
            save_responses_to_csv(st.session_state.dataframe['Input'], st.session_state.dataframe['Response'])
            st.success("Responses saved to responses.csv")

if __name__ == '__main__':
    main()
