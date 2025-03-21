import discord
from discord.ext import commands
import sqlite3
import random
import string

connection = sqlite3.connect("profile.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS details (user INTEGER, token TEXT)''')

class Vouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_random_token(self, length):
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for _ in range(length))
        return token  
    
    @commands.command(name="search")
    async def search_product(self, ctx, *, product_name: str):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT user FROM shop WHERE products LIKE ?", (f"%{product_name}%",))
        results = cursor.fetchall()

        if results:
            users = [await self.bot.fetch_user(row[0]) for row in results]
            usernames = "\n".join(user.name for user in users)
            embed = discord.Embed(
                title="Product Search",
                description=f"We found matches! Their Discord usernames are listed below:\n\n{usernames}",
                color=embed_color
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Product Search",
                description=f"No users found with the product '{product_name}'.",
                color=embed_color
            )
            await ctx.send(embed=embed)
    @commands.command(name="vouch", aliases=["rep","r"])
    async def _vouch(self, ctx, mem: discord.Member=None, *, vouch=None):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        if mem == ctx.author:
            embed = discord.Embed(description=f"{ctx.author.mention} You cannot vouch yourself.", color=embed_color)
            await ctx.reply(embed=embed)
        else:
            if vouch is None:
                embedd = discord.Embed(description=f"{ctx.author.mention} Please mention a reason to vouch.", color=embed_color)
                await ctx.reply(embed=embedd)
            elif not any(char.isdigit() for char in vouch):
                embedd = discord.Embed(description=f"{ctx.author.mention} Your vouch was automatically denied for not specifying the amount or the price of the product.", color=embed_color)
                await ctx.send(embed=embedd)
            elif not any(currency_symbol in vouch for currency_symbol in ["₹", "$", "£", "€"]):
                embedd = discord.Embed(description=f"{ctx.author.mention} Your vouch was automatically denied because currency symbol (₹/$/£/€) is missing.", color=embed_color)
                await ctx.send(embed=embedd)
            else:
                embeds = discord.Embed(description=f"{ctx.author.mention} Vouch submitted for {mem.display_name} successfully.", color=embed_color)
                await ctx.reply(embed=embeds)

                length = 6
                id = self.generate_random_token(length)

                embedu = discord.Embed(description=f"""You have received a positive vouch.

    **__Vouch Details:__**
  
    Vouch : {vouch}
    Author : {ctx.author}
    Id : {id}

    - If you think this vouch is done by mistakenly, please ignore.""", color=embed_color)

                if mem is None or mem.bot:
                    embed = discord.Embed(description=f"{ctx.author.mention} Unable to send a vouch to the specified user.", color=embed_color)
                    await ctx.reply(embed=embed)
                    return

                try:
                    await mem.send(embed=embedu)
                except discord.Forbidden:
                    embed = discord.Embed(description=f"{ctx.author.mention} Could not send a direct message to {mem.display_name}.", color=embed_color)
                    await ctx.reply(embed=embed)

                cursor.execute("INSERT INTO vouch_details (author, user, id, vouch) VALUES (?, ?, ?, ?)", (ctx.author.id, mem.id, id, vouch))
                connection.commit()

                channel = self.bot.get_channel(1338116728575492127)
                embedp = discord.Embed(description=f"""{self.bot.user.name} New Vouch Submitted.

    **__Vouch Details:__**

    Author : {ctx.author}
    Author Id : {ctx.author.id}

    Vouched User : {mem.name}
    Vouched User Id : {mem.id}

    Vouch Id : {id}
    Text : {vouch}""", color=embed_color)
                await channel.send(embed=embedp)
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (message.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        if message.author == self.bot.user:
            return
        cursor.execute("SELECT user FROM np WHERE user = ?", (message.author.id,))
        np = cursor.fetchone()
        if np:
            if message.content.startswith('accept'):
                role = discord.utils.get(message.guild.roles, name="new role")
                if role in message.author.roles:
                    parts = message.content.split()
                    command = parts[1] 
                    if command:
                        try:
                            vouch_id = command
                            cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (vouch_id,))
                            vouch = cursor.fetchone()
                            if vouch:
                                if vouch[0] == 1:
                                    await message.channel.send("This vouch is already accepted.")
                                elif vouch[0] == 2:
                                    await message.channel.send("This vouch is already denied.")
                                else:
                                    embed = discord.Embed(description=f"Successfully accepted the vouch with ID - `{vouch_id}`", color=embed_color)
                                    await message.channel.send(embed=embed)
                                    cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (1, vouch_id))
                                    user_id = vouch[2]
                                    user = await self.bot.fetch_user(user_id)
                                    embedu = discord.Embed(description=f"Your vouch with ID - `{vouch_id}` was accepted.", color=embed_color)
                                    await user.send(embed=embedu)

                                    cursor.execute("SELECT overall, positive FROM vouches WHERE user = ?", (user_id,))
                                    count = cursor.fetchone()
                                    if count is None:
                                        old_overall = 0
                                        old_positive = 0
                                        cursor.execute("INSERT INTO vouches (user, overall, positive) VALUES (?, ?, ?)", (user_id, old_overall, old_positive))
                                    else:
                                        old_overall = count[0]
                                        old_positive = count[1]

                                    new_overall = old_overall + 1
                                    new_positive = old_positive + 1

                                    cursor.execute("UPDATE vouches SET overall = ?, positive = ? WHERE user = ?", (new_overall, new_positive, user_id))
                                    connection.commit()

                                    channel = self.bot.get_channel(1169919193286717460)
                                    embedss = discord.Embed(description=f"""
            **__Vouch Accepted__**

            Admin: {message.author}
            Vouched User: {user}
            Vouch: {vouch[3]}
            ID: {vouch_id}
            """, color=embed_color)
                                    await channel.send(embed=embedss)
                            else:
                                embed = discord.Embed(description=f"The vouch ID is invalid.", color=embed_color)
                                await message.channel.send(embed=embed)
                        except ValueError:
                            await message.channel.send("Invalid vouch ID.")

    


    @commands.command(name="accept", aliases=["a"])
    async def _accept(self, ctx, *, id):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (id,))
        vouch = cursor.fetchone()
        if vouch:
            if vouch[0] == 1:
                await ctx.reply(content="This vouch is already accepted.")
            elif vouch[0] == 2:
                await ctx.reply(content="This vouch is already denied.")
            else:
                embed = discord.Embed(description=f"Sucessfully, Accepted the vouch with id - `{id}`", color=embed_color)
                await ctx.reply(embed=embed)
                cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (1, id))
                user_id = vouch[2]
                user = await self.bot.fetch_user(user_id)
                embedu = discord.Embed(description=f"Your vouch with ID - `{id}` was accepted.", color=embed_color)
                message = await user.send(embed=embedu)

                cursor.execute("SELECT overall, positive FROM vouches WHERE user = ?", (user_id,))
                count = cursor.fetchone()
                if count is None:
                    old_overall = 0
                    old_positive = 0
                    cursor.execute("INSERT INTO vouches (user, overall, positive) VALUES (?, ?, ?)", (user_id, old_overall, old_positive))
                else:
                    old_overall = count[0]
                    old_positive = count[1]

                new_overall = old_overall + 1
                new_positive = old_positive + 1

                cursor.execute("UPDATE vouches SET overall = ?, positive = ? WHERE user = ?", (new_overall, new_positive, user_id))
                connection.commit()

                channel = self.bot.get_channel(1338116728575492127)
                embedss = discord.Embed(description=f"""
**__Vouch Accepted__**

Admin : {ctx.author}
Vouched User : {user}
Vouch : {vouch[3]}
Id : {id}
""", color=embed_color)
                await channel.send(embed=embedss)
        else:
            embed = discord.Embed(description=f" The vouch ID is invalid.", color=embed_color)
            await ctx.reply(embed=embed)

    @commands.group(name="deny", aliases=['d'])

    async def _deny(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description=f"Please execute the command properly, choose on of the reasons to deny the vouch:\nincorrect\nlow-amount\nbot\nExaple - `{self.bot.command_prefix}deny incorrect`", color=embed_color)
            await ctx.reply(embed=embed)

    @_deny.command(name="incorrect", aliases=['inc'])
    async def deny_inc(self, ctx, *, id):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (id,))
        vouch = cursor.fetchone()
        if vouch:
                if vouch[0] == 1:
                    await ctx.reply(content="This vouch is already accepted.")
                elif vouch[0] == 2:
                    await ctx.reply(content="This vouch is already denied.")
                else:
                    embed = discord.Embed(description=f" Sucessfully, denied the vouch with id - `{id}` for reason `Incorrect Vouch.`", color=embed_color)
                    await ctx.reply(embed=embed)
                    cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (2, id))
                    connection.commit()
                    user_id = vouch[2]
                    user = await self.bot.fetch_user(user_id)
                    embedu = discord.Embed(description=f"""Your vouch with ID - `{id}` was denied.

> This vouch was denied as the format of vouch was incorrect or extra-ordinary.
> Please revouch with correct statements.
> Example - `{self.bot.command_prefix}rep <user> Legit 1x Minecraft Acc in 7$`
""", color=embed_color)
                    message = await user.send(embed=embedu)
                    channel = self.bot.get_channel(1338116728575492127)
                    embedss = discord.Embed(description=f"""
**__Vouch Denied__**

Admin : {ctx.author}
Vouched User : {user}
Vouch : {vouch[3]}
Reason : Incorrect
Id : {id}
""", color=embed_color)
                await channel.send(embed=embedss)
        else:
            embed = discord.Embed(description=f"The vouch ID is invalid.", color=embed_color)
            await ctx.reply(embed=embed)
    
    @_deny.command(name="bc", aliases=['bot-currency'])
    async def deny_bot(self, ctx, *, id):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (id,))
        vouch = cursor.fetchone()
        if vouch:
                if vouch[0] == 1:
                    await ctx.reply(content="This vouch is already accepted.")
                elif vouch[0] == 2:
                    await ctx.reply(content="This vouch is already denied.")
                else:
                    embed = discord.Embed(description=f"Sucessfully, denied the vouch with id - `{id}` for reason `Bot-Currency Vouch.`", color=embed_color)
                    await ctx.reply(embed=embed)
                    cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (2, id))
                    connection.commit()
                    user_id = vouch[2]
                    user = await self.bot.fetch_user(user_id)
                    embedu = discord.Embed(description=f""" Your vouch with ID - `{id}` was denied.

> This vouch was denied as the vouch contained bot-currency which is not allowed as per our **vouch-policy.**
""", color=embed_color)
                    message = await user.send(embed=embedu)
                    channel = self.bot.get_channel(1338116728575492127)
                    embedss = discord.Embed(description=f"""
**__Vouch Denied__**

Admin : {ctx.author}
Vouched User : {user}
Vouch : {vouch[3]}
Reason : Bot-Currency
Id : {id}
""", color=embed_color)
                await channel.send(embed=embedss)
        else:
            embed = discord.Embed(description=f" The vouch ID is invalid.", color=embed_color)
            await ctx.reply(embed=embed)
    
    @_deny.command(name="low-amount", aliases=['la'])
    async def deny_la(self, ctx, *, id):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (id,))
        vouch = cursor.fetchone()
        if vouch:
                if vouch[0] == 1:
                    await ctx.reply(content="This vouch is already accepted.")
                elif vouch[0] == 2:
                    await ctx.reply(content="This vouch is already denied.")
                else:
                    embed = discord.Embed(description=f"Sucessfully, denied the vouch with id - `{id}` for reason `Low Amount Vouch.`", color=embed_color)
                    await ctx.reply(embed=embed)
                    cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (2, id))
                    connection.commit()
                    user_id = vouch[2]
                    user = await self.bot.fetch_user(user_id)
                    embedu = discord.Embed(description=f"""Your vouch with ID - `{id}` was denied.

> This vouch was denied as the vouch contained Low-Amount which is not allowed as per our **vouch-policy.**
> The minimum amount to vouch is `0.5$ / 45 Rs`
""", color=embed_color)
                    message = await user.send(embed=embedu)
                    channel = self.bot.get_channel(1338116728575492127)
                    embedss = discord.Embed(description=f"""
**__Vouch Denied__**

Admin : {ctx.author}
Vouched User : {user}
Vouch : {vouch[3]}
Reason : Low Amount
Id : {id}
""", color=embed_color)
                await channel.send(embed=embedss)
        else:
            embed = discord.Embed(description=f"The vouch ID is invalid.", color=embed_color)
            await ctx.reply(embed=embed)

    

    @commands.command(name="verify",aliases=["v"])
    async def _verify(self, ctx, *, id):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT sts, id, user, vouch FROM vouch_details WHERE id = ?", (id,))
        vouch = cursor.fetchone()
        if vouch:
                if vouch[0] == 1:
                    await ctx.reply(content="This vouch is already accepted.")
                elif vouch[0] == 2:
                    await ctx.reply(content="This vouch is already denied.")
                elif vouch[0] == 3:
                    await ctx.reply(content="This vouch is already held for manual verification.")
                else:
                    embed = discord.Embed(description=f"Sucessfully, sent the vouch with id - `{id}` for verification.", color=embed_color)
                    await ctx.reply(embed=embed)
                    cursor.execute("UPDATE vouch_details SET sts = ? WHERE id = ?", (3, id))
                    connection.commit()
                    user_id = vouch[2]
                    user = await self.bot.fetch_user(user_id)
                    embedu = discord.Embed(description=f"""Your vouch with ID - `{id}` needs a manual verification.
Join our support guild to get your vouches verified.
You have 24 hours to do so.
Link : 
""", color=embed_color)
                    message = await user.send(embed=embedu)
                    channel = self.bot.get_channel(1338116728575492127)
                    embedss = discord.Embed(description=f"""
**__Vouch Verification__**

Admin : {ctx.author}
Vouched User : {user}
Vouch : {vouch[3]}
ID : {id}
""", color=embed_color)
                await channel.send(embed=embedss)
        else:
            embed = discord.Embed(description=f"The vouch ID is invalid.", color=embed_color)
            await ctx.reply(embed=embed)

    @commands.command(name="top")
    async def top_leaderboard(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6
        cursor.execute("SELECT user, positive FROM vouches ORDER BY positive DESC LIMIT 10")
        top_users = cursor.fetchall()

        if not top_users:
            embed = discord.Embed(
                title=f"{self.bot.user.name} Leaderboard",
                description="No vouches found.",
                color=embed_color
            )
            await ctx.send(embed=embed)
            return

        leaderboard = "\n".join(
            [f"`[{str(index + 1).zfill(2)}]` | **{await self.bot.fetch_user(row[0])}** | Count - `{row[1]}`" 
             for index, row in enumerate(top_users)]
        )

        embed = discord.Embed(
            title=f"{self.bot.user.name} Leaderboard",
            description=leaderboard,
            color=embed_color
        )
        embed.set_footer(text="Repture",icon_url=self.bot.user.display_avatar.url) 
        await ctx.send(embed=embed)

    @commands.command(name="token")
    async def generate_token(self, ctx):
        cursor.execute("SELECT color FROM shop WHERE user = ?", (ctx.author.id,))
        result = cursor.fetchone()
        embed_color = int(result[0], 16) if result and result[0] else 0xADD8E6

        cursor.execute("SELECT token FROM details WHERE user = ?", (ctx.author.id,))
        existing_token = cursor.fetchone()

        if existing_token:
            try:
                embed = discord.Embed(
                    title="Your Token",
                    description=f"Here is your existing token: `{existing_token[0]}`",
                    color=embed_color
                )
                await ctx.author.send(embed=embed)
                await ctx.reply(embed=discord.Embed(description="Your existing token has been sent to your DM.", color=embed_color))
            except discord.Forbidden:
                await ctx.reply(embed=discord.Embed(description="Unable to send you a DM. Please check your privacy settings.", color=embed_color))
            return

        token = self.generate_random_token(12)

        cursor.execute("INSERT INTO details (user, token) VALUES (?, ?)", (ctx.author.id, token))
        connection.commit()

        try:
            embed = discord.Embed(
                title="Your Token",
                description=f"Here is your generated token: `{token}`",
                color=embed_color
            )
            await ctx.author.send(embed=embed)
            await ctx.reply(embed=discord.Embed(description="Token has been sent to your DM.", color=embed_color))
        except discord.Forbidden:
            await ctx.reply(embed=discord.Embed(description="Unable to send you a DM. Please check your privacy settings.", color=embed_color))

async def setup(bot):
    await bot.add_cog(Vouch(bot))
