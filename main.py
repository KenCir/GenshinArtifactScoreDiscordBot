import logging
import os

import discord

from discord import ApplicationContext, Option, OptionChoice, Attachment, Embed
from dotenv import load_dotenv

from ArtifactScore import ArtifactScore

load_dotenv()
bot = discord.Bot()
logging.basicConfig(level=logging.INFO)

MY_GUILDS = [872880984205430834]

artifact_score = ArtifactScore()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="score", description="聖遺物のスコアを表示", guild_ids=MY_GUILDS)
async def check_score(ctx: ApplicationContext,
                      artifact_image: Option(Attachment, name="聖遺物の画像", description="聖遺物の画像", required=True),
                      score_type: Option(str, name="計算方法", description="スコアの計算方法", required=True,
                                         choices=[
                                             OptionChoice(name="火力型", value="attack"),
                                             OptionChoice(name="防御型", value="defense"),
                                             OptionChoice(name="HP型", value="hp"),
                                             OptionChoice(name="元素チャージ効率型", value="charge"),
                                             OptionChoice(name="元素熟知", value="familiarity")
                                         ]),
                      artifact_type: Option(str, name="聖遺物タイプ", description="聖遺物の種類", required=True,
                                            choices=[
                                                OptionChoice(name="花", value="flower"),
                                                OptionChoice(name="羽", value="wing"),
                                                OptionChoice(name="時計", value="clock"),
                                                OptionChoice(name="杯", value="cup"),
                                                OptionChoice(name="冠", value="crown")
                                            ]),
                      ):
    await ctx.defer()
    await artifact_image.save("img.png")
    score, comprehensive, score_type_str, artifact_type_str, fields = artifact_score.check(score_type, artifact_type)
    embed = Embed(title="聖遺物スコア評価")
    embed.set_image(url=artifact_image.url)
    embed.add_field(name="SCORE", value=str(score))
    embed.add_field(name="総合評価", value=comprehensive)
    embed.add_field(name="計算方法", value=score_type_str)
    embed.add_field(name="聖遺物種類", value=artifact_type_str)
    for score_field in fields:
        embed.add_field(name=score_field[0], value=score_field[1])

    await ctx.respond(
        embed=embed
    )


bot.run(os.getenv("DISCORD_TOKEN"))
