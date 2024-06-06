https://genai-prompter.streamlit.app/

## Generative AI Prompter

This Streamlit app allows you to generate prompts for large language models like Claude-3-opus, Gemini-1.5-pro, and OpenAI GPT-4-omni, based on your input.

**Features:**

- **Prompt Generation:** Enter your query and the app will generate a prompt following prompt engineering principles using the Gemini-1.5-pro model.
- **Response Display:** The generated prompt is displayed to you.
- **Input/Response History:** All your queries and the generated prompts are stored in a dataframe, which can be viewed and downloaded as a CSV file.


**Note:**

- This app uses the Gemini-1.5-pro model. You can change the model in the `gemini_chat` function.
- The prompt generation process may take some time depending on the complexity of the query.
- Please ensure you have a valid Google Cloud Platform API key and have enabled the Google Generative AI API in your project.

This app provides a simple way to generate prompts for large language models. You can modify it further to add more features or integrate it with other tools.
