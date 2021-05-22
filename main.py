import discord
from discord.ext import commands
import requests  # uncomment only in repl
import lxml  # uncomment only in repl
# from discord.ext.commands import Bot
# import kissmanga
# from manganelo import (MangaInfo, SearchManga)
import manganelo
import MangaHub
import kissmanga
import fanfox
from keep_alive import keep_alive
# manganelo==1.5.1


client = discord.Client()
cli = commands.Bot(command_prefix="+")
start_running = False


@client.event
async def on_ready():
    print(f'logged in as user {client.user}')


@client.event
async def on_message(own):
    global start_running

    # messages from bot will be Ignored
    msgAuth = own.author
    if own.author == client.user:
        return

    # part MAIN (part - 1) of message to initiate the conversation with bot :: will include the name of the manga
    if own.content.startswith('!shido> '):  # take the content : Manga Name
        # print("session started...")
        if not start_running:
            start_running = True

            if own.content == "!restart shido":
                start_running = False
                return await own.channel.send('```restarting session...```')

            A = own.content
            searchStr = A[8:]  # extract only the manga name
            search = manganelo.SearchManga(searchStr, threaded=False)  # search in Manganelo for correct name / options
            results = list(search.results())  # collect the results

            if len(results) == 0:  # if 0 results return
                await own.channel.send(" ```No results found with the name.```")
                start_running = False
                return await own.channel.send('```restarting session...```')

            count = 1  # if at least one result Proceed
            returnTxt = '```'  # designing the content inside
            for i in results:
                returnTxt += str(count) + "    " + i.title + "\n"  # result 1
                count += 1
            returnTxt += "```"

            embed = discord.Embed(  # making an EMBED object for the response
                title="MANGA",
                description=returnTxt,
                color=0xFF5733)
            embed.add_field(name="Selection", value="Type the Number corresponding to your selection.",
                            inline=False)

            await own.channel.send(embed=embed)  # sending the EMBED object in the chat

            start_running = False
            # will return list of mangas identified

        # inside part MAIN (part - 2): the argument used to denote the manga in the above list
        msg = await client.wait_for('message', check=lambda message: message.author == msgAuth)
        # wait for a command not from Bot

        if not start_running:
            start_running = True

            if msg.content == "!restart shido":
                start_running = False
                return await own.channel.send('```restarting session...```')

            if not msg.content.isnumeric():  # input must be number
                await own.channel.send('```Please enter Numeric response.\n```')  # if not return
                start_running = False
                return await own.channel.send('```restarting session...```')

            await own.channel.send('Give me a moment. Let me search the web for you ..')  # send msg to wait a little
            in1 = int(msg.content)  # Manga choose Input from command
            try:
                MangaName = results[in1 - 1].title   # select the name you were trying to search
                #embed = discord.Embed(  # making an EMBED object for the response
                #    color=0xFF5733)
                #embed.add_field(name="1  -  MangaNelo",
                #                value="Get access to large database of"
                #                      " manganelo with near instantaneous updates.",
                #                inline=False)
                #await own.channel.send(embed=embed)
                info = results[in1 - 1]
            except IndexError:  # if response was out of box : Exit session
                # print("unexpected input observed")
                await own.channel.send('```Please enter a Response within the given Options.\n```')
                start_running = False
                return await own.channel.send('```restarting session...```')

            # * once found search in other servers
            try:
                # raise IndexError
                #request = requests.get('https://1stkissmanga.com/')
                #if request.status_code != 200:
                #    raise IndexError
                info2 = kissmanga.SearchManga(MangaName, threaded=True)  # search for it in KissManga
                results = list(info2.results())
                info2 = [i for i in results if MangaName.lower() == i.title.lower()]   # find it from the results list
                info2 = info2[0]
                #embed = discord.Embed(  # making an EMBED object for the response
                #    color=0xFF5733)
                #embed.add_field(name="2  -  KissManga",
                #                value="Read manga from 1stkissmanga.com.",
                #                inline=False)
                #await own.channel.send(embed=embed)
            except IndexError:
                info2 = None  # if not found say it is empty
            try:
                # raise IndexError
                #request = requests.get('https://fanfox.net/')
                #if request.status_code != 200:
                #    raise IndexError
                info3 = fanfox.SearchManga(MangaName, threaded=True)  # search for it in FanFox
                results = list(info3.results())
                info3 = [i for i in results if MangaName.lower() == i.title.lower()]   # find it from the results list
                info3 = info3[0]
                #embed = discord.Embed(  # making an EMBED object for the response
                #    color=0xFF5733)
                #embed.add_field(name="3  -  FanFox",
                #                value="Read from one of the oldest Manga"
                #                      " Reader in existence ",
                #                inline=False)
                #await own.channel.send(embed=embed)
            except IndexError:
                info3 = None  # if not found say it is empty
            try:
                # raise IndexError
                #request = requests.get('https://mangahub.io/')
                #if request.status_code != 200:
                #    raise IndexError
                info4 = MangaHub.SearchManga(MangaName, threaded=True)  # search for it in MangaHub
                results = list(info4.results())
                info4 = [i for i in results if MangaName.lower() == i.title.lower()]   # find it from the results list
                info4 = info4[0]
                #embed = discord.Embed(  # making an EMBED object for the response
                #    color=0xFF5733)
                #embed.add_field(name="4  -  MangaHub",
                #                value="Manhuas are updated fastest in MangaHub",
                #                inline=False)
                #await own.channel.send(embed=embed)
            except IndexError:
                info4 = None  # if not found say it is empty
            # print("info :: ", info)
            # print("info2 :: ", info2)
            # print("info3 :: ", info3)
            # print("info4 :: ", info4)
            # embed = discord.Embed(  # making an EMBED object for the response
            #    title="Selection",
            #    description="Type the Number corresponding to your selection.",
            #    color=0xFF5733)
            # await own.channel.send(embed=embed)
            listofservers = ''  # initiate an empty list to serve allowed responses
            embed = discord.Embed(  # making an EMBED object for the Server List
                title="Select Server",
                color=0xFF5733)
            embed.add_field(name="1  -  MangaNelo",  # add a field for MangaNelo
                            value="Get access to large database of"
                                  " manganelo with near instantaneous updates.",
                            inline=False)
            listofservers += '1'
            thumbnail = manganelo.MangaInfo(info.url).results().icon
            embed.set_thumbnail(url=thumbnail)
            if info2:
                embed.add_field(name="2  -  KissManga", value="Read manga from 1stkissmanga.com.",
                                inline=False)   # add a field for KissManga if Exists
                listofservers += '2'
            if info3:
                embed.add_field(name="3  -  FanFox", value="Read from one of the oldest Manga"
                                                           " Reader in existence ",
                                inline=False)   # add a field for FanFox if Exists
                listofservers += '3'
            if info4:
                embed.add_field(name="4  -  MangaHub", value="Manhuas are updated fastest in MangaHub",
                                inline=False)   # add a field for MangaHub if Exists
                listofservers += '4'
            embed.add_field(name="Selection", value="Type the Number corresponding to your selection.",
                            inline=False)  # add a field to indicate selection
            await own.channel.send(embed=embed)  # send the created embed
            start_running = False
            # will return Manga Info with chapter list

        msg1 = await client.wait_for('message', check=lambda message: message.author == msgAuth)  # wait for cmd
        if not start_running:
            start_running = True

            if msg1.content == "!restart shido":
                start_running = False
                return await own.channel.send('```restarting session...```')

            if not msg1.content.isnumeric():  # if cmd not a number Exit session
                await own.channel.send('```Please enter Numeric response.\n```')
                start_running = False
                return await own.channel.send('```restarting session...```')

            serverChoice = msg1.content  # take the server choice, if not in active servers .Exit session
            if serverChoice not in listofservers:
                await own.channel.send('```Please enter a Response within the given Options.\n```')
                start_running = False
                return await own.channel.send('```restarting session...```')

            if serverChoice == '1':
                server = manganelo.MangaInfo(info.url)
                infoSelect = info
                serverName = "MangaNelo"
            elif serverChoice == '2':
                server = kissmanga.MangaInfo(info2.url)
                infoSelect = info2
                serverName = "KissManga"
            elif serverChoice == '3':
                server = fanfox.MangaInfo(info3.url)
                infoSelect = info3
                serverName = "FanFox"
            elif serverChoice == '4':
                server = MangaHub.MangaInfo(info4.url)
                infoSelect = info4
                serverName = "MangaHub"
            # server is a variable chosen according to our option
            chapter_list = server.results().chapters  # get list of chapters from the chosen server

            if len(chapter_list) == 0:  # if chapter is empty in fanfox .. it is protected
                Fmessage = f'Shido :sorry to break it to you, But {serverName} has decided to tag this content as mature... \n' \
                          f'So i cannot access it directly, but you can in their website... click [here]({infoSelect.url})' \
                          f' to open in browser'
                embed = discord.Embed(  # making an EMBED object for chapter list
                    title="FanFox",
                    description=Fmessage,
                    color=0xFF5733)
                await own.channel.send(embed=embed)
                start_running = False
                return await own.channel.send('```exiting session...```')

            lastNum = str(chapter_list[-1].num)  # get the last chapter
            chapters = f"```In this server '{MangaName}' has {lastNum} chapters,\n" \
                       f"type a number from index - 1 to {lastNum} to select a chapter...```"  # create response
            embed = discord.Embed(  # making an EMBED object for chapter list
                title="MANGA",
                description=chapters,
                color=0xFF5733)
            embed.add_field(name="Tip", value="To select multiple Chapters, "
                                              "simply type the range of chapters you want to watch!"
                                              " e.g. 4-10", inline=False)  # add a field for the tip
            await own.channel.send(embed=embed)  # send embed
            start_running = False

        # inside part MAIN (part - 3): the argument used to denote the chapter or list of chapters denoted
        msg2 = await client.wait_for('message', check=lambda message: message.author == msgAuth)
        # wait for user message...
        if not start_running:
            start_running = True

            if msg2.content == "!restart shido":
                start_running = False
                return await own.channel.send('```restarting session...```')

            chapter_sChose = msg2.content
            print(chapter_sChose)
            container = "0123456789- "  # set of allowed characters in the cmd
            if any((c not in container) for c in chapter_sChose):  # if not in allowed characters Exit Session
                await own.channel.send('```Please enter Numeric response.\n```')
                start_running = False
                return await own.channel.send('```restarting session...```')

            try:
                if "-" not in chapter_sChose:  # if it does not contain "-" then it's request for single chapter
                    chap = int(chapter_sChose)  # find the chapter No
                    if chap > int(lastNum) or chap < 1:  # verify Chapter No : otherwise Exit session
                        raise IndexError
                    temp = server.results().chapters[chap - 1]  # if valid Start making embed
                    embed = discord.Embed(  # Embed Object for main body
                        title=f"{serverName}",
                        description=f"` Shido ` I found a chapter 👍 !",
                        color=0xFF5733)
                    embed.add_field(name="Ready to Read!",  # add field for chapter
                                    value=f"\n {MangaName} = {temp.title}\n read"
                                          f"  here at [{serverName}]({temp.url}).",
                                    inline=False)
                    embed.set_thumbnail(url=thumbnail)  # give it a thumbnail
                    await own.channel.send(embed=embed)  # send it to the channel
                    # print(temp)

                elif "-" in chapter_sChose:  # if "-" present, assume it's request for list
                    getRange = chapter_sChose.replace(" ", "")  # remove whitespaces
                    getRange = getRange.split("-")  # split it into a list of 2 elements
                    if len(getRange) == 2 and getRange[0].isdecimal() and getRange[1].isdecimal():
                        # if the result is as expected proceed
                        lower = min(getRange)
                        higher = max(getRange)

                        if int(higher) > int(lastNum) or int(lower) < 1:
                            raise IndexError
                    else:
                        # if the list split is invalid format Exit session
                        raise IndexError

                    # same as above but now looping over a set of chapters
                    for i in range(int(lower), int(higher) + 1):
                        temp = server.results().chapters[i - 1]
                        embed = discord.Embed(
                            title=f"{serverName}",
                            description=f"` Shido ` I found a chapter 👍 !",
                            color=0xFF5733)
                        embed.add_field(name="Ready to Read!",
                                        value=f"\n`[{i}]` {MangaName} = {temp.title}\n read"
                                        f"  here at [{serverName}]({temp.url}).",
                                        inline=False)
                        embed.set_thumbnail(url=thumbnail)
                        await own.channel.send(embed=embed)
                        #  print(server.results().chapters[i - 1])
                await own.channel.send("Shido : That's it from me .. plz enjoy the stay... 😃")  # final message

                #await own.channel.send("waiting for message 2..")
                #embed = discord.Embed(
                #    title="Sample Embed",
                #    url="https://realdrewdata.medium.com/",
                #    description="This is an embed that will show how to build an"
                #                " embed and the different components reading " + msg2.content,
                #    color=0xFF5733)
                #await own.channel.send(embed=embed)

            except IndexError:
                await own.channel.send('```Please enter a valid response in given range.\nrestarting session...```')
                start_running = False
                return  # print("exception occurred")
            start_running = False
            # will return one (or) list of embeds of chapters from various sources

    return
print("entered script")
keep_alive()

token = open("TOKEN", "r")
token_str = token.read()
token.close()
client.run(token_str)
