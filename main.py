import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):   #get weather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "City not found. Please enter a valid city name."

    weather = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return (
        f"🌤️ Weather in {city.title()}:\n"
        f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)\n"
        f"💨 Wind: {wind} m/s\n"
        f"💧 Humidity: {humidity}%\n"
        f"📝 Description: {weather}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):   # /start command handler
    await update.message.reply_text("Hi! Send me a city name and I'll give you the weather report 🌦️")

async def weather_response(update: Update, context: ContextTypes.DEFAULT_TYPE):   # city name handler
    city = update.message.text
    weather = get_weather(city)
    await update.message.reply_text(weather)

def main():   # run the bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather_response))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
