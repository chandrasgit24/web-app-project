from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Azure OpenAI GPT-4o configuration
openai.api_type = "azure"
openai.api_base = "https://sentiment-app-resource.services.ai.azure.com/"
openai.api_version = "2024-02-15-preview"
openai.api_key = "2RJVGeUEbKBoCzKuC3dWvmp0uNEMO6GloERLOQdmJphjOY0sOJT9JQQJ99BEACHYHv6XJ3w3AAAAACOGei4V"

DEPLOYMENT_NAME = "sentiment-app-gpt4o"

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment_result = None
    if request.method == "POST":
        text = request.form["text"]

        # GPT-4o sentiment analysis
        gpt_response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that performs sentiment analysis."},
                {"role": "user", "content": f"Analyze the sentiment of the following text. Respond with one word (Positive, Negative, or Neutral) and a short explanation:\n\n{text}"}
            ]
        )
        sentiment_result = gpt_response.choices[0].message.content.strip()

    return render_template("index.html", sentiment=sentiment_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
