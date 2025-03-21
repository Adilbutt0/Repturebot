import discord
from discord.ext import commands
import sqlite3
connection = sqlite3.connect("profile.db")
cursor = connection.cursor()
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mark", aliases=["m"])
    async def _mark(self, ctx, user_id: int, *, reason=None):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        mem = await self.bot.fetch_user(user_id)
        if not reason:
            await ctx.reply("Please mention a reason to mark.")
        else:
            cursor.execute("SELECT type, reason FROM marks WHERE user = ?", (mem.id,))
            result = cursor.fetchone()
            if result:
                if result[0] == 1:
                    await ctx.reply(f"The user {mem.mention} is already marked as a scammer.")
                else:
                    cursor.execute("UPDATE marks SET type = ?, reason = ? WHERE user = ?", (1, reason, mem.id))
                    connection.commit()
                    embed = discord.Embed(description=f"The User {mem} is now marked as a scammer for reason - {reason}", color=embed_color)
                    await ctx.send(embed=embed)
                    channel = self.bot.get_channel(1170066506864935025)
                    if channel:
                        await channel.send(f"SCAMMER - {mem} ID : `{mem.id}` ({reason})")
            else:
                cursor.execute("INSERT OR REPLACE INTO marks (user, type, reason) VALUES (?, ?, ?)", (mem.id, 1, reason))
                connection.commit()
                embed = discord.Embed(description=f"The User {mem} is now marked as a scammer for reason - {reason}", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(1170066506864935025)
                await channel.send(f"SCAMMER - {mem} ID : `{mem.id}` ({reason})")

    @commands.command(name="dwc", aliases=["deal-with-caution"])
    async def dwc(self, ctx, user_id: int, *, reason=None):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        mem = await self.bot.fetch_user(user_id)
        if not reason:
            await ctx.reply("Please mention a reason to mark.")
        else:
            cursor.execute("SELECT type, reason FROM marks WHERE user = ?", (mem.id,))
            result = cursor.fetchone()
            if result:
                if result[0] == 2:
                    await ctx.reply(f"The user {mem.mention} is already marked as a dwc.")
                else:
                    cursor.execute("UPDATE marks SET type = ?, reason = ? WHERE user = ?", (2, reason, mem.id))
                    connection.commit()
                    embed = discord.Embed(description=f"The User {mem} is now marked as a dwc for reason - {reason}", color=embed_color)
                    embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                    await ctx.send(embed=embed)
                    channel = self.bot.get_channel(1170066531577774201)
                    await channel.send(f"DWC - {mem} ID : `{mem.id}` ({reason})")
            else:
                cursor.execute("INSERT OR REPLACE INTO marks (user, type, reason) VALUES (?, ?, ?)", (mem.id, 2, reason))
                connection.commit()
                embed = discord.Embed(description=f"The User {mem} is now marked as a dwc for reason - {reason}", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(1170066531577774201)
                await channel.send(f"DWC - {mem} ID : `{mem.id}` ({reason})")

    @commands.command(name="unmark", aliases=["um"])
    async def unmark(self, ctx, user_id: int):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        mem = await self.bot.fetch_user(user_id)
        cursor.execute("SELECT type, reason FROM marks WHERE user = ?", (mem.id,))
        result = cursor.fetchone()
        if result:
            if result[0] in (1, 2):
                cursor.execute("DELETE FROM marks WHERE user = ?", (mem.id,))
                connection.commit()
                embed = discord.Embed(description=f"Removed the mark for {mem.mention}.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"The user {mem.mention} is not marked as a scammer or dwc.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"The user {mem.mention} is not marked as a scammer or dwc.", color=embed_color)
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.reply(embed=embed)

    @commands.command(name="undwc", aliases=["udwc"])
    async def undwc(self, ctx, user_id: int):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        mem = await self.bot.fetch_user(user_id)
        cursor.execute("SELECT type, reason FROM marks WHERE user = ?", (mem.id,))
        result = cursor.fetchone()
        if result:
            if result[0] == 2:
                cursor.execute("DELETE FROM marks WHERE user = ?", (mem.id,))
                connection.commit()
                embed = discord.Embed(description=f"Removed the dwc mark for {mem.mention}.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"The user {mem.mention} is not marked as a dwc.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(description=f"The user {mem.mention} is not marked as a dwc.", color=embed_color)
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.reply(embed=embed)

    @commands.command(name="inv", aliases=["user-inv"])
    async def _invite_user(self, ctx, user_id: int):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        member = self.bot.get_user(user_id)
        if member:
            await member.send("Hello User! You have a report registered against you in Repture Support. Please join and defend your case within 24 Hours, or you will get marked as a scammer. Link: https://discord.gg/repturebot")
            embed = discord.Embed(description="Alright, I have successfully dmed", color=embed_color)
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I can't find this member.", color=embed_color)
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)

    @commands.command(name="np", aliases=["nop"])
    async def _npadd(self, ctx, user: discord.User):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        if ctx.author.id in (1162455661041434787, 314599100811051008):
            cursor.execute("SELECT user FROM np WHERE user = ?", (user.id,))
            mem = cursor.fetchone()
            if mem:
                embed = discord.Embed(description=f"{ctx.author.mention}: This user already has no-prefix access.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)
            else:
                cursor.execute("INSERT OR REPLACE INTO np (user) VALUES (?)", (user.id,))
                connection.commit()
                embed = discord.Embed(description=f"Added **{user}** into no-prefix bypass.", color=embed_color)
                embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
                await ctx.send(embed=embed)

    @commands.group(name="blacklist")
    async def blacklist(self, ctx):
        pass

    @blacklist.command(name="add")
    async def blacklist_add(self, ctx, user: discord.User):
        cursor.execute("SELECT user FROM blacklist WHERE user = ?", (user.id,))
        if cursor.fetchone():
            await ctx.send(f"{user.mention} is already blacklisted.")
        else:
            cursor.execute("INSERT INTO blacklist (user) VALUES (?)", (user.id,))
            connection.commit()
            await ctx.send(f"{user.mention} has been added to the blacklist.")

    @blacklist.command(name="remove")
    async def blacklist_remove(self, ctx, user: discord.User):
        cursor.execute("SELECT user FROM blacklist WHERE user = ?", (user.id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM blacklist WHERE user = ?", (user.id,))
            connection.commit()
            await ctx.send(f"{user.mention} has been removed from the blacklist.")
        else:
            await ctx.send(f"{user.mention} is not in the blacklist.")

    @blacklist.command(name="list")
    async def blacklist_list(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT user FROM blacklist")
        blacklisted_users = cursor.fetchall()
        if blacklisted_users:
            embed = discord.Embed(title="Repture Blacklist", color=embed_color)
            for user_id in blacklisted_users:
                user = await self.bot.fetch_user(user_id[0])
                embed.description = f"**{user.name}** | `{user.id}`"
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Repture Blacklist",
                description="No users are currently blacklisted.",
                color=embed_color
            )
            embed.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
