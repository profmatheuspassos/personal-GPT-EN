# Version 1.0
# Date: April 7, 2024
# DISCLAIMER: This script is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the script or the use or other dealings in the script.

import os
import openai
from pathlib import Path

def gather_messages():
    messages = []
    # Initial system instruction to the AI
    system_instruction = input("Please define the role of the AI, the context, and the task: ")
    messages.append({"role": "system", "content": system_instruction})
    
    while True:
        user_input = input("Enter your message (or type 'done' to finish): ")
        if user_input.lower() == 'done':
            break
        messages.append({"role": "user", "content": user_input})
    
    return messages

def save_to_file():
    while True:
        option = input("Do you want to save the results in a .txt file? (Y / N) ").upper()
        if option not in ["Y", "N"]:
            print("Please type only \"Y\" or \"N\". Please try again.")
            continue
        if option == "Y":
            print("The file will be saved in your home directory.")
            print("ATTENTION: If a file with the same name already exists, the previous file will be overwritten.")
            filename = input("IMPORTANT: Don't use spaces in the filename. Please type the name of the file: ")
            return filename.lower()
        else:
            return None

os.system("cls" if os.name == "nt" else "clear")
# Prompt the user for messages
messages = gather_messages()
# Prompt the user to save the results in a file
filename = save_to_file()
# Prompt the user to choose a template
try:
    model = input("Choose a model: gpt-4-turbo-preview, gpt-4 (default gpt-4): ")
except ValueError:
    model = "gpt-4" # Default model
# Ensure the model is either gpt-4-turbo-preview or gpt-4
if model not in ["gpt-4-turbo-preview", "gpt-4"]:
    model = "gpt-4"
    print("Invalid model value. Setting to default (gpt-4).")
# Prompt the user to set the temperature
try:
    temperature = float(input("Set the temperature: 0.0 to 2.0 (default 0.5): "))
except ValueError:
    temperature = 0.5  # Default temperature
    print("Invalid temperature value. Setting to default (0.5).")
# Ensure the temperature is within the acceptable range
if temperature < 0.0 or temperature > 2.0:
    temperature = 0.5
    print("Invalid temperature value. Setting to default (0.5).")
# OpenAI API key (Replace "your_api_key_here" with your actual OpenAI API key)
openai.api_key = 'your_api_key_here'
try:
    # Call the OpenAI API
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        # max_tokens=100,
        timeout=200
    )
    # Display the result
    print("AI Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")

if filename is not None:
    file_name = f"{filename}.txt"
    full_path = Path.home() / file_name
    print("\n")
    try:
        with open(full_path, "w") as result:
            result.write(response.choices[0].message.content)
        print(f"Response saved successfully at {full_path}.")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}.")