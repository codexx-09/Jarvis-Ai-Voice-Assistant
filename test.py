import google.generativeai as genai

genai.configure(api_key="AIzaSyBaoIgnLCpETz_1LMlKteGexVpJedvschs")

for m in genai.list_models():
    print(m.name)