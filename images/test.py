import google.generativeai as genai

# Use an environment variable or a secure secret manager for your key!
genai.configure(api_key="AIzaSyDz-2sa-xKrMbO7osQyKrBj6MkzT79UzrE")

model = genai.GenerativeModel("gemini-2.5-flash-lite")

try:
    response = model.generate_content("Explain AI in one line")
    
    # Check if the response actually contains text before printing
    if response.candidates:
        print(response.text)
    else:
        print("The model did not return a response (it might have been blocked).")
        
except Exception as e:
    print(f"An error occurred: {e}")