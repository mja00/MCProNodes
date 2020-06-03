from discord.ext import commands
from colorama import init, Fore, Style, Back
from discord import File, Embed
from discord.utils import get
from datetime import datetime as dt
from mcprostatus import Location, Node
import discord, os, json, requests, random


class statusHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nodestatus(self, ctx, node: str = None):
        if node is None:
            await ctx.channel.send("Please specify a node number.")
            return
        message = await ctx.channel.send("Getting node status")
        try:
            node = Node(node)
        except KeyError:
            await message.delete()
            await ctx.channel.send("Node doesn't exist")
        embed = self.createEmbed(node)
        await message.delete()
        await ctx.channel.send(embed=embed)

    def createEmbed(self, node: Node):
        embed = Embed(
            title=node.node,
            color=discord.Color.green() if node.online else discord.Color.red()
        )

        embed.timestamp = dt.utcnow()

        embed.add_field(name="Location", value=node.location, inline=True)
        embed.add_field(name="Online", value=node.online, inline=True)
        embed.add_field(name="Network Issue", value=node.network_issue, inline=True)
        embed.add_field(name="Message", value=node.message, inline=True)
        embed.add_field(name="Last Hearbeat", value=node.last_heartbeat, inline=True)
        return embed


def setup(bot):
    bot.add_cog(statusHandler(bot))
