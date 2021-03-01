import discord
from discord import file
from discord.ext import commands,menus
from jishaku.cog import Jishaku
from pretty_help import PrettyHelp, Navigation
from googleapiclient.discovery import build
import async_cse
import bs4
import requests
import aiohttp
import random
import jishaku
import asyncio
import json
from googletrans import Translator
import PyDictionary
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
translator = Translator(service_urls=['translate.googleapis.com'])
dictionary = PyDictionary.PyDictionary()

API = "AIzaSyDUW5x46SpqWVJTTnphKdP2_txtJwQBpCQ"
youtubeservice = build('youtube', version='v3', developerKey=API)
GOOGLE_API_KEY = "AIzaSyAfGRWztikfvzMEQ9sLQVkujcPHX19xVso"
engine = async_cse.Search(GOOGLE_API_KEY)

bot = commands.Bot(command_prefix="-")
class LolException(Exception):
    pass
class MyMenu(menus.Menu):
    def __init__(self, pages):
        super().__init__()
        self.pages:list = pages
        self.current_page:int = 0
    async def send_initial_message(self, ctx:commands.Context, channel:discord.TextChannel):
        return await channel.send(embed= self.pages[0].set_footer(text=f"Page={str(self.current_page+1)}/{str(len(self.pages))}"))
    async def change(self):
        embed:discord.Embed = self.pages[self.current_page]
        embed.set_footer(text=f"Page={str(self.current_page+1)}/{str(len(self.pages))}")
        await self.message.edit(embed=embed)
    @menus.button("⏮")
    async def first_page(self, payload):
        """Go to next page"""
        
        self.current_page = 0
        await self.change()
    @menus.button("◀")
    async def previous_page(self, payload):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            await self.change()

    @menus.button("\U000023f9")
    async def stop_pages(self, payload):
        """Stop it!"""
        self.stop()
        await self.message.delete()

    @menus.button("\U000025b6")
    async def next_page(self, payload):
        """Go to next page"""
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.change()
    @menus.button("⏭")
    async def last_page(self, payload):
        """Go to next page"""
        
        self.current_page = len(self.pages)-1
        await self.change()
class _HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=0x00ff00)
            await destination.send(embed=embed)
    async def send_bot_help(self, cog):
        ctx = self.context
        COG_LIST=[]
        COMMAND_LIST=[]
        temp = []
        emby= []
        docs = []
        for cog, coghelp in bot.cogs.items():
            COG_LIST.append(cog)
            docs.append(coghelp.__doc__)
            for x in coghelp.walk_commands():
            
                temp.append(x.qualified_name)
            COMMAND_LIST.append(temp)
            temp=[]

        for z in range(0,len(COG_LIST)):
            embed = discord.Embed(title='Shuddho bot all commands',description='Use -help [command] for more info on a command.\nYou can also use -help [category] for more info on a category.\nFor further help,join our official server: [click here](https://discord.gg/Stpr5F7uUy)',color=0x00ff00)
            embed.add_field(name=f"__**{COG_LIST[z]}**__",value=f"{docs[z]}\n\n`{' | '.join(COMMAND_LIST[z])}`",inline=True)
            emby.append(embed)
        menu = MyMenu(emby)
        await menu.start(ctx)

class Moderation(commands.Cog):
    """Basic Moderation!"""
    @commands.command()
    @commands.has_permissions(administrator= True)
    async def kick(self, ctx:commands.Context, member: discord.Member):
        '''Kick a member'''
        embed= discord.Embed(description= f"**{ctx.author.mention}** has pooply💩 kicked {member.mention}",color= 0xff0000)
        await member.kick()
        x= await ctx.send(embed=embed)
        await x.add_reaction("💩")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx:commands.Context, member: discord.Member, role: discord.Role):
        '''give roles!'''
        if role in member.roles:
            await member.remove_roles(role)
            embed= discord.Embed(title="__**Role change**__", description= f"__*{ctx.author.name} has removed {role.mention} from {member.mention} ❌*__")
            await ctx.send(embed= embed)
            
        else:
            await member.add_roles(role)
            embed= discord.Embed(title="__**Role change**__", description= f"__*{ctx.author.name} has added {role.mention} to {member.mention}*__ ✅ ")
            await ctx.send(embed= embed)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx:commands.Context,limit: int):
        '''clear clear!!!'''
        await ctx.channel.purge(limit= 1)
        await ctx.channel.purge(limit= limit)
        embed= discord.Embed(description= f"**{ctx.author.mention}** has pooply💩 purged {limit} messages",color= 0x00ff00)
        x= await ctx.send(embed= embed)
        await x.add_reaction("✅")
        await ctx.channel.purge(limit=1)
    @commands.command(description= '__Ban a member from your server!!__')
    @commands.has_permissions(administrator= True)
    async def ban(self, ctx ,member:discord.Member):
        '''Ban a member from your server!!'''
        await member.ban()
        await ctx.send(f"Banned {member}")

class ApiRelatedCommands(commands.Cog):
    """Made by google api keys!"""
    @commands.command()
    async def youtube(self, ctx:commands.Context,*,query):
        """Youtube Search!"""
        result = youtubeservice.search().list(part="snippet", maxResults=1,q=f"{query}")
        response = result.execute()
        print(response)
        try:
            await ctx.send("https://www.youtube.com/watch?v="+str(response["items"][0]["id"]["videoId"]))
        except Exception as e:
            try:
                await ctx.send("https://www.youtube.com/channel/"+str(response["items"][0]["id"]["channelId"]))
            except Exception as e:
                await ctx.send("https://www.youtube.com/watch?list="+str(response["items"][0]["id"]["playlistId"]))
    @commands.command()
    async def google(self, ctx:commands.Context, *,query):
        """Search Anything."""
        res = await engine.search(query=query,safesearch=True,image_search=True)
        li=[]
        for x in res:
            li.append(discord.Embed(title=x.title,description=x.description,url=x.url).set_thumbnail(url=x.image_url))
        menu = MyMenu(li)
        await menu.start(ctx)
    @commands.command()
    async def image(self, ctx:commands.Context, *,query):
        """Search AnyImage."""
        res = await engine.search(query=query,safesearch=True, image_search=True)
        li=[]
        for x in res:
            li.append(discord.Embed(title=x.title,url=x.url).set_image(url=x.image_url))
        menu = MyMenu(li)
        await menu.start(ctx)
    @commands.command()
    async def img(self, ctx:commands.Context, img_url:str):
        '''Google Image search!'''
        x= await ctx.send("Finding...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.google.com/searchbyimage?hl=en-US&image_url={img_url}&start=0",headers= headers) as r:
                resp = await r.text()
                soup=bs4.BeautifulSoup(resp,"html.parser")
                result= soup.find(class_="fKDtNb")
                embed = discord.Embed(title="Result:",description=result.text)
                embed.set_image(url=img_url)
                await x.edit(content="",embed=embed) 
    @commands.command()
    async def meme(self, ctx:commands.Context):
        '''MEME TIME!'''
        embed = discord.Embed(title="meme", description="test")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.trigger_typing()
                await ctx.send(embed=embed)



    @commands.command(aliases=['cw'])
    async def currentweather(self, ctx,*,area):
        """This command will return the satelite based current vast weather  data of the specified area.But while using this
        command,please make sure to spell the name of the city correctly or check if any city exists with your given name!.
        If you are trying for weather of a city,then,please  provide info as area in this format {'command_ctx'},
        {'city_name'},{'country_code'}. Example : London,uk .If the city/area is under a state under a country ,please make
        sure to  follow this pattern  while writing the command {'city/area name'},{'state_name'},{'country_code'}.While
        using this, please  make sure you have provided the accurate country code for the city/area name.A list of
        areas/cities  and their country code in json  can be downloaded here :http://bulk.openweathermap.org/sample/ Go to
        this link and download the  city.list.json.gz folder. After installing  the zipped folder ,open city.list.json file
        and you will find the list 😎 .Full code can  be found here:https://paste.pythondiscord.com/ukipucecib.py """
        url = f'http://api.openweathermap.org/data/2.5/weather?q={area}&appid=fc0e31b0e6b0229ee01671a6392d7374'
        alu = requests.get(url)
        response = alu.text
        response_to_python_dict = json.loads(response)
        print(response_to_python_dict)
        try:
            if response_to_python_dict['message'] == 'city not found':
                em = discord.Embed(title="City/area not found!!")
                em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                em.add_field(name="Error description and caution",
                            value=f"Dear ***{ctx.author.mention}***,please make sure to spell the name of the city correctly or check if any city exists with your given name!. If you are trying for weather of a city,then,please  provide info as area in this format {'command_ctx'},{'city_name'},{'country_code'}. Example : London,uk .If the city/area is under a state under a country ,please make sure to  follow this pattern  while writing the command {'city/area name'},{'state_name'},{'country_code'}.While using this, please  make sure you have provided the accurate country code for the city/area name.A list of  areas/cities  and their country code in json  can be downloaded here :http://bulk.openweathermap.org/sample/ Go to this link and download the  city.list.json.gz folder. After installing  the zipped folder ,open city.list.json file and you will find the list 😎")
                x=await ctx.send(embed=em)
                await x.add_reaction('❌')
            else:
                print("Allah!!")
        except Exception as e:

            try:
                geographical_coordinate_longitude = response_to_python_dict['coord']['lon']
                geographical_coordinate_latitude = response_to_python_dict['coord']['lat']
                weather_main_status = response_to_python_dict['weather'][0]['main']
                weather_current_temperature = response_to_python_dict['main']['temp']  # K
                the_human_perception_of_weather_temp = response_to_python_dict['main']['feels_like']  # K
                minimum_weather_temp = response_to_python_dict['main']['temp_min']  # K
                maximum_weather_temp = response_to_python_dict['main']['temp_max']  # K

                def pressure_or_sea_or_ground_level():
                    try:
                        weather_pressure = response_to_python_dict['main']['pressure']  # hPa
                        return ["weather_pressure", weather_pressure]
                    except Exception as e:
                        weather_Atmosphericpressure_on_the_sea_level = response_to_python_dict['main']['sea_level']  # hPa
                        weather_Atmosphericpressure_on_the_ground_level = response_to_python_dict['main'][
                            'grnd_level']  # hPa
                        return ["weather_Atmosphericpressure_on_the_ground_level",
                                'weather_Atmosphericpressure_on_the_sea_level',
                                weather_Atmosphericpressure_on_the_ground_level,
                                weather_Atmosphericpressure_on_the_sea_level]

                weather_humidity = response_to_python_dict['main']['humidity']  # %
                weather_visibility = response_to_python_dict['visibility']  # meters

                def wind_speed_or_gust():
                    try:
                        global weather_wind_speed
                        weather_wind_speed = response_to_python_dict['wind']['speed']
                        return ["weather_wind_speed", weather_wind_speed]
                    except Exception as e:
                        global weather_gust
                        weather_gust = response_to_python_dict['wind']['gust']
                        return ["weather_gust", weather_gust]

                weather_cloudiness = response_to_python_dict['clouds']['all']  # %
                weather_requested_country = response_to_python_dict['sys']['country']
                weather_sunrise_unixglobal = response_to_python_dict['sys']['sunrise']
                weather_sunset_unixglobal = response_to_python_dict['sys']['sunset']
                print('hello1!')
                em=discord.Embed(title="Weather Information",description=f"Weather info for **{area}** city/area")
                em.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                em.add_field(name="Area  name",value=f'{area}')
                em.add_field(name="Country", value=f"{weather_requested_country} ")
                em.add_field(name="Main  weather status of that area", value=f"{weather_main_status}")
                em.add_field(name="Geographical coordination : latitude", value=geographical_coordinate_latitude)
                em.add_field(name="Geographical coordination : longitude", value=geographical_coordinate_longitude)
                em.add_field(name="Area current mean temperature",value=f'{weather_current_temperature} K')
                em.add_field(name="Human perception of current weather mean temperature ",value=f'{the_human_perception_of_weather_temp} K')
                em.add_field(name="Maximum temperature of that area",value=f"{maximum_weather_temp} K")
                em.add_field(name="Minimum temperature of that area",value=f"{minimum_weather_temp} K")
                em.add_field(name="Humidity",value=f"{weather_humidity} %")
                em.add_field(name="Visibility",value=f"{weather_visibility} m")
                em.add_field(name="Cloudiness",value=f"{weather_cloudiness} %")
                em.add_field(name="Sunrise time of today in this area in unix format", value=f"{weather_sunrise_unixglobal}")
                em.add_field(name="Sunset time of today in this area in unix format", value=f"{weather_sunset_unixglobal}")

                em.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPF1zshzTiPuask9RbYVkwSbI42oayxog_FA&usqp=CAU')
                if type(wind_speed_or_gust())== list and wind_speed_or_gust()[0]=="weather_gust":
                    em.add_field(name="Wind_gust", value=f'{wind_speed_or_gust()[1]} m/s')
                elif  type(wind_speed_or_gust())== list and wind_speed_or_gust()[0]=="weather_wind_speed":
                    em.add_field(name="Wind_speed", value=f'{wind_speed_or_gust()[1]} m/s')
                elif type(pressure_or_sea_or_ground_level())==list and  pressure_or_sea_or_ground_level()[0]=="weather_pressure":
                    em.add_field(name="Atmospheric pressure",value=f'{pressure_or_sea_or_ground_level()[1]} hPa')
                elif type(pressure_or_sea_or_ground_level())==list and  pressure_or_sea_or_ground_level()[0]=="weather_Atmosphericpressure_on_the_ground_level" and  pressure_or_sea_or_ground_level()[1]=='weather_Atmosphericpressure_on_the_sea_level':
                    em.add_field(name="Atmospheric pressure on ground level",value=f"{pressure_or_sea_or_ground_level()[3]} hPa")
                    em.add_field(name="Atmospheric pressure on sea level", value=f"{pressure_or_sea_or_ground_level()[4]} hPa")
                em.set_footer(text=f'Requested by {ctx.author} ⚫ ©2021ShuddhoBot')
                x=await ctx.send(embed=em)
                await  x.add_reaction("✅")
            except  Exception  as e:
                print("Here is the exception")
                print(e)
    @commands.command()
    async def translate(self, ctx, lang='en',*,query):
        '''Get A Word Translated for you!'''
        res = translator.translate(text=query, dest=lang)
        await ctx.send(f"{res.text}")
    @commands.command()
    async def define(self, ctx,*,query):
        '''Get meanings of an Word'''
        des = f"```{dictionary.meaning(query)}```"
        await ctx.send(embed = discord.Embed(title=f"__Meaning of {query}__",description=des, color=0x00ff00).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
                
    @commands.command()
    async def synonym(self, ctx,*,query):
        '''Get synonyms of an Word'''
        des = f"```{dictionary.synonym(query)}```"
        await ctx.send(embed = discord.Embed(title=f"__Synonyms of {query}__",description=des, color=0x00ff00).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
    @commands.command()
    async def antonym(self, ctx,*,query):
        '''Get antonyms of an Word'''
        des = f"```{dictionary.antonym(query)}```"
        await ctx.send(embed = discord.Embed(title=f"__Antonyms of {query}__",description=des, color=0x00ff00).set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url))
class Games(commands.Cog):
    """Play games via me"""
    @commands.command(aliases=['gtn'],description='__Guess The Number game!!`[Only Admins can use!]`__')
    @commands.has_permissions(administrator=True)
    async def guessthenumber(self,ctx,limit: int):
        '''guess the number!'''
        ran_num= random.randint(1,limit)
        mes=0
        await ctx.channel.send(f"now choose numbers between 1 and {limit}")
        await ctx.author.send(f"The random number is {ran_num}.")
        while True:
            message=await bot.wait_for("message")
            if message.content.isdigit():
                mes+=1
                if int(message.content) == ran_num:
                    await ctx.channel.send("🥳🥳🥳🥳")
                    embed = discord.Embed(title="**Winner Winner Chicken Dinner**", description=f"{message.author.mention} has won the loling game", color=0x00ffff)
                    embed.add_field(name="__**Random number**__", value=f"The Random number was {ran_num}", inline=True)
                    embed.add_field(name="__**Total Attempts**__", value=f"{mes}", inline=False)
                    await ctx.channel.send(embed= embed)
                    break
            else:
                await ctx.channel.send("Pls pick up an integer")
     
    @commands.command(aliases=['cc'],description= "__The childhood game CHARLIE CHARLIE!!__")
    async def charlie_charlie(self,ctx,x):
        '''The childhood game CHARLIE CHARLIE!!'''
        t= "Yes"
        d= "No"
        await ctx.send(random.choice([d,t]))
    @commands.command(description= "Hack your friend `[LOL]`")
    async def hack(self, ctx, member:discord.Member):
        '''hack prank!'''
        member = (str(member.name).split(" "))[0]
        a= f"Hacking {member}..."
        hacking= "https://tenor.com/view/cyberpunk-hacker-gif-5648977"
        b= f"Hacked 50 % \nPass: {member}shitsHard123"
        num2= f"Hacked 60 %\n email user name = gamernoob{member}"
        c= f"Hacked 100% \n{member} bullied hard and now ready to suicide!"
        num3= f"Selling data to government 💻"
        d=f"A 100% real hacking done.{member} is now dead." 
        x= await ctx.send(content=a)
        hacked=await ctx.send(content= hacking)
        await asyncio.sleep(2.0)
        await x.add_reaction("✅")
        y= await x.edit(content=b)
        await asyncio.sleep(2.0)
        await x.add_reaction("✅")
        p= await x.edit(content= num2)
        await asyncio.sleep(2.0)
        await x.add_reaction("✅")
        await hacked.delete()
        z= await x.edit(content= c)
        await asyncio.sleep(2.0)
        await x.add_reaction("✅")
        q= await x.edit(content= num3)
        await asyncio.sleep(2.0)
        await x.add_reaction("✅")
        w= await x.edit(content= d)
        await asyncio.sleep(2.0)
        await x.edit(content= f"Hacking {member} successfully done!")
        await x.delete()
        await ctx.message.delete()
    @commands.command()
    async def slap(self, ctx, member:discord.Member):


        img = Image.open("slap.gif")
        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("arial.ttf", 100)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0),f"Slapping {member.name}",(255,255,255),font=font)
        
        img.save('slapout.gif')
        await ctx.send(file= file.File("slapout.gif"))
    @commands.command()
    async def plan(self, ctx,plan1, plan2, plan3, plan4):
        img = Image.open("template.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 60)
        draw.text((300,70),f"{plan1}", (0,0,0), font=font)
        draw.text((800, 70),f"{plan2}", (0,0,0), font=font)
        draw.text((300, 400),f"{plan3}", (0,0,0), font=font)
        draw.text((800, 400),f"{plan4}", (0,0,0), font=font)
        img.save("templateout.jpg")
        await ctx.send(file = file.File("templateout.jpg"))

class Direct_Send(commands.Cog):
    """Direct send your friend and surprise him!"""
    @commands.command(description= '__Direct Message your target__')
    async def dm(self, ctx, member:discord.Member, *,your_message):
        '''Direct Message your target'''
        await member.send(your_message)
        await ctx.message.add_reaction("😁")
        await ctx.channel.purge(limit= 1)
    @commands.command(description= '__Quickly direct emb your target__')
    async def demb(self, ctx, member:discord.Member, title,description):
        """Quickly direct emb your target"""
        embed=discord.Embed(title= title, description= description, color=0x00ff00)
        await member.send(embed= embed)
        await ctx.message.add_reaction("😁")
        await ctx.channel.purge(limit= 1)

class Send_Message(commands.Cog):
    """Express your thoughts via me!"""
    @commands.command(description= '__Send a message via me.__')
    async def say(self, ctx ,your_message):
        '''I will listen to what you say!'''
        await ctx.send(your_message)
    @commands.command(description='__Send a embed message via me__')
    async def emb(self, ctx, title, description):
        '''I can send embed message for you! :)'''
        embed= discord.Embed(title= title, description= description, color=0x00ff00)
        await ctx.send(embed= embed)
def getElements(param):
    methodlist=[]
    for x in dir(param):
        if x.startswith("__") and x.endswith("__"):
            pass
        if x.startswith("_"):
            pass
        else:
            methodlist.append(x)
    return methodlist
class Test(commands.Cog):
    @commands.command(name='😁')
    async def test(self, ctx):
        e = bot.cogs.items()
        await ctx.send(getElements(Moderation))
    @commands.command()
    async def connect(self, ctx:commands.Context, channel:discord.VoiceChannel):
        global connected
        connected = await channel.connect()
        
    @commands.command()
    async def play(self, ctx:commands.Context):
        '''Playing Song'''
        pass
        

def loading():
    global balance
    with open("data.json","r") as fr:
        balance = json.loads(fr.read())
loading()
balance = balance
def save():
    with open("data.json","w") as fw:
        fw.write(json.dumps(balance))
def create_account(name:str):
    balance[name] = 0
    save()

class Economy(commands.Cog):
    '''Economy Commands and it is halal! :)'''
    @commands.command()
    async def wallet(self, ctx, *kwargs:discord.Member):
        '''Get Wallet!'''
        if kwargs:
            if kwargs[0].name not in balance.keys():
                create_account(kwargs[0].name)
                save()
            embed = discord.Embed(title = f"{kwargs[0].name}'s Balance:", description=f"Wallet: {balance[kwargs[0].name]}", color=0x00ff00)
            await ctx.send(embed=embed)
            return
            
        if not ctx.author.name in balance.keys():
            create_account(ctx.author.name)
            save()
        await ctx.send(embed =  discord.Embed(title = f"{ctx.author.name}'s Balance:", description=f"Wallet: {balance[ctx.author.name]}", color=0x00ff00))
    @commands.command()
    @commands.cooldown(1,4)
    async def work(self, ctx):
        '''Work and earn!'''
        c =random.randint(1,100000)
        balance[ctx.author.name] += c
        await ctx.send(f"Congrats You got {c}$")
        save()
    @commands.command()
    async def give(self, ctx, member:discord.Member,limit):
        '''Share with your kindness!'''
        if limit == "all":
            limit = balance[ctx.author.name]
        else:
            limit = int(limit)
        if limit > int(balance[ctx.author.name]):
            raise LolException("You can't share more than you have in your wallet")
            return
        balance[member.name] += limit
        balance[ctx.author.name] -= limit
        save()
        await ctx.send(f"You gave {member.mention} {limit}")
        save()
class ServerStaffs(commands.Cog):
    """Server Stuffs"""
    @commands.command()
    async def poll(self, ctx:commands.Context, question, *,opts):
        '''Poll Time!'''
        option_lista = []
        num = 1
        numberlista= ['one','two','three','four','five','six','seven','eight','nine','ten']
        for x in opts.split("|"):
            option_lista.append(str(num)+"."+x)
            num+=1
        embed = discord.Embed(title = "Q:"+question, description="\n".join(option_lista), color=0x00ffff)
        x = await ctx.send(embed=embed)
        emojilista = "1⃣ 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ 7⃣ 8⃣ 9⃣ 0⃣"
        y = emojilista.split(" ")
        for l in range(0,len(option_lista)):
            await x.add_reaction(f"{y[l]}")
    @commands.command()
    async def profile(self, ctx,member: discord.Member):
        '''Profile of an member!'''
        m=list(map(str,member.roles))
        x=",".join(m)
        embed = discord.Embed(title=f"**Profile of{member.mention} is given below:-**", description=f"Name: {member.name}\nHashtag: {hash(member)}\nFull Discord Name: {member}\nid: {member.id}", color=0x00ff00)
        embed.add_field(name="**Roles:-**", value= f"__Roles:__ {x} \n__Highest role:__ \n{member.top_role}", inline=True)
        embed.add_field(name="**Icon Url:-**", value=f"[click here]({member.avatar_url})", inline=True)
        embed.add_field(name="**nickname:-**", value=f"{member.nick}", inline=True)
        embed.add_field(name="**status:-**", value=f"Main Status :{member.status}", inline=True)
        embed.add_field(name="**Current Server:-**", value=f"{member.guild}", inline=True)
        embed.add_field(name="**Currently Doing:-**", value=f"**{member.activity}**", inline=True)
        embed.add_field(name="**Premium Since:-**", value=f"{member.premium_since}", inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Watch out bros.ITZ {member.name}'s profile", icon_url=member.avatar_url)
        await ctx.send(embed= embed)

    @commands.command()
    async def sp(self, ctx):
        '''Server Infos!'''
        emoji= ctx.guild.emojis
        roles= ctx.guild.roles
        channels= ctx.guild.channels
        m=list(map(str,roles))
        s=",".join(m)
        y=0
        z=0
        r=0
        for x in emoji:
            y+=1
        for a in roles:
            z+=1
        for t in channels:
            r+=1
        txtch=ctx.guild.text_channels
        k=0
        vc= ctx.guild.voice_channels
        e=0
        for f in txtch:
            k+=1
        for p in vc:
            e+=1
        o=0
        bot= [i for i in ctx.guild.members if i.bot]
        for t in bot:
            o+=1
        embed = discord.Embed(title="**Server profile**", color=0x00ffff)
        embed.add_field(name="Informations:-", value=f"Name: {ctx.guild.name}\nRegion: {ctx.guild.region}\nID: {ctx.guild.id}\nCreated time: {ctx.guild.created_at}\n😏Emoji: {y}/{ctx.guild.emoji_limit}\nRoles= __*{s}*__\nOwner: {ctx.guild.owner}\nMax presence: {ctx.guild.max_presences}\nVerification Level: {ctx.guild.verification_level}\nTier: {ctx.guild.premium_tier}\nbooster: {ctx.guild.premium_subscribers}\nTotal Roles:{z}", inline=True)
        embed.add_field(name="Icon url:-", value=f"[click here]({ctx.guild.icon_url})", inline=True)
        embed.add_field(name="Features:-", value=ctx.guild.features, inline=True)
        embed.add_field(name="Members:-", value=f"Member max: {ctx.guild.max_members}\nTotal members: {ctx.guild.member_count}\nHuman: {ctx.guild.member_count-o}\nBot: {o}", inline=True)
        embed.add_field(name="Channels:-", value=f"Total channels: {r-(r-e-k)}\n\tText Channels: {k}\n Voice Channels: {e}\n**Total Categories:-** {r-k-e}", inline=True)
        embed.add_field(name="Upload Limit:-", value=f"{ctx.guild.filesize_limit//1000000}MB(Mega Byte)", inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Wat a Server Lol! 😂", icon_url="https://cdn.discordapp.com/attachments/770170269490610186/776442839017979954/unknown.png")
        await ctx.send(embed= embed)
    @commands.command()
    async def emoji(self, ctx:commands.Context, index:int):
        emlist = requests.get("https://emoji.gg/api")
        emlista = json.loads(emlist.text)
        await ctx.guild.create_custom_emoji(name=emlista[index]["title"],image= requests.get(emlista[index]["image"]).content)
        await ctx.send(embed=discord.Embed(title= "Emoji Added To Server", description="emoji name="+emlista[index]["title"]).set_image(url=emlista[index]["image"]))
class Fun(commands.Cog):
    @commands.command()
    async def welcome(self, ctx,member:discord.Member):
        embed = discord.Embed(title="Hi", description=f"{member.mention} Welcome to our server!!", color=0x00ffff)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://media.tenor.com/images/21876a70dc11009779f0c1cf8fddd531/tenor.gif")
        await ctx.send(embed= embed)

    @commands.command()
    async def bye(self, ctx,member:discord.Member):
        embed = discord.Embed(title="Bye", description=f"{member.mention}Bye Bye!!", color=0x00ffff)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url="https://media.tenor.com/images/cd0677015add1ccf42089651ce2494fb/tenor.gif")
        await ctx.send(embed= embed)
    @commands.command()
    async def sad(self, ctx,member:discord.Member):
        embed = discord.Embed(title="SO SAD", description=f"Sad bruh{ctx.author.mention} ", color=0x00ff00)
        embed.set_thumbnail(url= member.avatar_url)
        embed.set_image(url="https://media.tenor.com/images/f4d3196cf64ba98f370abdb8ca4b364b/tenor.gif")
        await ctx.send(embed= embed)
    @commands.command()
    async def bruh(self, ctx):
        await ctx.send("https://tenor.com/view/bruh-bye-ciao-gif-5156041")
    @commands.command()
    async def dance(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/770170269490610186/775926956876759050/122786266_706051873642540_2584264494843254926_n.gif")
    @commands.command()
    async def smack(self, ctx,member:discord.Member):
        embed = discord.Embed(title="**OH NO SHIT!!", description=f"{ctx.author.mention} has pooply smacked {member.mention}", color=0x00ffff)
        embed.set_image(url="https://media.tenor.com/images/7f65326a907d57d2fa5e80c046c8b42b/tenor.gif ")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_thumbnail(url="https://media1.tenor.com/images/ef59493b8238a9ed054baeb6203fbc95/tenor.gif?itemid=10905440")
        embed.set_footer(text="Watch buddies Lol", icon_url=member.avatar_url)
        await ctx.send(embed=embed)



                    
@bot.event
async def on_command_error(ctx:commands.Context,error):
    error = getattr(error, "original", error)
    if isinstance(error, discord.Forbidden):
        embed= discord.Embed(description= f"{ctx.author.mention} , my role is not higher than that role....make it at the top first.",color= 0x0ff000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed()
        embed.add_field(name="ERROR",value="```bash\n"+"|"+type(error).__name__+"|:"+str(error)+"```",inline=True)
        embed.set_footer(text="Write `report` to report to the official server",icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/BSOD_Windows_8.svg/1200px-BSOD_Windows_8.svg.png")
        await ctx.send(embed=embed)
        msg = await bot.wait_for("message")
        if msg.content == "report":
            destination:discord.TextChannel = bot.get_channel(815136930235940866)
            await destination.send(content="*Error:*"+"```bash\n"+"|"+type(error).__name__+"|:"+str(error)+"```")
    raise error

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if str(message.channel.id) == "815818627814522972":
        if message.content == "😁":
            await message.channel.send("Kire! hashos ken?")
        elif message.content == "😂":
            await message.channel.send("Hasar somoy kandar kisu hoy nai "+message.author.name)
        elif "chup thak" in message.content:
            await message.channel.send("Tui chup kor beta "+message.author.name)
        elif message.content == "😡":
            await message.channel.send("uttejito howar kono karon nai "+message.author.name)
    
nav = Navigation()

bot.add_cog(Moderation())
bot.add_cog(Games())
bot.add_cog(Economy())
bot.add_cog(Fun())
bot.add_cog(Direct_Send())
bot.add_cog(Send_Message())
bot.add_cog(ApiRelatedCommands())
bot.add_cog(Test())
bot.add_cog(ServerStaffs())
bot.load_extension('jishaku')
bot.help_command= _HelpCommand()


bot.run("ODE0MDIwMzc1NTU4MDk0ODUy.YDXxjQ.d_tEiQpR1t3dwg2oETyqaKprP0E")

