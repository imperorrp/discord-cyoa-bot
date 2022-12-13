#discord cyoa bot 

#v1.1(13th Dec 2022)----------------------------------------------------------
#features:
#custom game creation via google docs- free cyoa game databases, easy to edit, anyone can create

#bot logic: 1. Bot maintains a json file list of adventure names with their g-sheet
#              ids
#           2. Bot runs, waiting for commands (about, help, display advs, start adv
#              stop adv)
#           3. Upon start adv, bot retrieves first prompt data from gsheet, 
#              posts embed with that, adds 'buttons' to select more options
#           4. Based on 'button' selection, bot gets new prompts from gsheet, 
#              refreshes embed with that, adds new 'buttons'
#
#   (3.)->  a. 'adventure' class objects are created for each new adventure instance in a guild.
#           b. class variables: guild, adventure number, current page, message id, adventure name
#           c. every time an option is selected, page number is updated for the adv obj
#              and the new page + options are loaded from gsheets with get_page(). Button_sender() 
#              then creates and sends a new embed with buttons for the process to repeat. 


#importing third party modules->
import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import gspread
import json

#importing bot utility code->
import utilities.manage_adv as advmanager
import utilities.send_adv as advsender

#Loading credentials, authorizing gspread API->
gc = gspread.service_account(filename='discord-cyoa-bot-a171fc3ed3d6.json')
print('-Gspread API authorized')

#loading adventures.json file->
f = open('adventures.json',)
adv = json.load(f)
list_adv = adv["list_of_adventures"]
f.close()

TOKEN = open('token.txt','r').readline()
PREFIX = '>'
INTENTS = discord.Intents.default()
#INTENTS.message_content = True 
client = commands.Bot(command_prefix=PREFIX, intents=INTENTS, help_command=None)

@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')

@client.command()
async def add(ctx, arg1, arg2):
    print(f'">add" command invoked')
    name = arg1
    gsheet_id = arg2
    returned = advmanager.add_adventure(name, gsheet_id)
    if returned==1:
        print(f'add_adventure() successful.')
        await ctx.send("Adventure successfully added. Try `>adventures` to view in list.")
    elif returned==0:
        print(f'add_adventure() failed.')
        await ctx.send("Error: adventure not added. Please make sure:\n1. The sheet was shared with and is visible to me! (discord-cyoa-bot@discord-cyoa-bot.iam.gserviceaccount.com)\n2. Your `>add` command format is correct\n3. You've got the right sheet ID/key.\n\nTry again!")

@client.command()
async def remove(ctx, arg1: int):
    print(f'">remove" command invoked')
    adv_num = arg1
    returned = advmanager.remove_adventure(adv_num)
    if returned==1:
        print(f'remove_adventure() successful.')
        await ctx.send("Adventure successfully removed. Try `>adventures` to view in list.")
    elif returned==0:
        print(f'remove_adventure() failed.')
        await ctx.send("Error: adventure not removed. Please pick a valid adventure number (use `>adventures` to view) to remove and try again!")

@client.command()
async def adventures(ctx):
    print(f'">adventures" command invoked')
    f3 = open('adventures.json',)
    advs = json.load(f3)
    list_advs = advs["list_of_adventures"]
    f3.close()
    embed = discord.Embed(
        title = "Available Adventures",
        colour = discord.Colour.greyple()
    )
    i=1
    for adventure in list_advs:
        name = adventure["name"]
        url = 'https://docs.google.com/spreadsheets/d/'+ adventure["sheetid"] +'/'
        description = adventure["description"]
        embed.add_field(name=f"({i}) {name}", value=f'[Link]({url})\n*{description}*', inline=False)
        i+=1
    await ctx.send(embed=embed)
    print(f'">adventures" command embed sent.')

@client.command()
async def end(ctx, arg1: int):
    print(f'">end" command invoked with "arg={arg1}"')
    advnum = arg1
    guildid = 0
    for p in advmanager.advs:
        if ((p.advnum == advnum) and (p.guild == ctx.guild)):
            guildid = p.guild.id
            msgid = p._messageid
            msg = await ctx.fetch_message(msgid)
            await msg.delete()
            del p 
            print(f'adventure w/ message id: "{msgid}" deleted.')
    print(f'Destroyed adventure instance: "{advnum}" in guild id: "{guildid}"')
    ctx.send(f'Ended adventure {arg1}')

@client.command()
async def start(ctx, arg1: int):
    print(f'">start" command invoked with "arg={arg1}"')
    advnum = arg1
    page_1 = advmanager.get_page(advnum, 1)
    f3 = open('adventures.json',)
    advs = json.load(f3)
    list_advs = advs["list_of_adventures"]
    f3.close()
    first_advname = list_advs[advnum-1]["name"]

    content = page_1[1] #main content of page 1
    #global options
    options = page_1[2:]
    msg = await advsender.button_sender(ctx, first_advname, page_1)
    msgid = msg.id
    adventure : advmanager.Adventure = advmanager.get_adventure(msgid, advnum, ctx.guild)
    advname = adventure.advname
    advnum = adventure.advnum
    print(f'"{advname}" Adventure (ID: "{advnum}") instance created:\n{adventure}')

@client.on_click()
async def option_1(i: discord.Interaction, button):
    print(f'Option 1 clicked. Getting adventure...')
    #print(i)
    msgid = i.message.id
    guild = i.guild
    adventure: advmanager.Adventure = advmanager.get_adventure(msgid, 0, guild)
    print(f'adventure: "{adventure}"')
    pagenum = adventure.currentpage
    advnum = adventure.advnum
    advname = adventure.advname
    page = advmanager.get_page(advnum, pagenum)
    options = page[2:]
    new_page_num = options[0].split('@')[1]
    adventure.set_page(new_page_num)
    print(f'Option 1 selected. Set new page to "{new_page_num}"')
    new_page = advmanager.get_page(advnum, new_page_num)
    msg = await advsender.button_sender(i, advname, new_page, msgid)
    print(f'Message edited. Awaiting next on_click()...\n')

@client.on_click()
async def option_2(i: discord.Interaction, button):
    print(f'Option 2 clicked. Getting adventure...')
    #print(i)
    msgid = i.message.id
    guild = i.guild
    adventure: advmanager.Adventure = advmanager.get_adventure(msgid, 0, guild)
    print(f'adventure: "{adventure}"')
    pagenum = adventure.currentpage
    advnum = adventure.advnum
    advname = adventure.advname
    page = advmanager.get_page(advnum, pagenum)
    options = page[2:]
    new_page_num = int(options[1].split('@')[1])
    adventure.set_page(new_page_num)
    print(f'Option 2 selected. Set new page to "{new_page_num}"')
    new_page = advmanager.get_page(advnum, new_page_num)
    msg = await advsender.button_sender(i, advname, new_page, msgid)
    print(f'Message edited. Awaiting next on_click()...\n')

@client.on_click()
async def option_3(i: discord.Interaction, button):
    print(f'Option 1 clicked. Getting adventure...')
    #print(i)
    msgid = i.message.id
    guild = i.guild
    adventure: advmanager.Adventure = advmanager.get_adventure(msgid, 0, guild)
    print(f'adventure: "{adventure}"')
    pagenum = adventure.currentpage
    advnum = adventure.advnum
    advname = adventure.advname
    page = advmanager.get_page(advnum, pagenum)
    options = page[2:]
    new_page_num = options[2].split('@')[1]
    adventure.set_page(new_page_num)
    print(f'Option 3 selected. Set new page to "{new_page_num}"')
    new_page = advmanager.get_page(advnum, new_page_num)
    msg = await advsender.button_sender(i, advname, new_page, msgid)
    print(f'Message edited. Awaiting next on_click()...\n')

@client.on_click()
async def option_4(i: discord.Interaction, button):
    print(f'Option 1 clicked. Getting adventure...')
    #print(i)
    msgid = i.message.id
    guild = i.guild
    adventure: advmanager.Adventure = advmanager.get_adventure(msgid, 0, guild)
    print(f'adventure: "{adventure}"')
    pagenum = adventure.currentpage
    advnum = adventure.advnum
    advname = adventure.advname
    page = advmanager.get_page(advnum, pagenum)
    options = page[2:]
    new_page_num = options[3].split('@')[1]
    adventure.set_page(new_page_num)
    print(f'Option 4 selected. Set new page to "{new_page_num}"')
    new_page = advmanager.get_page(advnum, new_page_num)
    msg = await advsender.button_sender(i, advname, new_page, msgid)
    print(f'Message edited. Awaiting next on_click()...\n')

#about bot->
@client.command()
async def about(ctx):
    print('">about" command invoked.')
    embed = discord.Embed(
        title = 'About Me!',
        color = discord.Colour.greyple()
    )
    embed.add_field(name='Discord CYOA bot', value="Discord CYOA Bot lets you create your own choose-your-own-adventure text games on Google Sheets and play them on Discord. [Sample Adventure Google Sheet](https://docs.google.com/spreadsheets/d/1_ykm2JOQKqlWE9d_VUdWY1YApH0DfzVDQDbM__L4VtI/edit#gid=0)\n\nChange only the content and options- make sure to keep the rest of the template intact, and remember to follow up on options with '@x', indicating the page number to jump to for that option. Toggling the sheet's view to public is not necessary- sharing it with the bot's email (see add-adventure in >help) also works if private. \n\nAdd me to your own server- adventures are playable from anywhere!", inline=False)
    embed.add_field(name='Created by', value='imp#7772', inline=False)
    await ctx.send(embed=embed)
    print(f'">about" command embed sent.')


#commands functions->
@client.command()
async def help(ctx):
    print(f'">help" command invoked.')
    embed = discord.Embed(
        title = "CYOA Bot Help",
        colour = discord.Colour.greyple()
    )
    embed.add_field(name="About", value="About CYOA Bot\nUsage: `>about`")
    embed.add_field(name="Help", value="List of available commands\nUsage: `>help`")
    embed.add_field(name="Adventures", value="Display list of available adventures to play\nUsage: `>adventures`", inline=False)
    embed.add_field(name="Add Adventure", value='Add an adventure to the list of available ones with its gsheet ID.\nNote: Make sure to share the sheet with the bot- `discord-cyoa-bot@discord-cyoa-bot.iam.gserviceaccount.com`\n\nUsage: `>add "name-of-adv" "gsheet-id"`\nExample: `>add "The Wyrldrift" "1_ykm2JOQKqlWE9d_VUdWY1YApH0DfzVDQDbM__L4VtI"`', inline=False)
    embed.add_field(name="Remove Adventure", value="Remove an adventure from the list\nUsage: `>remove 1`, `>remove 2`, etc.", inline=False)
    embed.add_field(name="Start Adventure", value="Pick and start an adventure\nUsage: `>start 1`, `>start 2`, etc.", inline=False)
    embed.add_field(name="Stop Adventure", value="Stop the currently running adventure\nUsage: `>stop`", inline=False)
    await ctx.send(embed=embed)
    print(f'">help" command embed sent.')

client.run(TOKEN)

