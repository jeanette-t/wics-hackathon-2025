from google import genai

client = genai.Client(api_key="AIzaSyAU6kLeb1geAI5ZhyyeDFa6Dh44IwB3xS4")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)

