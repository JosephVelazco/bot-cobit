from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from unicodedata import normalize
import re

app=Flask(__name__)



bot=ChatBot('JP', read_only=True,
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    database_uri='sqlite:///JP_db.db',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response':'Lo siento, eso está fuera de mi enfoque. Pero puedes preguntarme algo sobre el coronavirus.',
            'maximum_similarity_treshold':0.999999,
        },
    ]
)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText=request.args.get('msg')
    userText=re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", userText), 0, re.I)
    userText= normalize( 'NFC', userText)
    userText=userText.lower()
    return str(bot.get_response(userText))
if __name__ == "__main__":
    app.run()