import asyncio
import re

import aiohttp
import discord
from discord import app_commands, Webhook
from discord.ext import commands
import orjson as json


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite = re.compile(
            "(https?://)?((ptb|canary)\.)?(discord\.(gg|io)|discord(app)?.com/invite)/[0-9a-zA-Z]+",
            re.IGNORECASE,
        )
        self.token = re.compile(
            r"[A-Za-z0-9\-_]{23,30}\.[A-Za-z0-9\-_]{6,7}\.[A-Za-z0-9\-_]{27,40}",
            re.IGNORECASE,
        )

    async def mod_msg(self, message: discord.Message):
        token = self.token.search(message.content)
        invite = self.invite.search(message.content)
        if token:
            await message.remove_reaction("🔄", message.guild.me)
            await message.add_reaction("❌")
            embed = discord.Embed(
                description="Discordのトークンをグローバルチャットに送信することはできません。",
                colour=discord.Colour.red(),
            )
            msg = await message.reply(embed=embed)
            await asyncio.sleep(2.5)
            await msg.delete()
            return True
        elif invite:
            await message.remove_reaction("🔄", message.guild.me)
            await message.add_reaction("❌")
            embed = discord.Embed(
                description="Discordの招待リンクをグローバルチャットに送信することはできません。",
                colour=discord.Colour.red(),
            )
            msg = await message.reply(embed=embed)
            await asyncio.sleep(2.5)
            await msg.delete()
            return True

    async def send_message(self, url, username, guild, message, avatar, image):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, session=session)
            if image is None:
                if message is None:
                    await webhook.send(
                        username="@" + username + " | {}".format(guild.name),
                        avatar_url=avatar,
                    )
                else:
                    await webhook.send(
                        content=message,
                        username="@" + username + " | {}".format(guild.name),
                        avatar_url=avatar,
                    )
            else:
                if message is None:
                    await webhook.send(
                        username="@" + username + " | {}".format(guild.name),
                        avatar_url=avatar,
                        embeds=image,
                    )
                else:
                    await webhook.send(
                        content=message,
                        username="@" + username + " | {}".format(guild.name),
                        avatar_url=avatar,
                        embeds=image,
                    )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        if message.author.bot:
            return
        with open("data/global.json", "r") as f:
            gc_guilds = json.loads(f.read())
        try:
            if gc_guilds.get(str(message.guild.id)) is None:
                return
            if not gc_guilds[str(message.guild.id)]["ch"] == message.channel.id:
                return
            await message.add_reaction("🔄")
            if await self.mod_msg(message):
                return
            for i in gc_guilds["channel"]:
                if i["id"] == str(message.guild.id):
                    pass
                else:
                    if message.attachments != []:
                        imgs = []
                        limit = 1
                        max_a = len(message.attachments)
                        if max_a >= 5:
                            max_a = "5"
                        else:
                            max_a = str(max_a)
                        for attachments in message.attachments:
                            if limit >= 6:
                                break
                            if attachments.content_type in (
                                "image/jpeg",
                                "image/jpg",
                                "image/png",
                                "image/gif",
                                "image/webp",
                            ):
                                if attachments.width is not None:
                                    embed = discord.Embed(
                                        title="添付ファイル ({}/{})".format(limit, max_a)
                                    )
                                    embed.set_image(url=attachments.url)
                                    imgs.append(embed)
                                    limit = limit + 1
                    else:
                        imgs = None
                    await self.send_message(
                        i["url"],
                        message.author.name,
                        message.guild,
                        message.content,
                        message.author.avatar.url,
                        image=imgs,
                    )
            await message.remove_reaction("🔄", message.guild.me)
            await message.add_reaction("✅")
        except KeyError:
            pass

    @commands.hybrid_command(
        name="global",
        description="グローバルチャットを有効にします。既に存在する場合は無効にしてwebhookを削除します。",
        with_app_command=True,
    )
    @app_commands.guilds()
    @app_commands.checks.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def globalchat(self, ctx: commands.Context):
        with open("data/global.json", "r") as f:
            gc_guilds = json.loads(f.read())
        if ctx.interaction is not None:
            interaction = ctx.interaction
            await interaction.response.defer()
            if gc_guilds.get(str(interaction.guild.id)) is None:
                wh = await interaction.channel.create_webhook(
                    name="IceCube GlobalChat", reason="webhook is created by IceCube"
                )
                gc_guilds[str(interaction.guild.id)] = {}
                gc_guilds[str(interaction.guild.id)]["url"] = wh.url
                gc_guilds[str(interaction.guild.id)]["ch"] = interaction.channel.id
                gc_guilds["channel"].append({"id": interaction.guild.id, "url": wh.url})
                with open("data/global.json", "w") as f:
                    f.write(json.dumps(gc_guilds).decode("utf-8"))
                await interaction.followup.send("グローバルチャットに接続しました。", ephemeral=True)
            else:
                url = gc_guilds[str(interaction.guild.id)]["url"]
                channel = self.bot.get_channel(
                    gc_guilds[str(interaction.guild.id)]["ch"]
                )
                channel_webhooks = await channel.webhooks()
                for webhook in channel_webhooks:
                    if webhook.url == url:
                        await webhook.delete()
                        gc_guilds.pop(str(ctx.guild.id))
                        gc_guilds["channel"].remove(
                            {"id": str(interaction.guild.id), "url": url}
                        )
                        with open("data/global.json", "w") as f:
                            f.write(json.dumps(gc_guilds).decode("utf-8"))
                        await interaction.followup.send(
                            "グローバルチャットから切断しました！", ephemeral=True
                        )
                        break
        else:
            if gc_guilds.get(str(ctx.guild.id)) is None:
                wh = await ctx.channel.create_webhook(
                    name="IceCube GlobalChat", reason="webhook is created by IceCube"
                )
                gc_guilds[str(ctx.guild.id)] = {}
                gc_guilds[str(ctx.guild.id)]["url"] = wh.url
                gc_guilds[str(ctx.guild.id)]["ch"] = str(ctx.channel.id)
                gc_guilds["channel"].append({"id": ctx.guild.id, "url": wh.url})
                with open("data/global.json", "w") as f:
                    f.write(json.dumps(gc_guilds).decode("utf-8"))
                msg = await ctx.reply("グローバルチャットに接続しました。")
                await asyncio.sleep(2.5)
                await msg.delete()
            else:
                url = gc_guilds[str(ctx.guild.id)]["url"]
                channel = self.bot.get_channel(gc_guilds[str(ctx.guild.id)]["ch"])
                channel_webhooks = await channel.webhooks()
                for webhook in channel_webhooks:
                    if webhook.url == url:
                        await webhook.delete()
                        gc_guilds.pop(str(ctx.guild.id))
                        gc_guilds["channel"].remove(
                            {"id": str(ctx.guild.id), "url": url}
                        )
                        with open("data/global.json", "w") as f:
                            f.write(json.dumps(gc_guilds).decode("utf-8"))
                        msg = await ctx.reply("グローバルチャットから切断しました！")
                        await asyncio.sleep(2.5)
                        await msg.delete()
                        break


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalChat(bot))
