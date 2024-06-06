import streamlit as st
import pandas as pd
from prompter import gemini_chat, save_responses_to_csv

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
        st.success(f"Result: {st.session_state.last_response}")
        
        # Display the dataframe with inputs and responses
        st.dataframe(st.session_state.dataframe)

        # Button to save the dataframe to CSV
        if st.button("Save to CSV"):
            save_responses_to_csv(st.session_state.dataframe['Input'], st.session_state.dataframe['Response'])
            st.success("Responses saved to responses.csv")

if __name__ == '__main__':
    main()
