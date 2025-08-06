import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# Rest of your imports and code
import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from browser_use import Agent
import nest_asyncio
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
nest_asyncio.apply()
load_dotenv()
def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        st.error(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Initialize the LLM
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error('GEMINI_API_KEY is not set')
    st.stop()

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

# Async main function
async def main(file_path):
    file_string = read_file_to_string(file_path)
    if file_string is None:
        return None
    
    st.text_area("File Content", file_string, height=200)
    agent = Agent(
        task=file_string,
        llm=llm,
        max_actions_per_step=4,
        # browser=browser,  # Uncomment if browser is defined
    )
    
    result = await agent.run()
    return result

# Streamlit UI
st.title("File Processing App")

# Option 1: Text input for file path
file_path = st.text_input("Enter the file path", value=R"C:\Python\python_automation_framework\report.txt")

# Option 2: File uploader (alternative to file path)
uploaded_file = st.file_uploader("Or upload a file", type=["txt"])

# Process button
if st.button("Process"):
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_report.txt", "wb") as f:
            f.write(uploaded_file.getvalue())
        file_path = "temp_report.txt"
    
    if file_path:
        with st.spinner("Processing..."):
            # Run the async main function
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(main(file_path))
            
            if result is not None:
                st.success("Processing complete!")
                st.write("Result:")
                st.write(result)
            
            # Clean up temporary file if used
            if uploaded_file is not None and os.path.exists("temp_report.txt"):
                os.remove("temp_report.txt")
    else:
        st.error("Please provide a file path or upload a file.")