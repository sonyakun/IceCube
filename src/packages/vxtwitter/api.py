import asyncio
import re

from aiohttp_client_cache import CachedSession, SQLiteBackend
import discord


async def get_twinf(url: list):
    vx = "api.vxtwitter.com"
    embeds = []
    for i in url:
        url_replaced = (
            i.replace("twitter.com", vx)
            .replace("x.com", vx)
            .replace("www.x.com", vx)
            .replace("www.twitter.com", vx)
            .replace("www.api.vxtwitter.com", vx)
        )
        async with CachedSession(cache=SQLiteBackend('vxtwitter_cache')) as session:
            async with session.get(url_replaced) as resp:
                if not resp.status == 500:
                    resp = await resp.json()
                    if not resp["mediaURLs"] == []:
                        murl = True
                    else:
                        murl = False
                    embed = discord.Embed(
                        title="{} (@{})".format(
                            resp["user_name"], resp["user_screen_name"]
                        ),
                        url=resp["tweetURL"],
                        description=resp["text"],
                        color=0x0091FF,
                    )
                    embed.set_author(
                        name="BetterTwitFix",
                        url="https://github.com/dylanpdx/BetterTwitFix",
                    )
                    if murl:
                        embed.set_image(url=resp["mediaURLs"][0])
                    embed.set_footer(text="IceCube Twitter Expander (using vxTwitter)")
                    embeds.append(embed)
    return embeds

async def parse(text):
    pattern = r"(?<!\|\|)(https?://(?:www\.)?(twitter\.com|x\.com)/[a-zA-Z0-9_]{1,15}/status/\d+)(?!\|\|)"
    urls = re.findall(pattern, text)
    resp = []
    for i in urls:
        resp.append(i[0])
    return resp