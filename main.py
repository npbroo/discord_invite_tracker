import os, discord
from discord.ext import commands
from quart import Quart, render_template, request
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
    help1 = "to get all invites for the server go to: /get-all-invites</br>"
    help2 = "to get invite counts for each link go to: /get-invite-counts</br>"
    help3 = "to check a specific invite link or set of invite links go to: /check-invites</br>"
    return help1 + help2 + help3

@app.route("/check-invites")
async def checkInvites():
    return await render_template("pasteInviteLinks.html")

@app.route('/results/', methods = ['POST'])
async def data():
    #get the form 
    form_data = await request.form
    links = form_data['discord links'].split('\r\n')
    print(links)

    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    inviteList = ""

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
        print(invite.inviter, "= ", invite.url, " ==> ", invite.uses, "uses")
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
        print(invite.inviter, "= ", invite.url)
    return inviteList

@app.route("/get-invite-counts")
async def getInviteCounts():
    guild = await bot.fetch_guild('882317671457243196')
    print(guild)
    invites = await guild.invites()
    inviteList = "<table><tr><th>Invite Link</th><th>Uses</th></tr>"
    for invite in invites:
        inviteList += "<tr><th>" + invite.url + "</th>"
        inviteList += "<th>" + str(invite.uses) + "</th></tr>"
        #inviteList += invite.url + " ==> " + str(invite.uses) + "</br>"
        print(invite.inviter, " ==> ", invite.url, " ==> ", invite.uses, "uses")
    inviteList += "</table>"
    return inviteList

bot.loop.create_task(app.run_task())

bot.run(TOKEN)