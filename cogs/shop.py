import discord
from discord.ext import commands
import sqlite3
import asyncio

db = sqlite3.connect("profile.db")
cursor = db.cursor()

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shop")
    async def create_shop(self, ctx, *, name: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        cursor.execute("SELECT user FROM shop WHERE user = ?", (ctx.author.id,))
        if cursor.fetchone():
            await ctx.send(f"{ctx.author.mention}, you already have a shop. This will overwrite it.")
        cursor.execute("INSERT OR REPLACE INTO shop (user, name, products, image, thmb, color) VALUES (?, ?, ?, ?, ?, ?)", (ctx.author.id, name, "", "", "", ""))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have updated shop to: `{name}`", color=color).set_footer(text="Repture"))

    @commands.command(name="product")
    async def add_products(self, ctx, *, items: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        products = ", ".join([item.strip() for item in items.split(",")])
        cursor.execute("UPDATE shop SET products = ? WHERE user = ?", (products, ctx.author.id))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have added `{products}` for {ctx.author.name} profile.", color=color).set_footer(text="Repture"))

    @commands.command(name="thumbnail")
    async def set_thumbnail(self, ctx, *, url: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        if "http" not in url:
            await ctx.send(f"{ctx.author.mention}, invalid URL.")
            return
        cursor.execute("UPDATE shop SET thmb = ? WHERE user = ?", (url, ctx.author.id))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have updated thumbanil", color=color).set_footer(text="Repture"))

    @commands.command(name="image")
    async def set_image(self, ctx, *, url: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        if "http" not in url:
            await ctx.send(f"{ctx.author.mention}, invalid URL.")
            return
        cursor.execute("UPDATE shop SET image = ? WHERE user = ?", (url, ctx.author.id))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have updated image", color=color).set_footer(text="Repture"))

    @commands.command(name="web")
    async def set_website(self, ctx, *, url: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        if "http" not in url:
            await ctx.send(f"{ctx.author.mention}, invalid URL.")
            return
        cursor.execute("UPDATE shop SET web = ? WHERE user = ?", (url, ctx.author.id))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have updated the web `{url}`", color=color).set_footer(text="Repture"))

    @commands.command(name="forum")
    async def set_forum(self, ctx, *, url: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        if "http" not in url:
            await ctx.send(f"{ctx.author.mention}, invalid URL.")
            return
        cursor.execute("UPDATE shop SET forum = ? WHERE user = ?", (url, ctx.author.id))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have updated forum to: `{url}`", color=color).set_footer(text="Repture"))

    @commands.command(name="embedcolor")
    async def change_color(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = cursor.fetchone()
        color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        embed = discord.Embed(title="Color Selector", description="React to select a color or reset.", color=color)
        msg = await ctx.send(embed=embed)
        reactions = {"⬛": "0x31373d", "⬜": "0xe6e7e8", "🟥": "0xdd2e44", "🟧": "0xf4900c", "🟨": "0xfdcb58", "🟩": "0x78b159", "🟦": "0x55acee", "🟪": "0xaa8ed6", "🟫": "0xc1694f", "⚙️": None, "💭": "custom"}
        for emoji in reactions:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            selected = reactions[str(reaction.emoji)]
            if selected == "custom":
                await ctx.send("Enter a hex code (e.g., `#FF5733`).")
                try:
                    msg = await self.bot.wait_for("message", timeout=30.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    if msg.content.startswith("#"):
                        selected = f"0x{msg.content[1:]}"
                    else:
                        await ctx.send("Invalid format.")
                        return
                except asyncio.TimeoutError:
                    await ctx.send("Timeout.")
                    return
            if selected is None:
                cursor.execute("UPDATE shop SET color = NULL WHERE user = ?", (ctx.author.id,))
                db.commit()
                await msg.edit(embed=discord.Embed(description="Color reset.", color=0xADD8E6).set_footer(text="Repture"))
            else:
                cursor.execute("UPDATE shop SET color = ? WHERE user = ?", (selected, ctx.author.id))
                db.commit()
                await msg.edit(embed=discord.Embed(description=f"Color set to: `{selected[2:]}`", color=int(selected, 16)).set_footer(text="Repture"))
        except asyncio.TimeoutError:
            await ctx.send("Timeout.")

    @commands.command(name="reset")
    async def reset_shop(self, ctx):
        cursor.execute("SELECT user FROM shop WHERE user = ?", (ctx.author.id,))
        if not cursor.fetchone():
            await ctx.send(f"{ctx.author.mention}, no shop to reset.")
            return
        cursor.execute("DELETE FROM shop WHERE user = ?", (ctx.author.id,))
        db.commit()
        await ctx.send(embed=discord.Embed(description=f"Alright, I have reset the products data for **{ctx.author.name}** profile.", color=0xADD8E6).set_footer(text=self.bot.user.name, icon_url=self.bot.user.display_avatar.url))

async def setup(bot):
    await bot.add_cog(Shop(bot))
