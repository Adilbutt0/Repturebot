import discord
from discord.ext import commands
import sqlite3
connection = sqlite3.connect("profile.db")
cursor = connection.cursor()
class HelpVIew(discord.ui.Select):
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx  # Save the context
        opts = [discord.SelectOption(label="Vouch"),
                discord.SelectOption(label="General"),
                discord.SelectOption(label="Guild"),
                discord.SelectOption(label="Leaderboard")]

        super().__init__(placeholder="Select a Category of All Modules", max_values=1, min_values=1, options=opts)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author: 
            await interaction.response.send_message(content="You Can't Use This Menu!", ephemeral=True)
            return

        embed = None
        if self.values[0] == "Vouch":
            embed = discord.Embed(title="__Vouch__", description="• `profile` , `vouch` , `rep` , `reset` , `product` , `report` , `search` , `status` , `shop` , `forum` , `web` , `image` , `thumb` , `token` , `color` , `embedcolor` , `display`")
        elif self.values[0] == "General":
            embed = discord.Embed(title="__General__", description="• `invite` , `uptime` , `ping`")
        elif self.values[0] == "Guild":
            embed = discord.Embed(title="__Guild__", description="• `set` , `set action` , `set logs` , `set reset` , `set config` , `set dwc` , `set scammer` , `set status`")
        elif self.values[0] == "Leaderboard":
            embed = discord.Embed(title="__Top__", description="• `top`")

        if embed:
            embed.set_author(name=f"{self.ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
            embed.set_footer(text=f"Showing Page {['Vouch', 'General', 'Guild', 'Leaderboard'].index(self.values[0]) + 1}/4", icon_url=self.bot.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

class dropdown(discord.ui.View):

    def __init__(self, bot, ctx):
        super().__init__() 
        self.bot = bot
        self.ctx = ctx
        self.add_item(HelpVIew(bot, ctx))

class CogHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def help(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        commands_list = list(ctx.bot.walk_commands())
        usable_commands = [c for c in commands_list if await c.can_run(ctx)] 
        em = discord.Embed(description=f"• Global prefix is `+`\n• Total Commands: `{len(commands_list)}` | Usable by you (here): `{len(usable_commands)}`\n• [Get Repture](<https://discord.com/api/oauth2/authorize?client_id=1251802551804887050&permissions=8&scope=bot>) | [Support Server](<https://discord.gg/repturebot>)\n• Type `+help <command | module>` for more info\n**Module**\n{vouch_emo} Vouch\n{general_emo} General\n{guild_emo} Guild\n{top_emo} Leaderboard",color=embed_color )
        em.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        em.set_footer(text="Repture", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em, content="https://discord.gg/repturebot", view=dropdown(self.bot, ctx))

async def setup(bot):
    await bot.add_cog(CogHelp(bot))