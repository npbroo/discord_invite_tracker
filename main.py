import os, discord
from discord.ext import commands
from quart import Quart, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

app = Quart(__name__) 

@app.route("/")
async def home():
    return await render_template("index.html")

@app.route("/check-invites")
async def checkInvites():
    return await render_template("pasteInviteLinks.html")

@app.route('/results/', methods = ['POST'])
async def data():
    #get the form 
    form_data = await request.form
    links = form_data['discord links'].split('\r\n')

    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()

    distinctInvites = []
    for invite in invites:
        url = invite.url
        for link in links:
            if (url == link):
                distinctInvites.append(invite)
                break

    inviteList = ""
    totalInvites = 0
    for invite in distinctInvites:
        inviteList += invite.url + "  ==>  " + str(invite.uses) + "</br>"
        totalInvites += invite.uses
        #print(invite.inviter, "= ", invite.url, " ==> ", invite.uses, "uses")
    inviteList += "</br>Total invites for this set: " + str(totalInvites) + "</br>"

    return inviteList

@app.route("/get-all-invites")
async def getAllInvites():
    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    inviteList = ""
    for invite in invites:
        inviteList += invite.url + "</br>"
        #print(invite.inviter, "= ", invite.url)
    return inviteList

@app.route("/get-invite-stats")
async def getInviteStats():
    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    inviteList = "<table><tr><th>Invite Link</th><th>Uses</th><th>Inviter</th></tr>"
    totalInvites = 0
    for invite in invites:
        inviteList += "<tr><td>" + invite.url + "</td>"
        inviteList += "<td>" + str(invite.uses) + "</td>"
        inviteList += "<td>" + str(invite.inviter) + "</td></tr>"
        totalInvites += invite.uses
        #inviteList += invite.url + " ==> " + str(invite.uses) + "</br>"
        #print(invite.inviter, " ==> ", invite.url, " ==> ", invite.uses, "uses")
    inviteList += "</table></br>"
    inviteList += "</br>Total invites: " + str(totalInvites) + "</br>"
    return inviteList

@app.route("/clear-unused-invites-0-1")
async def clearUnusedInvites():
    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    deleted_invites = 0
    render_page = "Deleted Invites: </br>"
    for invite in invites:
        # whitelisted invite usernames (dont delete invites from these users)
        if str(invite.inviter) == "Skipper#7343" or str(invite.inviter) == "Finn  🏆#8141" or str(invite.inviter) == "npbroo#5486" or str(invite.inviter) == "Hopper#3211" or str(invite.inviter) == "Aura#4527" or str(invite.inviter) == "Scott#2054" or str(invite.inviter) == "canopyman#4147" or str(invite.inviter) == "Devin#1667":
            render_page += "</br>Found invite by: " + str(invite.inviter) + " | This user is whitelisted (will not delete invite)"
            continue
        if invite.uses == 0 or invite.uses == 1:
            print(invite)
            deleted_invites += 1
            await invite.delete(reason="Too many invites on Discord server")
            render_page += "</br>Deleted invite: " + str(invite.url) + " by " + str(invite.inviter) + " | total uses: " + str(invite.uses)
  
    render_page += "</br>Deleted " + str(deleted_invites) + " invites"
    return render_page

@app.route("/clear-unused-invites-2-3")
async def clearUnusedInvites2():
    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    deleted_invites = 0
    render_page = "Deleted Invites: </br>"
    for invite in invites:
        # whitelisted invite usernames (dont delete invites from these users)
        if str(invite.inviter) == "Skipper#7343" or str(invite.inviter) == "Finn  🏆#8141" or str(invite.inviter) == "npbroo#5486" or str(invite.inviter) == "Hopper#3211" or str(invite.inviter) == "Aura#4527" or str(invite.inviter) == "Scott#2054" or str(invite.inviter) == "canopyman#4147" or str(invite.inviter) == "Devin#1667":
            render_page += "</br>Found invite by: " + str(invite.inviter) + " | This user is whitelisted (will not delete invite)"
            continue
        if invite.uses == 2 or invite.uses == 3:
            print(invite)
            deleted_invites += 1
            await invite.delete(reason="Too many invites on Discord server")
            render_page += "</br>Deleted invite: " + str(invite.url) + " by " + str(invite.inviter) + " | total uses: " + str(invite.uses)
  
    render_page += "</br>Deleted " + str(deleted_invites) + " invites"
    return render_page

PORT = int(os.environ.get("PORT", 5000))
bot.loop.create_task(app.run_task(host='0.0.0.0', port=PORT))
#bot.loop.create_task(app.run_task())

bot.run(TOKEN)