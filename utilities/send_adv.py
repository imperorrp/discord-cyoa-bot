#cyoa bot adventure+button embed sender

import discord
from discord import Button, ButtonStyle

async def button_sender(ctx, advname, page, msgid = 0):
    #if msgid = 0, send new message (for 'start'ing an adv). Else edit existing embed.
    content = page[1].split("@img")[0]
    image = page[1].split("@img")[1]
    options = page[2:]
    print(options)
    choice_num = len(options)
    embed=discord.Embed(title=advname, description=content)
    embed.set_image(url=image)
    if choice_num==1:
        label1 = options[0].split("@")[0]
        if msgid==0:
            msg = await ctx.send(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey)]])
        else:
            #msg = await ctx.fetch_message(msgid)
            await ctx.edit(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey)]])
    if choice_num==2:
        label1 = options[0].split("@")[0]
        label2 = options[1].split("@")[0]
        if msgid==0:
            msg = await ctx.send(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey)]])
        else:
            await ctx.edit(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey)]])
    if choice_num==3:
        label1 = options[0].split("@")[0]
        label2 = options[1].split("@")[0]
        label3 = options[2].split("@")[0]
        if msgid==0:
            msg = await ctx.send(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey),
                            Button(label=label3,
                                    custom_id="option_3",
                                    style=ButtonStyle.grey)]])
        else:
            await ctx.edit(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey),
                            Button(label=label3,
                                    custom_id="option_3",
                                    style=ButtonStyle.grey)]])
    if choice_num==4:
        label1 = options[0].split("@")[0]
        label2 = options[1].split("@")[0]
        label3 = options[2].split("@")[0]
        label4 = options[3].split("@")[0]
        if msgid==0:
            msg = await ctx.send(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey),
                            Button(label=label3,
                                    custom_id="option_3",
                                    style=ButtonStyle.grey),
                            Button(label=label4,
                                    custom_id="option_4",
                                    style=ButtonStyle.grey)]])
        else:
            msg = await ctx.edit(embed=embed, components=[[
                            Button(label=label1,
                                    custom_id="option_1",
                                    style=ButtonStyle.grey),
                            Button(label=label2,
                                    custom_id="option_2",
                                    style=ButtonStyle.grey),
                            Button(label=label3,
                                    custom_id="option_3",
                                    style=ButtonStyle.grey),
                            Button(label=label4,
                                    custom_id="option_4",
                                    style=ButtonStyle.grey)]])
    print(f'returning message from button_sender()')
    return msg