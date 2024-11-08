#########################模組############################
import discord
import os
from dotenv import load_dotenv
from myfunction.myfunction import WeatherAPI

########################初始化###########################
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))


#########################事件############################
@bot.event
async def on_ready():
    print(f"{bot.user}is ready and online!")
    await tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.message.channel.send("hey!")


#########################指令############################
@tree.command(name="hello", description="say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("hello")


@tree.command(name="weather", description="get weather")
async def weather(interaction: discord.Interaction, city: str, forecast: bool = False):
    await interaction.response.defer()

    unit_symbot = "C" if weather_api.units == "metric" else "F"


if not forecast:
    info = weather_api.get_current_weather(city)
    if "weather" in info and "main" in info:
        current_temrerature = info["main"]["temp"]
        weather_description = info["weather"][0]["description"]
        icon_code = info["weather"][0]["icon"]
        icon_url = weather_api.get_icon_url(icon_code)
        embed = discord.Embed(
            title=f"{city}的天氣",
            description=f"描述:{weather_description}\n{current_temrerature}{unit_symbot}",
            color=0x00FF00,
        )


#########################啟動############################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
