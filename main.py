import discord
import requests
import json
import os
from datetime import datetime
from dateutil import tz
import pytz
from keep_alive import keep_alive
client=discord.Client()
API_KEY=r""
def utc_to_ist(dt_str):
    format="%Y-%m-%d %H:%M:%S"
    dt_utc=datetime.strptime(dt_str, format)
    dt_utc=dt_utc.replace(tzinfo=pytz.UTC)
    local_zone=tz.gettz("Asia/Kolkata") # For Replit
    dt_local=dt_utc.astimezone(local_zone)
    local_time_str=dt_local.strftime(format+" "+"%p")
    return local_time_str
def player_stats(name,platform):
    embed=discord.Embed(title="Player Stats")
    r=requests.get(f"https://api.mozambiquehe.re/bridge?auth={API_KEY}&player={name}&platform={platform}").text
    parsed=json.loads(r)
    try:
        _global=parsed["global"]
    except:
        embed=discord.Embed(title="Couldn't Find A Player With Provided Name/Platform",description="Check If Your **Origin** Username Is Correct Or Maybe The Platform You Entered Was Wrong. Enter A Platform Like This :")
        embed.add_field(name="For PC",value="-playerstats 0xN1nja **PC**",inline=False)
        embed.add_field(name="For XBOX",value="-playerstats 0xN1nja **X1**",inline=False)
        embed.add_field(name="For Play Station",value="-playerstats 0xN1nja **PS4**",inline=False)
        return embed
    else:
        # Main
        embed.add_field(name="In Game Name",value=_global["name"],inline=True)
        embed.add_field(name="Level",value=_global["level"],inline=True)
        embed.add_field(name="UID",value=_global["uid"],inline=True)
        embed.add_field(name="XP Needed To Level Up",value=_global["internalUpdateCount"],inline=True)
        embed.add_field(name="Is Banned",value=_global["bans"]["isActive"],inline=True)
        embed.add_field(name="Remaining Penalty Cooldown",value=str(_global["bans"]["remainingSeconds"])+" "+"Seconds",inline=True)
        embed.add_field(name="Last Ban Reason",value=_global["bans"]["last_banReason"],inline=True)
        embed.set_thumbnail(url=_global["rank"]["rankImg"])
        # Lobby Status
        embed.add_field(name="Lobby State",value=parsed["realtime"]["lobbyState"])
        embed.add_field(name="Is In A Game",value=parsed["realtime"]["isInGame"])
        embed.add_field(name="Party Full",value=parsed["realtime"]["partyFull"])
        embed.add_field(name="Selected Legend",value=parsed["realtime"]["selectedLegend"])
        embed.add_field(name="Current State",value=parsed["realtime"]["currentStateAsText"])
        # Battle Pass
        embed.add_field(name="Battle Pass Level History",value=_global["battlepass"]["history"])
        # Badges
        embed.add_field(name="Badges",value=[i for i in [i["name"] for i in _global["badges"]]],inline=False)
        # Rank (Battle Royale)
        embed.add_field(name="Rank (Battle Royale)",value=_global["rank"]["rankName"])
        embed.add_field(name="RP",value=_global["rank"]["rankScore"])
        embed.add_field(name="Rank Div",value=_global["rank"]["rankDiv"])
        embed.add_field(name="Ranked Season",value=_global["rank"]["rankedSeason"],inline=False)
        # Rank (Arenas)
        embed.add_field(name="Rank (Arenas)",value=_global["arena"]["rankName"])
        embed.add_field(name="RP",value=_global["arena"]["rankScore"])
        embed.add_field(name="Rank Div",value=_global["arena"]["rankDiv"])
        embed.add_field(name="Ranked Season",value=_global["arena"]["rankedSeason"])
        return embed
def map_rotation_br():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["battle_royale"]
    embed=discord.Embed(title="Current Map On Rotation",description="Battle Royale")
    embed.add_field(name="Map Name",value=parsed["current"]["map"],inline=False)
    embed.set_image(url=parsed["current"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["current"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["current"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["current"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    embed.add_field(name="Remaining Minutes",value=parsed["current"]["remainingTimer"],inline=False)
    return embed
def map_rotation_arenas():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["arenas"]
    embed=discord.Embed(title="Current Map On Rotation",description="Arenas")
    embed.add_field(name="Map Name",value=parsed["current"]["map"],inline=False)
    embed.set_image(url=parsed["current"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["current"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["current"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["current"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    embed.add_field(name="Remaining Minutes",value=parsed["current"]["remainingTimer"],inline=False)
    return embed
def map_rotation_ranked_br():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["ranked"]
    embed=discord.Embed(title="Current Map On Rotation",description="Battle Royale Ranked")
    embed.add_field(name="Map Name",value=parsed["current"]["map"],inline=False)
    embed.set_image(url=parsed["current"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["current"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["current"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["current"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    embed.add_field(name="Remaining Minutes",value=parsed["current"]["remainingTimer"],inline=False)
    return embed
def map_rotation_ranked_arenas():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["arenasRanked"]
    embed=discord.Embed(title="Current Map On Rotation",description="Arenas Ranked")
    embed.add_field(name="Map Name",value=parsed["current"]["map"],inline=False)
    embed.set_image(url=parsed["current"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["current"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["current"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["current"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    embed.add_field(name="Remaining Minutes",value=parsed["current"]["remainingTimer"],inline=False)
    return embed
def nextmap_br():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["battle_royale"]
    embed=discord.Embed(title="Next Map On Rotation",description="Battle Royale")
    embed.add_field(name="Map Name",value=parsed["next"]["map"],inline=False)
    embed.set_image(url=parsed["next"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["next"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["next"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["next"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    return embed
def nextmap_arenas():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["arenas"]
    embed=discord.Embed(title="Next Map On Rotation",description="Arenas")
    embed.add_field(name="Map Name",value=parsed["next"]["map"],inline=False)
    embed.set_image(url=parsed["next"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["next"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["next"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["next"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    return embed
def nextmap_br_ranked():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["ranked"]
    embed=discord.Embed(title="Next Map On Rotation",description="Battle Royale Ranked")
    embed.add_field(name="Map Name",value=parsed["next"]["map"],inline=False)
    embed.set_image(url=parsed["next"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["next"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["next"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["next"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    return embed
def nextmap_arenas_ranked():
    r=requests.get(f"https://api.mozambiquehe.re/maprotation?version=2&auth={API_KEY}").text
    parsed=json.loads(r)["arenasRanked"]
    embed=discord.Embed(title="Next Map On Rotation",description="Arenas Ranked")
    embed.add_field(name="Map Name",value=parsed["next"]["map"],inline=False)
    embed.set_image(url=parsed["next"]["asset"])
    embed.add_field(name="Start",value=utc_to_ist(parsed["next"]["readableDate_start"]),inline=False)
    embed.add_field(name="Till",value=utc_to_ist(parsed["next"]["readableDate_end"]),inline=False)
    embed.add_field(name="Duration",value=str(parsed["next"]["DurationInMinutes"])+" "+"Minutes",inline=False)
    return embed
def help_menu():
    embed=discord.Embed(title="Help",description="Commands")
    embed.add_field(name="-playerstats",value="Returns Stats Of Provided Player Name",inline=False)
    embed.add_field(name="-maprotation br",value="Returns Current Map Rotation Of Battle Royale",inline=False)
    embed.add_field(name="-maprotation arenas",value="Returns Current Map Rotation Of Arenas",inline=False)
    embed.add_field(name="-maprotation br_ranked",value="Returns Current Map Rotation Of Ranked Battle Royale",inline=False)
    embed.add_field(name="-maprotation arenas_ranked",value="Returns Current Map Rotation Of Ranked Arenas",inline=False)
    embed.add_field(name="-nextmap br",value="Returns Next Map On Rotation (For Battle Royale)",inline=False)
    embed.add_field(name="-nextmap arenas",value="Returns Next Map On Rotation (For Arenas)",inline=False)
    embed.add_field(name="-nextmap br_ranked",value="Returns Next Map On Rotation (For Ranked Battle Royale)",inline=False)
    embed.add_field(name="-nextmap arenas_ranked",value="Returns Next Map On Rotation (For Ranked Arenas)",inline=False)
    return embed
@client.event
async def on_ready():
    print(f"Bot Has Successfully Logged In As {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='-help'))
@client.event
async def on_message(message):
    msg=message.content
    if msg.startswith("-help"):
        await message.channel.send(embed=help_menu())
    if msg.startswith("-playerstats"):
        which_player=msg.replace("-playerstats","").strip().split()
        try:
          __playername=which_player[0]
          __platform=which_player[1]
        except:
          embed=discord.Embed(title="Missing Parameter(s)",description="You Didn't Enter `Playername` Or `Platform` Correctly")
          embed.add_field(name="For Example If You're Using PC",value="-playerstats **0xN1nja PC**",inline=False)
          embed.add_field(name="For XBOX",value="-playerstats **0xN1nja X1**",inline=False)
          embed.add_field(name="For Play Station",value="-playerstats **0xN1nja PS4**",inline=False)
          await message.channel.send(embed=embed)
        else:
          await message.channel.send(embed=player_stats(__playername,__platform))
    if msg.startswith("-maprotation"):
        which_mode=msg.replace("-maprotation","").strip()
        if which_mode=="br":
            await message.channel.send(embed=map_rotation_br())
        elif which_mode=="arenas":
            await message.channel.send(embed=map_rotation_arenas())
        elif which_mode=="br_ranked":
            await message.channel.send(embed=map_rotation_ranked_br())
        elif which_mode=="arenas_ranked":
            await message.channel.send(embed=map_rotation_ranked_arenas())
    if msg.startswith("-nextmap"):
        which_mode=msg.replace("-nextmap","").strip()
        if which_mode=="br":
            await message.channel.send(embed=nextmap_br())
        elif which_mode=="arenas":
            await message.channel.send(embed=nextmap_arenas())
        elif which_mode=="br_ranked":
            await message.channel.send(embed=nextmap_br_ranked())
        elif which_mode=="arenas_ranked":
            await message.channel.send(embed=nextmap_arenas_ranked())
keep_alive()
client.run()