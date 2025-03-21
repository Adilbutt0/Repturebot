import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
import jishaku

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = sqlite3.connect("profile.db")
        self.cursor = self.db.cursor()

    async def on_command_completion(self, ctx):
        self.cursor.execute("SELECT total_commands FROM command_stats WHERE user = ?", (ctx.author.id,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("UPDATE command_stats SET total_commands = total_commands + 1 WHERE user = ?", (ctx.author.id,))
        else:
            self.cursor.execute("INSERT INTO command_stats (user, total_commands) VALUES (?, ?)", (ctx.author.id, 1))
        self.db.commit()

bot = Bot(command_prefix='+', intents=discord.Intents.all())
bot.remove_command('help')
bot.owner_id = 1162455661041434787

if __name__ == "__main__":
    async def initialize():
        for module in os.listdir('cogs'):
            if module.endswith(".py"):
                await bot.load_extension(f'cogs.{module[:-3]}')
        await bot.load_extension("jishaku")

    asyncio.run(initialize())

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user.name}')
    await bot.change_presence(status=discord.Status.idle)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    database = sqlite3.connect("profile.db")
    db_cursor = database.cursor()
    db_cursor.execute("SELECT color FROM shop WHERE user = ?", (message.author.id,))
    result = db_cursor.fetchone()
    embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6

    context = await bot.get_context(message)
    if context.valid:
        db_cursor.execute("SELECT user FROM blacklist WHERE user = ?", (message.author.id,))
        if db_cursor.fetchone():
            embed = discord.Embed(
                description="It appears that your access to our bot services has been globally restricted. "
                            "If you wish to contest this decision, we kindly ask you to join our [Support Server](https://discord.gg/repturebot).",
                color=embed_color
            )
            view = discord.ui.View()
            support_button = discord.ui.Button(label="Support Server", url="https://discord.gg/repturebot", style=discord.ButtonStyle.link)
            view.add_item(support_button)
            await message.channel.send(embed=embed, view=view, delete_after=5)
            database.close()
            return

    database.close()
    await bot.process_commands(message)

bot.run("token",reconnect=True)