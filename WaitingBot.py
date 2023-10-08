import re
import discord
import time
import datetime
import os

def listFind(listToSearch, itemToFind):
    for index, item in enumerate(listToSearch):
        if item == itemToFind:
            return index
    return -1

def findTimeTerm(message):
    message = message.split()
    if len(message) < 2:
        return None

    for term, termUnit in dictionary.items():
        if (index := listFind(message, term)) >= 0:
            # "a minute" should be treated as "1 minute"
            if (messageUnits := message[index-1]) in ["a", "an"]:
                messageUnits = "1"
                # Make sure that what is in front of the term is a number
                if messageUnits.isnumeric():
                    return [messageUnits, term]
    return None

def generateText(stringList):
    return f"ME WAITING FOR BACS \"{' '.join(stringList).upper()}\""

class MyClient(discord.Client):
    messageChannel = None
    messageTime = -1
    termTimeUnits = 0
    messageTimeUnits = 0

    def resetValues(self):
        self.messageChannel = None
        self.messageTime = -1
        self.termTimeUnits = 0
        self.messageTimeUnits = 0

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if currentMessageUnits := findTimeTerm(message.content):
            print(f'Message from {message.author}({message.author.id}): {message.content}')

            if (message.author.id == userId or message.guild.id == server):
                self.messageChannel = message.channel
                self.messageTimeUnits = int(currentMessageUnits[0])
                self.termTimeUnits = int(dictionary[currentMessageUnits[1]])
                self.messageTime = time.time()

                os.system(f"echo {generateText(currentMessageUnits)} | createImage.bat")
                await message.channel.send(file=discord.File("image.jpg"))
        
    async def on_voice_state_update(self, member, before, after):
        now = time.time()

        # Debug values
        print(f"""Member: {member}
              Before: {before}
              After: {after}
              Guild: {member.guild.name} | {member.guild.id}
              """)

        if (member.id == userId or (member.guild.id == server and member != self.user)) and before.channel == None and self.messageTime != -1 and now < (self.messageTime + self.messageTimeUnits * self.termTimeUnits):
            if isinstance(self.messageChannel, discord.abc.GuildChannel):
                await self.messageChannel.send(content="HE ACTUALLY JOINED WHEN HE SAID HE WOULD!", file=discord.File("SpittingCerealGuy.png")) # pyright: ignore
                voice_client = await member.voice.channel.connect()
                audio = await discord.FFmpegOpusAudio.from_probe("proud.opus")
                voice_client.play(audio)
                date = datetime.datetime.now()
                print(date)
                second = (date.second+2)%60
                minute = (date.second+2)//60
                date = date.replace(second=second, minute=date.minute + minute)
                print(date)
                await discord.utils.sleep_until(date)
                await voice_client.disconnect()

                self.resetValues()

dictionary = {}
with open("dictionary.txt") as f:
    # ["min", "60"]
    for line in f.readlines():
        term = line.split()[:2]
        dictionary[term[0]] = term[1]

regex = re.compile("[^a-zA-Z0-9\s]") # pyright: ignore

if __name__ == "__main__":
    
    delimiter = " = "
    tokenString = "token" + delimiter
    userIdString = "id" + delimiter
    serverString = "server" + delimiter

    token = ""
    userId = 0
    server = 0
    with open("secrets.txt") as f:

        for line in f:

            if tokenString in line:
                token = line[len(tokenString):-1]
            elif userIdString in line:
                userId = int(line[len(userIdString):-1])
            elif serverString in line:
                server = int(line[len(serverString):-1])

    with open("messages.txt") as f:
        for message in f.readlines():
            message = regex.sub("", message)
            print(f"{message[:-1]} | {findTimeTerm(message)}")



    with open("proud.opus", "rb") as f:
        audioBytes = f.read()


    print(f"token = {token}\n userId = {userId}\n server = {server}\n")

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents, activity=discord.Game(name="v2.2"))
    client.run(token)
