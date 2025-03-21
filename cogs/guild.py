import discord
from discord.ext import commands
import sqlite3
connection = sqlite3.connect("profile.db")
cursor = connection.cursor()
class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(name="set", aliases=["s"],invoke_without_command=True)
    async def set(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        embed = discord.Embed(
            title="Set Commands - 7",
            description="<...> Duty | [...] Optional",
            color=embed_color
        )
        embed.add_field(
            name="`set logs <channel>`",
            value="Notifies the members when a user gets marked.",
            inline=False
        )
        embed.add_field(
            name="`set dwc <role>`",
            value="Sets DWC role for the server.",
            inline=False
        )
        embed.add_field(
            name="`set config`",
            value="Shows the current configuration of the guild.",
            inline=False
        )
        embed.add_field(
            name="`set reset`",
            value="Reset the current configuration of the guild.",
            inline=False
        )
        embed.add_field(
            name="`set scammer <role>`",
            value="Sets scammer role for the server.",
            inline=False
        )
        embed.add_field(
            name="`set status <status>`",
            value="Toggles automatic ban system for scammers.",
            inline=False
        )
        embed.add_field(
            name="`set action <channel>`",
            value="Notifies the members when an action is taken on any marked user.",
            inline=False
        )
        embed.set_footer(text="Repture",icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)
    @set.command(name="log")
    @commands.has_permissions(manage_guild=True)
    async def set_logs(self, ctx, channel: discord.TextChannel):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO logs (guild, channel) VALUES (?, ?)", (ctx.guild.id, channel.id))
        conn.commit()
        conn.close()
        embed = discord.Embed(
            description=f"Alright, I would notify the members in {channel.mention} when a user gets marked.",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="dwc")
    @commands.has_permissions(manage_guild=True)
    async def set_dwc(self, ctx, role: discord.Role):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO configs (guild, dwc_role) VALUES (?, ?)", (ctx.guild.id, role.id))
        conn.commit()
        conn.close()
        embed = discord.Embed(
            description=f"Alright, I would give {role.mention} if a DWC joins the server.",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="scammer")
    @commands.has_permissions(manage_guild=True)
    async def set_scammer(self, ctx, role: discord.Role):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO configs (guild, scammer) VALUES (?, ?)", (ctx.guild.id, role.id))
        conn.commit()
        conn.close()
        embed = discord.Embed(
            description=f"Alright, I would give {role.mention} if a scammer joins the server.",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="action")
    @commands.has_permissions(manage_guild=True)
    async def set_action(self, ctx, channel: discord.TextChannel):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO logs (guild, action_channel) VALUES (?, ?)", (ctx.guild.id, channel.id))
        conn.commit()
        conn.close()
        embed = discord.Embed(
            description=f"Alright, I would notify the members in {channel.mention} when an action is taken on any marked user.",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="reset")
    @commands.has_permissions(manage_guild=True)
    async def set_reset(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM configs WHERE guild = ?", (ctx.guild.id,))
        cursor.execute("DELETE FROM logs WHERE guild = ?", (ctx.guild.id,))
        conn.commit()
        conn.close()
        embed = discord.Embed(
            description=f"Alright, reverting all the current configuration for **{ctx.guild.name}**",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="status")
    @commands.has_permissions(manage_guild=True)
    async def set_status(self, ctx, status: bool):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO configs (guild, auto_ban) VALUES (?, ?)", (ctx.guild.id, int(status)))
        conn.commit()
        conn.close()
        state = "enabled" if status else "disabled"
        embed = discord.Embed(
            title="Group Configuration",
            description=f"Successfully updated the automatic ban system settings for **{ctx.guild.name}**",
            color=embed_color
        )
        await ctx.send(embed=embed)
    @set.command(name="config")
    @commands.has_permissions(manage_guild=True)
    async def set_config(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("SELECT channel, action_channel FROM logs WHERE guild = ?", (ctx.guild.id,))
        logs_result = cursor.fetchone()
        logs_channel = self.bot.get_channel(logs_result[0]) if logs_result and logs_result[0] else "Not Set"
        action_channel = self.bot.get_channel(logs_result[1]) if logs_result and logs_result[1] else "Not Set"
        cursor.execute("SELECT scammer, dwc_role, auto_ban FROM configs WHERE guild = ?", (ctx.guild.id,))
        configs_result = cursor.fetchone()
        if not configs_result:
            embed = discord.Embed(
                description=f"No Guild Database Found For {ctx.guild.name}. Kindly use +help set to know more.",
                color=embed_color
            )
            await ctx.send(embed=embed)
            return
        scammer_role = ctx.guild.get_role(configs_result[0]) if configs_result[0] else "Not Set"
        dwc_role = ctx.guild.get_role(configs_result[1]) if configs_result[1] else "Not Set"
        auto_ban_status = bool(configs_result[2])
        conn.close()
        embed = discord.Embed(
            title=f"Group Configuration For {ctx.guild.name}",
            description="Below is your group configuration! If the role or channel says 'Not Set', you must set it to a role that the bot can access!",
            color=embed_color
        )
        embed.add_field(name="Logs Channel", value=logs_channel.mention if isinstance(logs_channel, discord.TextChannel) else logs_channel, inline=False)
        embed.add_field(name="Action Channel", value=action_channel.mention if isinstance(action_channel, discord.TextChannel) else action_channel, inline=False)
        embed.add_field(name="Scammer Role", value=scammer_role.mention if isinstance(scammer_role, discord.Role) else scammer_role, inline=False)
        embed.add_field(name="DWC Role", value=dwc_role.mention if isinstance(dwc_role, discord.Role) else dwc_role, inline=False)
        embed.add_field(name="Automatic Status", value=str(auto_ban_status), inline=False)
        await ctx.send(embed=embed)
    async def notify_mark(self, guild_id, user, mark_type, reason):
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("SELECT channel FROM logs WHERE guild = ?", (guild_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="User Marked",
                    description=f"User: {user}\nType: {mark_type}\nReason: {reason}",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
    async def notify_action(self, guild_id, user, action, details):
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("SELECT action_channel FROM logs WHERE guild = ?", (guild_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            channel_id = result[0]
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="Action Taken",
                    description=f"User: {user}\nAction: {action}\nDetails: {details}",
                    color=discord.Color.blue()
                )
                await channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        conn = sqlite3.connect("profile.db")
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM marks WHERE user = ?", (member.id,))
        mark_result = cursor.fetchone()
        cursor.execute("SELECT scammer, dwc_role, auto_ban FROM configs WHERE guild = ?", (member.guild.id,))
        config_result = cursor.fetchone()
        conn.close()
        if mark_result and config_result:
            mark_type = mark_result[0]
            scammer_role_id, dwc_role_id, auto_ban = config_result
            if mark_type == 1 and auto_ban:
                await member.ban(reason="User marked as scammer")
                return
            if mark_type == 1 and scammer_role_id:
                scammer_role = member.guild.get_role(scammer_role_id)
                if scammer_role:
                    await member.add_roles(scammer_role, reason="User marked as scammer")
            elif mark_type == 2 and dwc_role_id:
                dwc_role = member.guild.get_role(dwc_role_id)
                if dwc_role:
                    await member.add_roles(dwc_role, reason="User marked as DWC")
async def setup(bot):
    await bot.add_cog(Guild(bot))
