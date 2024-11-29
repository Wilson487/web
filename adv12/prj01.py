#########################模組############################
import discord
import os
from dotenv import load_dotenv
from myfunction.myfunction import WeatherAPI
import openai

########################初始化###########################
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = WeatherAPI(os.getenv(""))
openai.api_key = os.getenv("")


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
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
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
                description=f"描述:{weather_description}",
                color=0x1E90FF,
            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(
                name="溫度",
                value=f"{current_temrerature}度{unit_symbot}",
                inline=False,
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("查詢失敗")

    else:
        info = weather_api.get_forecast(city)
        if "list" in info:
            if not ai:
                forecast_list = info["list"][:10]
                embeds = []
                for forecast in forecast_list:
                    dt_txt = forecast["dt_txt"]
                    temp = forecast["main"]["temp"]
                    description = forecast["weather"][0]["description"]
                    icon_code = forecast["weather"][0]["icon"]
                    icon_url = weather_api.get_icon_url(icon_code)

                    embed = discord.Embed(
                        title=f"(city)天氣預報-(dt_txt)",
                        description=f"描述:{description}",
                        color=0x1E90FF,
                    )
                    embed.set_thumbnail(url=icon_url)
                    embed.add_field(
                        name="溫度", value=f"{temp}度{unit_symbot}", inline=False
                    )
                    embeds.append(embed)
                await interaction.followup.send(embeds=embeds)

            else:
                try:
                    response = openai.chat.Completion.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "你是一個天氣查詢器，請根據下面的天氣預報回答以下問題：",
                            },
                            {
                                "role": "user",
                                "content": f"以下是{city}未來的天氣預報，請回答以下問題：\n{info}",
                            },
                        ],
                        temperature=0.2,
                    )
                    awalysis = response.choices[0].message.content

                    await interaction.followup.send(f"**(city)**天氣預報\n{awalysis}")
                except Exception as e:
                    await interaction.followup.send(f"查詢失敗，{e}")
        else:
            await interaction.followup.send("查詢失敗")


#########################啟動############################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
