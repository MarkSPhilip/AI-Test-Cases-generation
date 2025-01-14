# .\myenv\Scripts\activate

import json
import re
import ollama
import streamlit as st
import inspect
import importlib.util
import os

# Loading function from file and extracting function details
def load_function_from_file(file_path, func_name):
    """Dynamically loads a function from a specified file path and function name."""
    if not os.path.isfile(file_path):
        st.error("File not found. Please provide a valid file path.")
        return None

    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, func_name, None)
    if func is None:
        st.error("Function not found. Please check the function name.")
    return func

def read_function_details(func):
    """Reads details about the given function without calling it."""
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    source_code = inspect.getsource(func)
    
    return {
        "signature": str(signature),
        "docstring": docstring,
        "source_code": source_code
    }

# Generate Python test functions
def generate_test_cases_code(function_details):
    """Generate test functions for a given function using LLM output."""
    func_name = function_details.get("signature").split("(")[0]

    # Prompt for Python-based test cases
    prompt = (
    f"Generate pytest test functions for the function '{func_name}' using the following details:\n\n"
    f"Function details:\n{function_details.get('source_code')}\n\n"
    "Requirements:\n"
    "1. Each test function should validate the input against the following fields:\n"
    "   - 'first_name': The first name of the user (string).\n"
    "   - 'last_name': The last name of the user (string).\n"
    "   - 'age': The age of the user (integer).\n"
    "2. Test cases must include edge cases, such as:\n"
    "   - A valid average user with typical values.\n"
    "   - A user with the maximum valid age (e.g., 120).\n"
    "   - A user with the minimum valid age (e.g., 0).\n"
    "   - Invalid cases, such as missing fields, incorrect types, or out-of-range values.\n"
    "3. Ensure invalid test cases explicitly expect the validation to fail, but pass the test by asserting expected failure conditions (e.g., raise an exception or assert with a specific error message).\n"
    "4. Only generate the test function definitions with `assert` statements, and ensure they are ready to copy into a test file.\n\n"
    "Output:\n"
    "- Provide only the function definitions for pytest test cases.\n"
    "- Ensure each function covers a unique scenario and includes edge cases.\n"
    "- Test functions for invalid cases must explicitly check for expected failures and pass the test accordingly.\n\n"
    "Example format:\n"
    "```python\n"
    "def test_valid_user():\n"
    "    entry = {\"first_name\": \"Jane\", \"last_name\": \"Doe\", \"age\": 30}\n"
    "    assert 'first_name' in entry\n"
    "    assert isinstance(entry['first_name'], str)\n"
    "    assert 'last_name' in entry\n"
    "    assert isinstance(entry['last_name'], str)\n"
    "    assert 'age' in entry\n"
    "    assert isinstance(entry['age'], int)\n"
    "    assert 0 <= entry['age'] <= 120\n\n"
    "def test_max_age():\n"
    "    entry = {\"first_name\": \"John\", \"last_name\": \"Smith\", \"age\": 120}\n"
    "    assert entry['age'] == 120\n\n"
    "def test_invalid_missing_field():\n"
    "    entry = {\"first_name\": \"Alice\", \"age\": 25}\n"
    "    assert 'last_name' in entry, \"Missing last_name field\"\n"
    "    assert True, \"Invalid scenario expected and handled\"\n\n"
    "def test_invalid_type_first_name():\n"
    "    entry = {\"first_name\": 123, \"last_name\": \"Doe\", \"age\": 30}\n"
    "    assert not isinstance(entry['first_name'], str), \"Expected invalid type for first_name\"\n"
    "    assert True, \"Invalid scenario expected and handled\"\n"
    "```\n\n"
    "Generate the test functions exactly as specified above."
)


    # API Call with Timeout
    try:
        response = ollama.generate(model="llama3.1:latest", prompt=prompt)
    except Exception as e:
        st.error(f"Error in API call: {e}")
        return []

    # Validate Response
    response_text = response.get('response', '')
    if not response_text:
        st.warning("Empty response received from the API.")
        return []

    # Extract Python test functions
    python_test_pattern = r"def\s+test_[\s\S]*?(?=\ndef\s+test_|$)"
    test_functions = re.findall(python_test_pattern, response_text)

    if not test_functions:
        st.warning("No valid test functions found in the response.")
        st.write("Raw response for debugging:", response_text)
        return []

    return test_functions

# Streamlit rendering function
def rendering():
    st.title("Test Cases Generator")

    # Input fields for file path and function name
    file_path = st.text_input("Enter the file path")
    func_name = st.text_input("Enter the function name")

    if st.button("Generate Test Cases"):
        if not file_path or not func_name:
            st.error("Please provide both file path and function name.")
        else:
            func = load_function_from_file(file_path, func_name)
            if func:
                function_details = read_function_details(func)
                generated_test_functions = generate_test_cases_code(function_details)
                
                if generated_test_functions:
                    # Display the newly generated test cases
                    st.success("Test cases generated successfully.")
                    st.subheader("Generated Test Cases:")
                    for test_func in generated_test_functions:
                        st.code(test_func, language="python")

if __name__ == "__main__":
    rendering()
