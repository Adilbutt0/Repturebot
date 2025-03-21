import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3
import random
import string
import threading

connection = sqlite3.connect("profile.db")
db_cursor = connection.cursor()
thread_lock = threading.Lock()

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_token(self, length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @commands.command(name="profile", aliases=["p"])
    async def display_profile(self, ctx, target: discord.Member = None):
        db_cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        color_data = db_cursor.fetchone()
        embed_color = int(color_data[0], 16) if color_data and color_data[0] else 0xADD8E6
        with thread_lock:
            try:
                target = target or ctx.author
                db_cursor.execute("SELECT overall, positive, negative FROM vouches WHERE user = ?", (target.id,))
                stats = db_cursor.fetchone() or (0, 0, 0)  # Default values for overall, positive, and negative
                db_cursor.execute("SELECT name, products, web, forum FROM shop WHERE user = ?", (target.id,))
                shop_info = db_cursor.fetchone() or ("Not Set", "Not Set", "Not Set", "Not Set")
                db_cursor.execute("SELECT vouch FROM vouch_details WHERE user = ? ORDER BY id DESC LIMIT 5", (target.id,))
                recent_vouches = db_cursor.fetchall()
                comments = "\n".join(v[0] for v in recent_vouches) or "No comments Yet."
                db_cursor.execute("SELECT badge FROM badges WHERE user = ?", (target.id,))
                badge_list = db_cursor.fetchall()
                embed = discord.Embed(
                        description=f"**__User Information:__**\n**Id:** {target.id}\n**Registered Date:** {target.created_at.strftime('%d %B, %Y')}\n**Display Name:** {target.display_name}\n**Mention:** {target.mention}\n",
                        color=embed_color
                    )
                db_cursor.execute("SELECT thmb FROM shop WHERE user = ?", (target.id,))
                thumbnail_data = db_cursor.fetchone()
                thumbnail_url = thumbnail_data[0] if thumbnail_data and thumbnail_data[0] else target.display_avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                embed.add_field(
                        name="__Feedback Information:__",
                        value=f"**Positive:** {stats[1]}\n**Negative:** {stats[2]}\n**Overall:** {stats[0]}",
                        inline=False
                    )
                db_cursor.execute("SELECT user, positive FROM vouches ORDER BY positive DESC")
                rank = next((index + 1 for index, (user_id, _) in enumerate(db_cursor.fetchall()) if user_id == target.id), None)
                embed.add_field(name="__Global Rank__", value=f"`#{rank}`" if rank else "`#0`", inline=False)
                db_cursor.execute("SELECT total_commands FROM command_stats WHERE user = ?", (target.id,))
                command_stats = db_cursor.fetchone()
                total_commands = command_stats[0] if command_stats else 0
                embed.add_field(
                    name="__Commands Runned__",
                    value=f"{total_commands}",
                    inline=False
                )
                view = View()
                shop_button = Button(label="Server and Goods", style=discord.ButtonStyle.primary)
                async def shop_callback(interaction: discord.Interaction):
                    shop_name = shop_info[0] if shop_info[0] != "Not Set" else "Not Set"
                    products = shop_info[1] if shop_info[1] != "Not Set" else "Not Set"
                    forum = shop_info[3] if shop_info[3] != "Not Set" else "Not Set"
                    web = shop_info[2] if shop_info[2] != "Not Set" else "Not Set"
                    products_list = products.split(", ") if products != "Not Set" else ["No products available."]
                    products_formatted = "\n".join(f"- {item}" for item in products_list if item != "Not Set")
                    embed = discord.Embed(
                        title="Shop Configuration",
                        description=f"__Services & Goods__\n**Shop:** {shop_name}\n**Forum:** {forum}\n**Web Shop**: {web}\n\n**Products**\n{products_formatted}",
                        color=embed_color
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                shop_button.callback = shop_callback
                view.add_item(shop_button)
                comments_button = Button(label="Past 5 Comments", style=discord.ButtonStyle.secondary)
                async def comments_callback(interaction):
                    db_cursor.execute("SELECT id, vouch, sts FROM vouch_details WHERE user = ? ORDER BY id DESC LIMIT 5", (target.id,))
                    recent_vouches = db_cursor.fetchall()
                    comments = "\n".join(
                            f"Vouch Id: {v[0]} | Comment: {v[1]} | Status: {'Accepted' if v[2] == 1 else 'Denied' if v[2] == 2 else 'Pending'}"
                            for v in recent_vouches
                        ) or "No comments yet."
                    await interaction.response.send_message(f"**Past 5 Comments:**\n{comments}", ephemeral=True)
                comments_button.callback = comments_callback
                view.add_item(comments_button)
                all_comments_button = Button(label="Past Comments", style=discord.ButtonStyle.secondary)
                async def all_comments_callback(interaction):
                    db_cursor.execute("SELECT id, vouch, sts FROM vouch_details WHERE user = ?", (target.id,))
                    all_vouches = db_cursor.fetchall()
                    comments = "\n".join(
                            f"Vouch Id: {v[0]} | Comment: {v[1]} | Status: {'Accepted' if v[2] == 1 else 'Denied' if v[2] == 2 else 'Pending'}"
                            for v in all_vouches
                        ) or "No comments yet."
                    await interaction.response.send_message(f"**All Past Comments:**\n{comments}", ephemeral=True)
                all_comments_button.callback = all_comments_callback
                view.add_item(all_comments_button)
                badges = []
                if stats[1] >= 1000:
                    badges.append(":gem:")
                elif stats[1] >= 500:
                    badges.append(":crown:")
                elif stats[1] >= 250:
                    badges.append(":trophy:")
                elif stats[1] >= 100:
                    badges.append(":medal:")
                elif stats[1] >= 50:
                    badges.append(":third_place:")
                else:
                    badges.append("No Badges Present!")
                embed.add_field(name="__Badges__", value=", ".join(badges), inline=False)
                embed.set_author(name=f"{target.name}")
                embed.set_footer(text=f"Repture | Your protector in digital realm", icon_url=self.bot.user.display_avatar.url)
                db_cursor.execute("SELECT type FROM marks WHERE user = ?", (target.id,))
                mark = db_cursor.fetchone()
                image_url = None
                db_cursor.execute("SELECT image FROM shop WHERE user = ?", (target.id,))
                image_data = db_cursor.fetchone()
                if image_data and image_data[0]:
                    embed.set_image(url=image_data[0])
                else:
                    embed.set_image(url=None)
                await ctx.send(embed=embed, view=view, delete_after=20)
                connection.commit()
            finally:
                connection.commit()

async def setup(bot):
    await bot.add_cog(Profile(bot))
