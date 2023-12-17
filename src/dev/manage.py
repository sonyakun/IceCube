import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import orjson as json

administrator = [875651011950297118]


class manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load_extension")
    @commands.is_owner()
    async def publish(self, ctx: commands.Context, cog: str):
        if ctx.author.id in administrator:
            await self.bot.load_extension("hello")

    @commands.command(name="reload_extension")
    @commands.is_owner()
    async def publish(self, ctx: commands.Context, cog: str):
        if ctx.author.id in administrator:
            await self.bot.reload_extension(cog)

    @commands.command(name="error")
    @commands.is_owner()
    async def publish(self, ctx: commands.Context):
        raise Exception("test")


async def setup(bot: commands.Bot):
    await bot.add_cog(
        manage(bot),
        guilds = [discord.Object(id=961559815191134229)]
    )
