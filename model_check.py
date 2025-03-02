import google.generativeai as genai

genai.configure(api_key="AIzaSyAu69ssSbnmPEvwrYAILKqkWWHpkWGLba4") #replace with your api key.

for model in genai.list_models():
    print(model)