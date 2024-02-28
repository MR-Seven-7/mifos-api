import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyBaafmbVClFxg_PED6sIV_gSKiioYDZPYU')

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Please summarise this document: ```Hello```')

print(response)