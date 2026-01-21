"""
Quick script to list available Gemini models for your API key
Run: python list_models.py
"""
import google.generativeai as genai

# Replace with your API key
API_KEY = input("Enter your Google Gemini API Key: ")

genai.configure(api_key=API_KEY)

print("\n" + "="*60)
print("Available Models that support generateContent:")
print("="*60 + "\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  ✓ {model.name}")

print("\n" + "="*60)
print("Copy one of the model names above and let me know!")
print("="*60)

