from datetime import datetime
from datetime import timedelta
import discord
import asyncio
import sqlite3

token = 'YOUR TOKEN HERE'
client = discord.Client()
connection = sqlite3.connect('rentals.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS rental (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, renter TEXT, duration INTEGER, price INTEGER, start TEXT, end TEXT)")
connection.commit()

@client.event
async def on_ready():
    print('-------------------------')
    print('Rental Bot v1.0.0')
    print('Made by @Expected')
    print('-------------------------')

@client.event
async def on_message(message):
    if message.content.startswith('!rental'):
        # STARTING EMBED
        embedStart = discord.Embed(color=0xFF0000)
        embedStart.add_field(name="Rental Bot", value="What bot are you renting?")
        embedStart.set_footer(text="Created by @Expected")
        message = await message.channel.send(embed=embedStart)

        embedStart2 = discord.Embed(color=0xFF0000)
        embedStart2.add_field(name="Rental Bot", value="Who's renting it?")
        embedStart2.set_footer(text="Created by @Expected")

        embedStart3 = discord.Embed(color=0xFF0000)
        embedStart3.add_field(name="Rental Bot", value="How long is it being rented for (Days)?")
        embedStart3.set_footer(text="Created by @Expected")

        embedStart4 = discord.Embed(color=0xFF0000)
        embedStart4.add_field(name="Rental Bot", value="How much is the rental?")
        embedStart4.set_footer(text="Created by @Expected")

        botName = await client.wait_for('message')
        await botName.delete()
        await message.edit(embed=embedStart2)

        renterName = await client.wait_for('message')
        await renterName.delete()
        await message.edit(embed=embedStart3)
        
        rentalLength = await client.wait_for('message')
        await rentalLength.delete()
        await message.edit(embed=embedStart4)
        
        rentalPrice = await client.wait_for('message')
        await rentalPrice.delete()
        await message.delete()

        startDate = datetime.now()
        endDate = startDate + timedelta(days=int(rentalLength.content))

        # EMBED CREATION
        embed = discord.Embed(title='New Rental Created', color=0x00FF00)
        embed.set_thumbnail(url='https://texomainspection.com/wp-content/uploads/2013/09/cropped-checkmark.png')
        embed.add_field(name='Bot Name:', value='{}'.format(botName.content), inline=False)
        embed.add_field(name='Renter Name:', value='{}'.format(renterName.content), inline=False)
        embed.add_field(name='Rental Duration:', value='{} Days'.format(rentalLength.content), inline=False)
        embed.add_field(name='Rental Price:', value='${}'.format(rentalPrice.content), inline=False)
        embed.add_field(name='Start Date:', value='{}'.format(startDate), inline=False)
        embed.add_field(name='End Date:', value='{}'.format(endDate), inline=False)
        embed.set_footer(icon_url='https://pbs.twimg.com/profile_images/1325672283881484289/oaGtVIOD_400x400.png', text='Created by @Expected')
        await message.channel.send(embed=embed)

        cursor.execute("INSERT INTO rental(name, renter, duration, price, start, end) VALUES (?, ?, ?, ?, ?, ?)", (botName.content, renterName.content, rentalLength.content, rentalPrice.content, startDate, endDate))
        connection.commit()

    if message.content.startswith('!view'):
        rows = cursor.execute("SELECT id, name, renter, duration, price, start, end FROM rental").fetchall()
        for x in rows:
            embed = discord.Embed(title='Rental #{}'.format(x[0]), color=0x0000FF)
            embed.set_thumbnail(url='https://www.pngkit.com/png/detail/231-2316751_database-database-icon-png.png')
            embed.add_field(name='Bot Name:', value=x[1], inline=False)
            embed.add_field(name='Renter Name:', value=x[2], inline=False)
            embed.add_field(name='Rental Duration:', value='{} day(s)'.format(x[3]), inline=False)
            embed.add_field(name='Rental Price:', value='${}'.format(x[4]), inline=False)
            embed.add_field(name='Start Date:', value=x[5], inline=False)
            embed.add_field(name='End Date:', value=x[6], inline=False)
            embed.set_footer(icon_url='https://pbs.twimg.com/profile_images/1325672283881484289/oaGtVIOD_400x400.png', text='Created by @Expected')
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction('\U0001F5D1')

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    if str(payload.emoji) == '\U0001F5D1':
        channel = await client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        try:
            embed = message.embeds[0]
            rental_id = embed.title.rsplit('#', 1)[1]
        except:
            return
        await message.delete()
        cursor.execute("DELETE FROM rental WHERE id={}".format(rental_id))
        connection.commit()

client.run(token)
