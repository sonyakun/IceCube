import asyncio
import os
import statistics
import math
import logging

import discord
from discord.ext import commands
import yaml

from src.packages.logger import log

with open("config.yml", "r") as f:
    conf = yaml.safe_load(f)
    log_ = log()
    logger = log_.getlogger()
    if conf["debug"]:
        prefix = conf["bot"]["prefix_debug"]
        log_.logger.setLevel(logging.DEBUG)
        logger.info(
            "It is currently operating in development mode! Please set debug in config.yml to false in the production environment!"
        )
        token = conf["token_debug"]
    else:
        prefix = conf["bot"]["prefix"]
        log_.logger.setLevel(logging.INFO)
        token = conf["token"]

bot = commands.AutoShardedBot(command_prefix=prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.info("logged in: {}".format(bot.user.name))
    while True:
        servers = str("{:,}".format(int(len(bot.guilds))))
        await bot.change_presence(
            activity=discord.Activity(
                name="/help | {} servers".format(servers),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        await asyncio.sleep(15)
        users = str("{:,}".format(int(len(bot.users))))
        await bot.change_presence(
            activity=discord.Activity(
                name="ice.sonyakun.com (準備中) | {} users".format(users),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        pings = []
        for i in range(15):
            raw = bot.latency
            ping = round(raw * 1000)
            pings.append(ping)
            await asyncio.sleep(1)
        ping = str(math.floor(statistics.mean(pings)))
        await bot.change_presence(
            activity=discord.Activity(
                name="/help | ping: {}ms".format(ping),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        await asyncio.sleep(15)


@bot.event
async def setup_hook():
    for file in os.listdir("./src"):
        if file.endswith(".py"):
            await bot.load_extension(f"src.{file[:-3]}")
    if conf["debug"]:
        for file in os.listdir("./src/dev"):
            if file.endswith(".py"):
                await bot.load_extension(f"src.dev.{file[:-3]}")
    await bot.tree.sync(guild=discord.Object(961559815191134229))


bot.run(token)
