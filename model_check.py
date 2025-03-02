import google.generativeai as genai

genai.configure(api_key="") #replace with your api key.

for model in genai.list_models():
    print(model)
