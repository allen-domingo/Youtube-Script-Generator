import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
       idea = request.form["idea"]
       category = request.form["category"]
       trait1 = request.form["trait1"]
       trait2 = request.form["trait2"]
       print(trait1,trait2)
      # print(idea)
    #    response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #         {"role": "user", "content": "Where was it played?"}
    #         ]
    #         )
       
     # Note: you need to be using OpenAI Python v0.27.0 for the code below to worlk
       print(generate_prompt(idea))
       response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
           # prompt=generate_prompt(idea),
            max_tokens=1000,
            messages=[
            {"role": "system", "content": f"You are a {trait1}, but also {trait2} {category} youtuber."},
            {"role": "user", "content": generate_prompt(idea)}
            ],
            temperature=1.0,
            )
       response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
           # prompt=generate_prompt(idea),
           
            max_tokens=2000,
            
            messages=[
            {"role": "system", "content": f"You are a {trait1}, but also {trait2} {category} youtuber."},
            {"role": "user", "content": generate_prompt(idea)},
            {"role": "system","content": response.choices[0].message["content"]},
            {"role": "user","content": "Create a long essay based on the outline"}
            ],
            temperature=1.0,
       )
       return redirect(url_for("index", result=response2.choices[0].message["content"]))
    #print("TESTTESTTESTTESTTESTTESTTESTTEST")
    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(idea1):
    return f"Create a youtube video essay outline based on {idea1}"
    
