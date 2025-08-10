import google.generativeai as genai
genai.configure(api_key='AIzaSyDxBGhZe9_06TC1xw97cib087oN0rD60jU')

for m in genai.list_models():
    print(m.name)