from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Azure OpenAI GPT-4o configuration (with hardcoded key)
openai.api_type = "azure"
openai.api_base = "https://chandra24-resource.services.ai.azure.com/"
openai.api_version = "2024-02-15-preview"
openai.api_key = "EREKqTqt1fbKoM62MpVBi8n3aLOIZt8nHxCZQCXDmvTxBfFp9INuJQQJ99BEACHYHv6XJ3w3AAAAACOGwGc8"

DEPLOYMENT_NAME = "gpt-4o"  # Make sure this matches your Azure deployment name

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment_result = None
    if request.method == "POST":
        text = request.form.get("text", "")
        try:
            # Call Azure OpenAI GPT-4o
            gpt_response = openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that performs sentiment analysis."},
                    {"role": "user", "content": f"Analyze the sentiment of the following text. Respond with one word (Positive, Negative, or Neutral) and a short explanation:\n\n{text}"}
                ]
            )
            sentiment_result = gpt_response.choices[0].message.content.strip()
        except Exception as e:
            sentiment_result = f"Error: {str(e)}"
            print(f"OpenAI API error: {e}")

    return render_template("index.html", sentiment=sentiment_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
