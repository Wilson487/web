#########################模組############################
import discord
import os
from dotenv import load_dotenv
from myfunction.myfunction import WeatherAPI
import openai

ans = os.getenv("WEATHER_API_KEY")
print(f"!!!!!{ans}!!!!!!!!!!!!!!!!!!!")
########################初始化###########################
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")


#########################事件############################
@bot.event
async def on_ready():
    print(f"{bot.user}is ready and online!")
    await tree.sync()


@bot.event
async def on_message(message):
    channel_id = message.channel.id
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.message.channel.send("hey!")
    elif channel_id in channel_games:
        user_input = message.content.strip()
        if user_input == "結束遊戲":
            channel_games.pop(channel_id)
            await message.channel.send("遊戲結束")
        else:
            game_data = channel_games[channel_id]["game_data"]
            if "history" not in channel_games[channel_id]:
                channel_games[channel_id]["history"] = []
            history = channel_games[channel_id]["history"]
            history.append({"role": "user", "content": user_input})
            messages = (
                [
                    {
                        "role": "system",
                        "content": f"""
你是一場海龜湯遊戲的主持人，根據以下謎題回答玩家的問題：
你的回答只會是 [是],[不是],[無可奉告]或[恭喜答對],並盡可能簡短
當玩家要求提示時,你可以提供"關鍵字"當作提示
謎題:{game_data["question"]}
解答:{game_data["answer"]}
""",
                    }
                ]
                + history
            )
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temeprature=0.5,
                )
                answer = response.choices[0].message.content
                if answer == "恭喜答對":
                    game_data["solved"] = True
                    await message.channel.send("恭喜玩家提出正確答案，遊戲結束")
                    channel_games.pop(channel_id)
                else:
                    history.append({"role": "assistant", "content": answer})
                    channel_games[channel_id]["history"] = history
                    await message.channel.send(answer)
                    print(messages)
            except Exception as e:
                await message.channel.send(f"查詢失敗，{e}")
    else:
        await bot.process_commands(message)


channel_games = ()


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


@tree.command(name="turtle_soup", description="開始海龜湯遊戲")
async def turtle_soup(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id in channel_games:
        await interaction.response.send_message(
            "正在遊戲中，請勿重複開始", ephemeral=True
        )
    else:
        channel_games[channel_id] = {
            "game_data": {
                "question": "一個人在沙漠中發現了一具屍體，旁邊又一根燒過的火柴，發生甚麼是",
                "answer": "她參加了熱氣球比賽，為了減重需要有人跳下去，他抽到了最短的火柴，只好跳下去。",
                "solved": False,
            },
            "history": [],
        }
        await interaction.response.send_message(
            f"""
        遊戲開始!
        題目:{channel_games[channel_id]["game_data"]["question"]}
        請大家開始提問，輸入'結束遊戲'可結束遊戲。
        我的回答只會是 [是],[不是] 或 [無可奉告]。"""
        )


#########################啟動############################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
