from config import *
from pokes import pokemon as names
import datetime
import time
from token_ import *
lastpoke = ""
approved_channels = [
    1174005255189569587,
#    1085999031047704658
]
approved_users = open("users.txt", "r").read().split("\n") if os.path.exists("users.txt") else gen_app_users()
pokemon_have = {}
cheating=True
amount_have=0
@client.event
async def on_message(ctx):
    global lastmessage, lastpoke, pokemon_have,cheating,amount_have
    if not ctx.channel.id in approved_channels:
        return
    print(ctx.content)
    if True:  # not ctx.author == client.user:
        if not ctx.author.id in [716390085896962058, client.user.id]:
            return
        if ctx.embeds:
            if "your pokémon" in ctx.embeds[0].title.lower():
                # determine pokemon on page
                cheating=False
                description = (ctx.embeds[0].description.split("\n"))
                for item in description:
                    split = item.split("`")[2].split(" ")[1].split("**")[0]
                    poke_index = item.split("`")[1]
                    if split in pokemon_have.keys():
                        pokemon_have.update({split: [pokemon_have[split][0] + 1,pokemon_have[split][1]+[poke_index]]})
                    else:
                        pokemon_have.update({split: [1,[poke_index]]})
                # determine page number, and number of pages
                print(ctx.embeds[0].footer.text)
                page_count = int(ctx.embeds[0].footer.text.split(
                    " ")[5][:-1])/20
                page = int(ctx.embeds[0].footer.text.split(
                    " ")[2].split("–")[1])//20
                to = int(ctx.embeds[0].footer.text.split(
                    " ")[2].split("–")[1])
                have = int(ctx.embeds[0].footer.text.split(
                    " ")[5][:-1])
                amount_have=have
                print(page_count//1,page, page>=page_count//1)
                secs=(page_count*5-page*5)
                print(f"time to completion: {page_count-page} pages & {secs} seconds ({secs//60//60} hours {secs//60} minutes)")
                if int(str(page_count).split(".")[1]) > 0:
                    page_count = int(str(page_count).split(".")[0])+1
                print(pokemon_have)
                if to == have:
                    cheating=True
                    return
                sleep = 5
                print(f"sleeping for {sleep} seconds")
                time.sleep(sleep)
                await ctx.channel.send(f"<@716390085896962058> p {page+1}")
                return
            if not "wild" in ctx.embeds[0].title.lower():
                return
            await ctx.channel.send(f"<@716390085896962058> h")
        if "Congratulations" in ctx.content:
            await ctx.channel.send(":3")
            amount_have+=1
            split = ctx.content.split(" ")[7][:-1]
            if split in pokemon_have.keys():
                pokemon_have.update({split: [pokemon_have[split][0] + 1,[amount_have]]})
            else:
                pokemon_have.update({split: [1,[amount_have]]})
            print(pokemon_have[split])
        elif "That is the wrong pokémon!" in ctx.content:
            await ctx.channel.send(f"<@716390085896962058> h")
        elif 'The pokémon is' in ctx.content and cheating:
            poke = ctx.content.split(' ')[3:]
            if len(poke) > 1:
                poke = f"{poke[0]} {poke[1][:-1]}".replace("\\", "")
            else:
                poke = poke[0].replace("\\", "")[:-1]
            lastpoke = poke
            poses = []
            bestcandidate = ""
            print(poke)
            for i, char in enumerate(poke):
                if not char in [r"\\", "_"]:
                    poses.append({str(i): char})
            print(poses)
            for pokemon in names:
                if len(pokemon) == len(poke):
                    matches = 0
                    for pos in poses:
                        for key in pos:
                            if pokemon[int(key)] == pos[key]:
                                matches += 1
                    if matches >= len(poses):
                        bestcandidate = pokemon
            print(bestcandidate)
            await ctx.channel.send(f"<@716390085896962058> c {bestcandidate}")
        elif "#!pokesearch" in ctx.content and ctx.author.id == client.user.id:
            cmd, poke = ctx.content.split(" ")
            message=""
            for pokemon in names:
                if poke.lower() in pokemon.lower():
                    message += f"{pokemon}\n"  
            if message=="":
                message=f"No pokemon found with the search term *{poke}\*"  
            await ctx.channel.send(message)
        #elif "#!libsearch" in ctx.content and ctx.author.id in approved_users:   
client.run(TOKEN)
