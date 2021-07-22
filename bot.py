# bot.py
import os
import argparse
import sqlite3
import asyncio

from discord.ext import commands
from discord import File, Embed
from db.champ import Champ
from factions import get_faction_color
from flask import Flask

TOKEN = os.getenv('TOKEN')
TOKEN_TEST = os.getenv('TOKEN_TEST')

DB_DIR = "db/tqs.db"
CARDS_DIR = 'db/cards'

parser = argparse.ArgumentParser()
parser.add_argument('--deploy', action='store_true')
args = parser.parse_args()

if args.deploy:
    token = TOKEN
else:
    token = TOKEN_TEST

bot = commands.Bot(command_prefix='!')
conn = sqlite3.connect(DB_DIR)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='who_stupid')
async def who_is_stupid(ctx):
    response = 'Bịt diết là thằng ngu nhất cái group này :)'
    await ctx.send(response)


@bot.command(name='who_the_boss')
async def who_the_boss(ctx):
    response = 'Lumine is the boss of this group =3='
    await ctx.send(response)


@bot.command(name='champ', help='Tra cứu tướng theo tên Tiếng Việt hoặc Tiếng Anh.')
async def champ(ctx, *args):
    args = ' '.join(args)
    if ',' in args:
        name, mode = args.split(',')
    else:
        name = args
        mode = 'new'
    
    name = name.strip()
    mode = mode.strip().lower()

    response = {}
    if name == '':
        response['content'] = 'Xin hãy nhập thêm tên của tướng bạn cần tìm: !champ tên_tướng'
    else:
        champ = Champ(conn).get_champ_by_name(name.title())

        if champ == None:
            response['content'] = 'Xin lỗi, tôi không tìm thấy tướng có tên [{}] trong cơ sở dữ liệu'.format(name)
        else:
            try:
                image = File('{}/{}.jpg'.format(CARDS_DIR, champ['cn_name']).lower())
            except FileNotFoundError:
                image = None
            
            faction_color = get_faction_color(champ['faction'])
            embed = Embed(title='{} - {}'.format(champ['name'], champ['cn_name']), color=faction_color)
            embed = embed.add_field(name='Phe phái', value=champ['faction'])
            embed = embed.add_field(name='HP', value=champ['hp'])
            embed = embed.add_field(name='Cặp đôi hoàn hảo', value='Không có')
            
            if champ['banned'] == 0:
                embed = embed.add_field(name='Banned', value='NO')
            else:
                embed = embed.add_field(name='Banned', value='YES')

            if mode == 'ori':
                embed.add_field(name='Reworked', value='NO')
                embed.add_field(name='Skills', value=champ['original_desc'], inline=False)
            else:
                if champ['reworked'] == 0:
                    embed.add_field(name='Reworked', value='NO')
                    embed.add_field(name='Skills', value=champ['original_desc'], inline=False)
                else:
                    embed.add_field(name='Reworked', value='YES')
                    embed.add_field(name='Skills', value=champ['new_desc'], inline=False)

            response = {
                'file': image,
                'embed': embed
            }

    await ctx.send(**response)


@bot.command(name='all_champs', help='Số lượng tướng đã có trong database.')
async def all_champs(ctx):
    champs = Champ(conn).get_all_champs()
    response = 'Hiện có tổng cộng {} tướng trong cơ sở dữ liệu'.format(len(champs))
    
    await ctx.send(response)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'ok'

async def start_bot():
    bot.run(token)

async def start_flask():
    app.run(debug=True)

async def main():
    asyncio.gather(start_bot(), start_flask())

asyncio.run(main())