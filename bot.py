# bot.py
import os
import argparse

from discord.ext import commands
from discord import File, Embed, Color
from db.champ import Champ

TOKEN = "NzA4MjM2NDE2MzgzMTg5MDIz.XrVQEw.FJ2egGivTVqxpDCsl0MBkMelm6c"
TOKEN_TEST = "NzA4OTQwNTg2NzYxMzIyNTM2.Xreqmw.jwSbw3JFKltpnK5nIQUUW_ulXZg"

ROOT = "bot"
CARDS_DIR = "db/cards"
FACTION_COLORS = {
    "Thục": Color.red(),
    "Quần": Color.dark_grey(),
    "Ngụy": Color.blue(),
    "Ngô": Color.green()
}

parser = argparse.ArgumentParser()
parser.add_argument("--deploy", action="store_true")
args = parser.parse_args()

if args.deploy:
    token = TOKEN
else:
    token = TOKEN_TEST

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="who_stupid")
async def who_is_stupid(ctx):
    response = "Bịt diết là thằng ngu nhất cái group này :)"
    await ctx.send(response)


@bot.command(name="who_the_boss")
async def who_the_boss(ctx):
    response = "Lumine is the boss of this group =3="
    await ctx.send(response)


@bot.command(name="champ", help="Tra cứu tướng theo tên Tiếng Việt hoặc Tiếng Anh.")
async def champ(ctx, *args):
    args = " ".join(args)
    if "," in args:
        name, mode = args.split(",")
    else:
        name = args
        mode = "new"
    
    name = name.strip()
    mode = mode.strip().lower()

    response = {}
    if name == "":
        response["content"] = "Xin hãy nhập thêm tên của tướng bạn cần tìm: !champ tên_tướng"
    else:
        champ = Champ().get_champ_by_name(name.title())

        if champ == None:
            response["content"] = "Xin lỗi, tôi không tìm thấy tướng có tên [{}] trong cơ sở dữ liệu".format(name)
        else:
            try:
                image = File("{}/{}/{}.jpg".format(ROOT, CARDS_DIR, champ["cn_name"]).lower())
            except FileNotFoundError:
                image = None
            
            embed = Embed(title="{} - {}".format(champ["name"], champ["cn_name"]), color=FACTION_COLORS[champ["faction"]])
            embed = embed.add_field(name="Phe phái", value=champ["faction"])
            embed = embed.add_field(name="HP", value=champ["hp"])
            embed = embed.add_field(name="Cặp đôi hoàn hảo", value="Không có")
            
            if champ["banned"] == 0:
                embed = embed.add_field(name="Banned", value="NO")
            else:
                embed = embed.add_field(name="Banned", value="YES")

            if mode == "ori":
                embed.add_field(name="Reworked", value="NO")
                embed.add_field(name="Skills", value=champ["original_desc"], inline=False)
            else:
                if champ["reworked"] == 0:
                    embed.add_field(name="Reworked", value="NO")
                    embed.add_field(name="Skills", value=champ["original_desc"], inline=False)
                else:
                    embed.add_field(name="Reworked", value="YES")
                    embed.add_field(name="Skills", value=champ["new_desc"], inline=False)
            

            # await ctx.send(file=image)
            # response = "Tên: {} - {}\n".format(champ["name"], champ["cn_name"])
            # response += "Phe phái: {}\n".format(champ["faction"])
            # response += "HP: {}\n".format(champ["hp"])
            
            # if mode == "ori":
            #     response += "Reworked: NO\n\n"
            #     response += champ["original_desc"]
            # else:
            #     if champ["reworked"] == 0:
            #         response += "Reworked: NO\n\n"
            #         response += champ["original_desc"]
            #     else:
            #         response += "Reworked: YES\n\n"
            #         response += champ["new_desc"]

            response = {
                "file": image,
                "embed": embed
            }

    await ctx.send(**response)


@bot.command(name="all_champs", help="Số lượng tướng đã có trong database.")
async def all_champs(ctx):
    champs = Champ().get_all_champs()
    response = "Hiện có tổng cộng {} tướng trong cơ sở dữ liệu".format(len(champs))
    
    await ctx.send(response)

bot.run(token)