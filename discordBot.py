import os
import discord
import time
import datetime


def getNumberFromEnd(string):
    ''' Returns the relevant number as a string from the given string.

        Returns an empty string if no number is found.
    '''
    number = ""

    # Search for characters matching an ascii numeral.
    # Done in reverse as we want the last number in the string.
    for n in range(string):
        character = string[-(n+1)]
        if 47 < ord(character) < 58:
            number += character


def getNumberFromEndLocation(string):
    ''' Returns location of the relevant number as an integer.

        Returns -1 if no number is found.
    '''
    index = -1

    # Search for characters matching an ascii numeral.
    streak = 0
    for n, character in enumerate(string):
        # reset the streak if the last character was not a number.
        if 47 < ord(character) < 58 and (48 > ord(string[n-1]) or ord(string[n-1]) > 57):
            streak = 0
            index = n
        elif 47 < ord(character) < 58:
            streak += 1
            index = n

    return index - streak


def numberPrecedes(text):
    '''Returns the number if argument contains a number preceding the last word, None otherwise.

    Examples:
    * "The quick brown 5 fox" : 5
    * "The quick 100 brown fox" : None
    * "The quick brown fox" : None
    '''

    possibleNumber = text.split()[-2]

    for character in possibleNumber:
        if 47 > ord(character) or ord(character) > 58:
            return None
        
    return possibleNumber


def generateText(text):
    #isolatedText = text[getNumberFromEndLocation(text):]
    #return f"ME WAITING FOR BACS \"{isolatedText.upper()}\""
    
    # Get last two words, and make them upper case.
    addText = " ".join(text.split()[-2:]).upper()
    return f"ME WAITING FOR BACS \"{addText}\""


def messageTerm(message):
    '''Checks if message ends with a term in the dictionary, and returns that term if so.
    '''
    for term in dictionary:
        # TODO  Should test per word, not per character, maybe convert message to list (split) upon receival
        if message.endswith(term) and numberPrecedes(message):
            return term
    
    return None


class MyClient(discord.Client):
    messageChannel = None
    messageTime = -1
    timeScale = 0
    timeUnit = 0

    def resetValues(self):
        self.messageChannel = None
        self.messageTime = -1
        self.timeScale = 0
        self.timeUnit = 0

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}({message.author.id}): {message.content}')

        currentMessageTerm = messageTerm(message.content)
        if (message.author.id == userId or message.guild.id == server) and currentMessageTerm and len(message.content.split()) >= 2:
            self.messageChannel = message.channel
            self.timeScale = dictionary[currentMessageTerm]
            self.timeUnit = int(message.content.split()[-2])
            self.messageTime = time.time()

            os.system(f"echo {generateText(message.content)} | createImage.bat")
            await message.channel.send(file=discord.File("image.jpg"))

            return
        
    async def on_voice_state_update(self, member, before, after):
        now = time.time()
        if (member.id == userId or (member.guild.id == server and member != client.user)) and before.channel == None and self.messageTime != -1 and now < (self.messageTime + self.timeUnit * self.timeScale):
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


if __name__ == "__main__":

    dictionary = {}
    with open("dictionary.txt") as f:
        for line in f:
            lineSplit = line.split()
            dictionary[lineSplit[0]] = int(lineSplit[1])


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


    # with open("proud.opus", "rb") as f:
    #     audioBytes = f.read()


    print(f"token = {token}\n userId = {userId}\n server = {server}\n")

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents, activity=discord.Game(name="v2.0"))
    client.run(token)