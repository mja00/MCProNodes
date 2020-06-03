from discord.ext import commands
from colorama import init, Fore, Style, Back
from discord import File
from discord.utils import get
from datetime import datetime as dt
import discord, os, json, requests, random


class statusHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nodestatus(self, ctx, node: int = None):
        if node is None:
            await ctx.channel.send("Please specify a node number.")
            return
        await ctx.channel.send("Getting node status")



def setup(bot):
    bot.add_cog(statusHandler(bot))
