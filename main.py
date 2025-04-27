from keep_alive import keep_alive

keep_alive()
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import os

# إعداد البوت
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ البوت شغال: {bot.user}")


@bot.event
async def on_member_join(member):
    try:
        # تحميل صورة العضو
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        avatar_response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(avatar_response.content)).convert("RGBA")

        # تحميل صورة السيرفر
        guild_icon_url = member.guild.icon.url if member.guild.icon else None
        if guild_icon_url:
            guild_response = requests.get(guild_icon_url)
            guild_image = Image.open(BytesIO(guild_response.content))
            server_icon = guild_image.convert('RGBA')
        else:
            server_icon = None

        # تحميل الخلفية
        background = Image.open("wlcomez.png").convert("RGBA")
        background = background.resize((735, 245))

        # إعداد صورة العضو
        avatar = avatar.resize((100, 100))
        mask = Image.new('L', (100, 100), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 100, 100), fill=255)
        avatar = ImageOps.fit(avatar, (100, 100))
        avatar.putalpha(mask)

        # إعداد أيقونة السيرفر
        if server_icon:
            server_icon = server_icon.resize((80, 80))
            mask_server = Image.new('L', (80, 80), 0)
            draw_mask_server = ImageDraw.Draw(mask_server)
            draw_mask_server.ellipse((0, 0, 80, 80), fill=255)
            server_icon = ImageOps.fit(server_icon, (80, 80))
            server_icon.putalpha(mask_server)

        # لصق صورة العضو مكان الدائرة الرمادية
        background.paste(avatar, (193, 53), avatar)

        # لصق أيقونة السيرفر على وجه الرجل
        if server_icon:
            background.paste(server_icon, (435, 40), server_icon)

        # حفظ الصورة
        with BytesIO() as image_binary:
            background.save(image_binary, 'PNG')
            image_binary.seek(0)

            channel = discord.utils.get(member.guild.text_channels,
                                        name="الترحيب﹒﹢💡")
            if channel:
                await channel.send(
                    content=f"أهلاً وسهلاً بك {member.mention}🌹",
                    file=discord.File(fp=image_binary, filename='welcome.png'))

    except Exception as e:
        print(f"❌ خطأ أثناء الترحيب: {e}")

        keep_alive()

        bot.run(os.getenv("TOKEN"))
