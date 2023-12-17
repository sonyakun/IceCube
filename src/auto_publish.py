import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import orjson as json

from .packages.func import func_ctx, func_inter

class auto_publish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        if message.author.bot:
            return
        try:
            with open("./data/settings.json", "r") as f:
                cfg = json.loads(f.read())
            if (
                str(message.channel.id)
                in cfg[str(message.guild.id)]["auto_publish"]["channels"]
            ):
                if message.channel.type == discord.ChannelType.news:
                    await message.publish()
                    await message.add_reaction("✅")
                else:
                    print(False)
        except KeyError:
            pass

    @commands.hybrid_command(
        name="publish",
        description="有効なアナウンスチャンネルでメッセージが送信された場合に自動的に公開します",
        with_app_command=True,
    )
    @app_commands.guilds()
    @app_commands.checks.has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def publish(self, ctx: commands.Context):
        if ctx.interaction is not None:
            interaction = ctx.interaction
            if await func_inter.disable_dm(interaction):
                return
            await interaction.response.defer()
            with open("./data/settings.json", "r") as f:
                cfg = json.loads(f.read())
            try:
                if (
                    str(interaction.channel.id)
                    in cfg[str(interaction.guild.id)]["auto_publish"]["channels"]
                ):
                    cfg[str(interaction.guild.id)]["auto_publish"]["channels"].remove(
                        str(interaction.channel.id)
                    )
                    embed = discord.Embed(title="自動公開を無効にしました。")
                else:
                    cfg[str(interaction.guild.id)]["auto_publish"]["channels"].append(
                        str(interaction.channel.id)
                    )
                    embed = discord.Embed(title="自動公開を有効にしました。")
            except KeyError:
                cfg[str(interaction.guild.id)]["auto_publish"]["channels"] = [
                    str(interaction.channel.id),
                ]
                embed = discord.Embed(title="自動公開を有効にしました。")
            with open("./data/settings.json", "w") as f:
                f.write(json.dumps(cfg).decode("utf-8"))
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            if await func_ctx.disable_dm(ctx):
                return
            with open("./data/settings.json", "r") as f:
                cfg = json.loads(f.read())
            try:
                if (
                    str(ctx.channel.id)
                    in cfg[str(ctx.guild.id)]["auto_publish"]["channels"]
                ):
                    cfg[str(ctx.guild.id)]["auto_publish"]["channels"].remove(
                        str(ctx.channel.id)
                    )
                    embed = discord.Embed(title="自動公開を無効にしました。")
                else:
                    cfg[str(ctx.guild.id)]["auto_publish"]["channels"].append(
                        str(ctx.channel.id)
                    )
                    embed = discord.Embed(title="自動公開を有効にしました。")
            except KeyError:
                cfg[str(ctx.guild.id)]["auto_publish"]["channels"] = [
                    str(ctx.channel.id),
                ]
                embed = discord.Embed(title="自動公開を有効にしました。")
            with open("./data/settings.json", "w") as f:
                f.write(json.dumps(cfg).decode("utf-8"))
            msg = await ctx.reply(embed=embed)
            await asyncio.sleep(2.5)
            await msg.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(auto_publish(bot))
