# test_invoke_http.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
import os

import requests


app = Flask(__name__)
CORS(app)
TOKEN = ""

bot = telebot.TeleBot(TOKEN)
# invoke book microservice to get all books
#results = invoke_http("http://localhost:5006/notification", method='GET')
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Your telegram chat id is: " + str(message.chat.id))
bot.polling()
#bot.polling()


