from datetime import datetime
from datetime import timedelta
import discord
import asyncio

token = 'YOUR TOKEN HERE'
client = discord.Client()

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
        embedStart3.add_field(name="Rental Bot", value="How long is it being rented for (DAYS)?")
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

client.run(token)
