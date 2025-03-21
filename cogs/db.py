import discord
from discord.ext import commands
import sqlite3

class Db(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    connection = sqlite3.connect("profile.db")
    cursor = connection.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS details (
    user INTEGER,
    token TEXT
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS configs (
    guild INTEGER,
    scammer INTEGER,
    dwc INTEGER,
    dwc_role INTEGER DEFAULT NULL,
    auto_ban INTEGER DEFAULT 0
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS badges (
    user INTEGER,
    badge INTEGER
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS np (
    user INTEGER
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    user INTEGER,
    type INTEGER,
    reason TEXT
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS vouches (
    user INTEGER,
    overall INTEGER DEFAULT 0,
    positive INTEGER DEFAULT 0,
    negative INTEGER DEFAULT 0
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS vouch_details (
    sts INTEGER DEFAULT 0,
    author INTEGER,
    user INTEGER,
    id TEXT,
    vouch TEXT
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS shop (
    user INTEGER,
    name TEXT,
    products TEXT,
    image TEXT DEFAULT None,
    thmb TEXT DEFAULT None,
    color TEXT,
    web TEXT DEFAULT None,
    forum TEXT DEFAULT None
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    guild INTEGER,
    channel INTEGER,
    action_channel INTEGER DEFAULT NULL
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS command_stats (
    user INTEGER,
    total_commands INTEGER DEFAULT 0
)''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS blacklist (
    user INTEGER PRIMARY KEY
)''')
    cursor.execute('''
INSERT OR IGNORE INTO command_stats (rowid, total_commands)
VALUES (1, 0)
''')

    connection.commit()

async def setup(bot):
    await bot.add_cog(Db(bot))
