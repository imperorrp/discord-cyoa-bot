#cyoa bot adventures management

import discord 
import json
import gspread


gc = gspread.service_account(filename='discord-cyoa-bot-a171fc3ed3d6.json')
print('-utilities/manage_adv.py Gspread API authorized')

#defining 'adventure' class and related functions->
class Adventure:
    def __init__(self, msgid, advnum, guild:discord.guild):
        print(f'adventure __init__: setting guild, adv num, first page')
        self.guild = guild #server in which this adventure instance is running
        self._advnum = advnum #adventure number in adventures.json
        self._currentpage = 1 #default start page 
        self._messageid = msgid #message id of the embed adventure ongoing 
        f3 = open('adventures.json',)
        advs = json.load(f3)
        list_advs = advs["list_of_adventures"]
        f3.close()
        self._advname = list_advs[advnum-1]["name"] #name of the adventure corresponding to advnum in adventures.json
        print(f'guild + _advnum + _currentpage + _messageid +_advname set.\n')
    
    @property
    def currentpage(self):
        return self._currentpage

    def set_page(self, x: int):
        self._currentpage = x
        return self._currentpage

    @property
    def advnum(self):
        return self._advnum

    @property 
    def messageid(self):
        return self._messageid

    @property 
    def advname(self):
        return self._advname


advs = []
#create new adventure instance if non-existent, or find an existing instance->
def get_adventure(msgid, advnum, obj:discord.guild):
    #if isinstance(obj, discord.Guild):
    print(f'get_adventure() called. Current active adventure instances = "{advs}"\n')
    for p in advs:
        if p.messageid == msgid:
            return p
    advs.append(Adventure(msgid, advnum, obj))
    return get_adventure(msgid, advnum, obj)

#retrieve a page (content + options)
def get_page(advnum, pagenum):
    print(f'Getting page "{pagenum}" for adventure "{advnum}"...')
    f3 = open('adventures.json',)
    advs = json.load(f3)
    list_advs = advs["list_of_adventures"]
    key = list_advs[advnum-1]["sheetid"]
    sht1 = gc.open_by_key(key)
    worksheet = sht1.get_worksheet(0)
    page = worksheet.row_values(2+int(pagenum)) #corresponds to row pagenum+2 of g-sheet
    print(f'retrieved page = {page}')
    return page

#utility functions-> (adding adventure, removing adventure, etc.)
def add_adventure(name, gsheet_id):
    #attempt to open gsheet_id (possible if shared with bot email or public sheet)
    gsheet_id = str(gsheet_id)
    try: 
        sheet = gc.open_by_key(gsheet_id)
        print(sheet.sheet1)
        worksheet = sheet.get_worksheet(0)
        values_list = worksheet.row_values(1)
        description = values_list[1]
        print(f'Description of adventure:\n{description}\n-----------\n')
        f2 = open('adventures.json',)
        adv2 = json.load(f2)
        f2.close()
        #list_adv2 = adv2["list_of_adventures"]
        new_adv_dict = {"name" : str(name), "sheetid" : str(gsheet_id), "description" : str(description)}
        #list_adv2.append(new_adv_dict)
        adv2["list_of_adventures"].append(new_adv_dict)
        #adv2["list_of_adventures"] = list_adv2
        print(adv2)
        f2 = open('adventures.json','w')
        json.dump(adv2, f2, indent=2)
        f2.close()
        print(f'Adventure added')
        return 1 #successfull
    except Exception as e:
        print(f"Exception:\n{e}")
        return 0 #unsuccessful

def remove_adventure(adv_num):
    try:  
        f2 = open('adventures.json',)
        adv2 = json.load(f2)
        f2.close()
        list_adv2 = adv2["list_of_adventures"] 
        list_adv2.pop(adv_num-1)
        adv2["list_of_adventures"] = list_adv2
        f2 = open('adventures.json','w')
        json.dump(adv2, f2, indent=2)
        f2.close()
        print(f'Adventure removed')
        return 1 #successfull
    except Exception as e:
        print(f"Exception:\n{e}")
        return 0 #unsuccessful

