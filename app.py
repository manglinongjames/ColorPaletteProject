import openai
import json

import os

from flask import Flask, render_template, request
# from dotenv import dotenv_values

# print("Hello")
# config = dotenv_values(".env")

config = os.getenv("OPENAI_API_KEY")

openai.api_key = config

# openai.api_key = config["OPENAI_API_KEY"]



app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'
            )

#openai endpoint
def get_colors(msg):
    prompt=f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    You should generate a color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 
    
    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["F006699","#66CCCC","#FF0E68C","#008000","#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6","#9DC08B","F809966","#405130B"]
    
    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user", "content": prompt
            }
        ],
    )

    colors = json.loads(response.choices[0]["message"]["content"])
    return  {"colors": colors} 


@app.route("/palette", methods=["POST"])
def  prompt_to_palette():
    app.logger.info("HIT THE POST REQUEST ROUTE")
    app.logger.info(request.form.get("query"))

    query = request.form.get("query")
    colors = get_colors(query)
    app.logger.info(colors)
    return colors

@app.route("/")         #homepage
def  index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)