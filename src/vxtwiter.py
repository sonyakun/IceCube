import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import orjson as json

from .packages.vxtwitter import parse, get_twinf

class vxTwitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        with open("data/settings.json", "r") as f:
            settings = json.loads(f.read())
        if settings[str(message.guild.id)]["vxtwitter"]["enable"]:
            urls = await parse(message.content)
            if urls == []:
                return
            await message.reply(embeds=await get_twinf(urls))

    @commands.hybrid_command(
        name="vxtwitter",
        description="有効の場合、twitter.com/x.comのURLが投稿された場合に自動で展開します",
        with_app_command=True,
    )
    @app_commands.guilds()
    @app_commands.checks.has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def cfg_vxtwitter(self, ctx: commands.Context):
        with open("data/settings.json", "r") as f:
            settings = json.loads(f.read())
        if ctx.interaction is not None:
            interaction = ctx.interaction
            await interaction.response.defer()
            if settings[str(interaction.guild.id)]["vxtwitter"]["enable"]:
                settings[str(interaction.guild.id)]["vxtwitter"]["enable"] = False
                with open("data/settings.json", "w") as f:
                    f.write(json.dumps(settings).decode('utf-8'))
                embed = discord.Embed(title="", description="vxTwitterの自動展開を**無効**に設定しました")
            else:
                settings[str(interaction.guild.id)]["vxtwitter"]["enable"] = True
                with open("data/settings.json", "w") as f:
                    f.write(json.dumps(settings).decode('utf-8'))
                embed = discord.Embed(title="", description="vxTwitterの自動展開を**有効**に設定しました")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            if settings[str(ctx.guild.id)]["vxtwitter"]["enable"]:
                settings[str(ctx.guild.id)]["vxtwitter"]["enable"] = False
                with open("data/settings.json", "w") as f:
                    f.write(json.dumps(settings).decode('utf-8'))
                embed = discord.Embed(title="", description="vxTwitterの自動展開を**無効**に設定しました")
            else:
                settings[str(ctx.guild.id)]["vxtwitter"]["enable"] = True
                with open("data/settings.json", "w") as f:
                    f.write(json.dumps(settings).decode('utf-8'))
                embed = discord.Embed(title="", description="vxTwitterの自動展開を**有効**に設定しました")
            msg = await ctx.reply(embed=embed, ephemeral=True)
            await asyncio.sleep(2.5)
            await msg.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(vxTwitter(bot))