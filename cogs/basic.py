import sqlite3
import time
import discord
from discord.ext import commands

connection = sqlite3.connect("profile.db")
cursor = connection.cursor()
class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="report")
    async def report(self,ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        m = discord.Embed(color=embed_color,description=f"Please head to [Support Server](<https://discord.gg/repturebot>) to report a user.")
        m.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        m.set_footer(text="Repture",icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=m)
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000, 2)
        await ctx.send(f"Discord Gateway Latency : {latency}ms")
    @commands.command(name="uptime")
    async def uptime(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        current_time = time.time()
        difference = int(current_time - self.start_time)
        days, remainder = divmod(difference, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(embed=discord.Embed(color=embed_color,description=f"**I have been running for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.**"))
    @commands.command(name="invite")
    async def invite(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        invite_url = "https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot"
        embed = discord.Embed(description=f"Hey {ctx.author.name},\nClick on the button to get the invite link.",color=embed_color)
        
        button = discord.ui.Button(label="Click On Invite Button",style=discord.ButtonStyle.blurple)
        
        async def button_callback(interaction):
            new_button = discord.ui.Button(label="Invite Repture", url=invite_url)
            new_view = discord.ui.View()
            new_view.add_item(new_button)
            await interaction.response.edit_message(view=new_view)
        
        button.callback = button_callback
        
        view = discord.ui.View()
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
async def setup(bot):
    await bot.add_cog(Basic(bot))
