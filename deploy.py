''''
Discord:

$ Weerwolven van wakeredam

# Het plein     (Iedereen kan hier praten)
# Cupido        (De ziener kan hier zeggen wie verbonden moet worden)
# Ziener        (De ziener kan hier zeggen wie ze wil zien)
# Weerwolfen    (De weerwolfen kunnen hier praten en zeggen wie dood moet)
# Heks          (De heks kan hier iemand doden of redden)
# Eventuweel kech (Slaap plek regelen)
# Geliefde      (Geliefde chat)
# Jager

> Dag           (Hier kan iedereen tijdens de dag periode in)
> Nacht         (Hier kunnen de weerwolfen in)
------------------------------------------------------------------------------------------------------------------------
Maak een rol select met weerwolfen potje
Maak een start commando
Als start comando
    Pak alle mensen met weerwolfen rol
    Maak lijst met class vorm van alle leden
    Geef random rollen met random namen en zet ze in een dictionary
------------------------------------------------------------------------------------------------------------------------
1e Nacht
    Haal acces weg van dag chat
    Vraag cupido wie verbonden moet worden  :   >verbind @naam1 @naam2
    Als goed Verbind hun en zeg het tegen ze

    Vraag ziener wie gezien wil worden   :   >zien @naam
    return de rol en naam via dictionary

    Vraag weerwolfen wie ze willen vermoorden   :   >killvote @naam (persoon met meeste votes gaat dood)
    Sla op wie dood is

    Zeg tegen heks deze persoon is dood en zeg dan wat ze nog kan doen als niks word ze ook niet opgeroepen
    >kill @naam  >genees en dan >submmit

1e Dag
    -Geef iedereen acces tot dag voice chat
    Burgermeester kiezen
    >Burgermeester @naam
    error handeling -> als alle votes klaar zijn verder

    Kiezen wie dood moet
    >Stem @naam
    error handeling -> als alle votes klaar zijn verder

Nacht   2..
    Zelfde als eerste nacht alleen dan zonder cupido

Dag     2..
    Hetzelfde als eerste dag maar geen burgermeester


------------------------------------------------------------------------------------------------------------------------
Rollen
Tel hoeveel spelers meedoen
Kijk of meer dan 8
doe nummer in dict waaruit lijst komt met alle te verdelen rollen
maak persoon classen en voeg ze toe aan een lijst
Maak een dictionary met random rol namen

------------------------------------------------------------------------------------------------------------------------
Geliefde apart
'''

description = 'Testing...'

import discord
from random import shuffle, choice
import string
from json import load
from io import BytesIO
from time import sleep

class Player():
    # Dit is een player class van iemand die meedoet
    def __init__(self,member):
        self.member = member
        self.name = self.member.name
        self.rol = None
        self.rol_display_name = None
        self.in_love = "alone"
        self.levend = True
        self.burgermeester = False

    def __str__(self):
        return "Speler: {}\nHij/zij is {}\n----------------".format(self.name,self.rol_display_name)

class Vote():
    emoji_lijst = ["0⃣","1⃣","2⃣","3⃣","4⃣","5⃣","6⃣","7⃣","8⃣","9⃣","🔟","💟","☮","✝","☪","🕉","☸","✡","🕎","☯","☦","🛐","⛎","♈","♉","⚛","♋","♌","♍","♎","♏","♐","🈚","♒","♓","🆔","⚛"]
    def __init__(self, speler_lijst, message_text, channel):
        self.message_text = message_text + '\n'
        self.speler_lijst = speler_lijst
        self.channel = channel
        self.member_aantal = len(speler_lijst)
        self.vote = []
        self.emoji_to_member_dict = {}
        self.member_to_emoji_dict = {}
        for speler,emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            self.member_to_emoji_dict[speler] = emoji
        for speler,emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            self.emoji_to_member_dict[emoji] = speler

    async def send_message(self):
        # stuur de message
        # add reactions
        for speler,emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            self.message_text += "{}    -   {}\n".format(emoji,speler.name)
        self.message = await self.channel.send(self.message_text)

        for speler in self.speler_lijst:
            await self.message.add_reaction(self.member_to_emoji_dict[speler])

    async def cupido(self,channel):
        geliefden = [self.emoji_to_member_dict[i.emoji] for i in self.vote]
        await channel.set_permissions(target=geliefden[0].member, read_messages=True, send_messages=True)
        await channel.set_permissions(target=geliefden[1].member, read_messages=True, send_messages=True)

        geliefden[0].in_love = geliefden[1] # zet elkaar in elkaars player class
        geliefden[1].in_love = geliefden[0] # zet elkaar in elkaars players class
        await self.channel.send("{} en {} zijn intens verlieft op elkaar geworden".format(geliefden[0].name, geliefden[1].name))
        return

    async def ziener(self,reaction):
        target = self.emoji_to_member_dict[reaction.emoji]
        await reaction.message.channel.send("{} is {}".format(target.name,target.rol_display_name))
        return






class MyClient(discord.Client):
    # Dit is de custom bot class van de rewrite
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('----------------')
        print(self.guilds)
        self.init = False


    async def on_message(self, message):
        # dit triggert als er een message komt
        self.server = message.guild         # van welke server kwam de message
        self.bericht_text = message.content.split()     # split de bericht text

        if message.author != client.user:                   # check of auteur niet bot is zodat je niet dood gespamt wordt
            self.bericht_text = message.content.split()

            #Add text channels
            if self.bericht_text[0] == "!init":
                # if self.init == True:
                #     return
                # self.init = True
                self.weerwolfen_category = await self.server.create_category("Weerwolfen")

                self.het_plein_channel = await self.server.create_text_channel("Het plein",category=self.weerwolfen_category)
                self.cupido_channel = await self.server.create_text_channel("Cupido",category=self.weerwolfen_category)
                self.ziener_channel = await self.server.create_text_channel("Ziener",category=self.weerwolfen_category)
                self.weerwolfen_channel = await self.server.create_text_channel("Weerwolfen",category=self.weerwolfen_category)
                self.heks_channel = await self.server.create_text_channel("Heks",category=self.weerwolfen_category)
                self.geliefde_channel = await self.server.create_text_channel("Geliefde chat",category=self.weerwolfen_category)
                self.jager_channel = await self.server.create_text_channel("Jager",category=self.weerwolfen_category)
                #voice
                self.dag_channel = await self.server.create_voice_channel("🌞 Dag",category=self.weerwolfen_category)
                self.nacht_channel = await self.server.create_voice_channel("🌙 Nacht",category=self.weerwolfen_category)

                self.channel_dict = {"Het plein:":self.het_plein_channel,
                                     "Cupido":self.cupido_channel,
                                     "Ziener":self.ziener_channel,
                                     "Weerwolf":self.weerwolfen_channel,
                                     "Heks":self.heks_channel,
                                     "Geliefde":self.geliefde_channel,
                                     "Jager":self.jager_channel,
                                     "Dag":self.dag_channel,
                                     "Nacht":self.nacht_channel}

                self.weerwolfen_spel_rol = await self.server.create_role(name="spel Weerwolfen",mentionable=True)

                # set permissions op de channels
                for i in self.weerwolfen_category.channels:
                    await i.set_permissions(target=self.server.default_role, read_messages=False)
                await self.het_plein_channel.set_permissions(target=self.weerwolfen_spel_rol,send_messages=True,read_messages=True)
                await self.dag_channel.set_permissions(target=self.weerwolfen_spel_rol,connect=True, speak=True, use_voice_activation=True,read_messages=True)


            # Start commando
            print(message.content)
            if self.bericht_text[0] == "!start":
                self.player_lijst = []


                for member in self.weerwolfen_spel_rol.members:
                    self.player_lijst.append(Player(member))
                shuffle(self.player_lijst)
                self.player_hoeveelheid = len(self.player_lijst)
                if self.player_hoeveelheid < 6:
                    await message.channel.send("Te weinig spelers doen mee.\nGeef meer leden de Weerwolf spel rol")
                    return

                self.rollen_lijst = await self.get_game_rollen(self.player_hoeveelheid)
                if len(self.rollen_lijst) == self.player_hoeveelheid:
                    for speler, rol in zip(self.player_lijst,self.rollen_lijst):
                        speler.rol = rol                                            # Doe rol object in de player class
                        await speler.member.add_roles(rol)                          # Voeg rol toe aan member
                        speler.rol_display_name = rol.name                          # Voeg display name toe aan member
                        await rol.edit(name=id_generator())                         # Verander rol naam in random string
                        # await message.channel.send(str(speler))

                        if not speler.member.bot:                                   # Als speler niet bot stuur dan bericht met info
                            await speler.member.send(delete_after=30,embed=discord.Embed(description="You are {}".format(speler.rol_display_name),colour=discord.Colour(value=1412412)))

                    for i in self.player_lijst:
                        if i.rol_display_name == "Burger":
                            continue
                        await self.channel_dict[i.rol_display_name].set_permissions(target=i.rol,read_messages=True,send_messages=True)
                        if i.rol_display_name == "Weerwolf":
                            await self.nacht_channel.set_permissions(target=i.rol,connect=True,speak=True,use_voice_activation=True)

                    # Eerste nacht
                    await self.het_plein_channel.send("Het is nacht cupido wordt wakker en wijst 2 geliefde aan")
                    self.cupido_vote = Vote(message_text="Cupido wijst 2 gelefde aan",speler_lijst=self.player_lijst,channel=self.cupido_channel)
                    await self.cupido_vote.send_message()
                    self.gameloop_currentrol = "cupido"
                return

            # !Clean
            if self.bericht_text[0] == "!clean":
                cool = []
                for i in self.server.roles:
                    if i.name != "spel Weerwolfen":
                        if i.name in ("Jager","Weerwolf","Cupido","Ziener","Heks","Burger") or i.name[:4] == "spel":
                            cool.append(i)

                for i in cool:
                    await i.delete()

                return

            # !join all
            if self.bericht_text[0] == "!join" and self.bericht_text[1] == "all":
                for i in self.server.members:
                    await i.add_roles(self.weerwolfen_spel_rol)
                await message.channel.send("Done",delete_after=2)
                return


            # exit remove text channels
            if self.bericht_text[0] == "!exit":
                # if self.init == False:
                #     return
                # self.init = False

                for i in self.server.channels:
                    if i.category != None and i.category.name == "Weerwolfen":
                        await i.delete()

                for i in self.server.categories:
                    if i.name == "Weerwolfen":
                        await i.delete()

                delete_list = []
                for i in self.server.roles:
                    if i.name[:4] == "spel":
                        delete_list.append(i)

                for i in delete_list:  # anders lukt het niet goed
                    await i.delete()
                return

            # purge
            if self.bericht_text[0] == "!purge":
                try:
                    if len(self.bericht_text) == 1 or self.bericht_text[1] == 1:
                        hoeveel_messages = 2
                    else:
                        hoeveel_messages = int(self.bericht_text[1])+1

                    await message.channel.purge(limit=hoeveel_messages)
                except ValueError:
                    await message.channel.send("Geen getal gegeven",delete_after=7)
                return


    async def get_game_rollen(self,player_hoeveelheid):
        rollen_lijst = [await self.server.create_role(name="Cupido"),
                        await self.server.create_role(name="Ziener"),
                        await self.server.create_role(name="Weerwolf"),
                        await self.server.create_role(name="Weerwolf"),
                        await self.server.create_role(name="Heks"),
                        await self.server.create_role(name="Jager")
                        ]

        if player_hoeveelheid > 26:
            rollen_lijst.extend((
                await self.server.create_role(name="Weerwolf"),
                await self.server.create_role(name="Weerwolf"),
                self.server.create_role(name="Weerwolf")))
        elif player_hoeveelheid > 17:
            rollen_lijst.extend((await self.server.create_role(name="Weerwolf"),
                                 await self.server.create_role(name="Weerwolf")))
        elif player_hoeveelheid > 12:
            rollen_lijst.append(await self.server.create_role(name="Weerwolf"))

        while player_hoeveelheid != len(rollen_lijst):
            rollen_lijst.append(await self.server.create_role(name="Burger"))

        shuffle(rollen_lijst)
        return rollen_lijst


    async def on_reaction_add(self,reaction, user):

        if user == client.user:
            return

        # kijk in welk channel de reaction is
        # doe de logica voor dat channel en ga naar de volgende

        self.react_channel = reaction.message.channel

        # cupido
        if self.react_channel.name == "cupido" and self.gameloop_currentrol == "cupido":

            self.cupido_vote.vote.append(reaction)
            if self.get_reaction_amount(reaction) == 2:          # look for 2 reactions and they should have a count of 2
                await self.cupido_vote.cupido(channel=self.geliefde_channel)
                del self.cupido_vote

                await reaction.message.delete()

                # we gaan nu naar ziener
                self.gameloop_currentrol = "ziener"
                await self.het_plein_channel.send("De ziener wordt wakker en bekijkt iemands persoonlijkheid")
                self.ziener_vote = Vote(message_text="Wie wil de ziener bekijken", speler_lijst=self.player_lijst,
                                        channel=self.ziener_channel)
                await self.ziener_vote.send_message()


        # Ziener
        if self.react_channel.name == "ziener" and self.gameloop_currentrol == "ziener":
            await self.ziener_vote.ziener(reaction=reaction)
            del self.ziener_vote
            await reaction.message.delete()

            # we gaan nu over naar weerwolfen
            self.gameloop_currentrol = "weerwolf"
            await self.het_plein_channel.send("De weerwolfen worden wakker opzoek naar een midnight snack")
            self.weerwolfen_vote = Vote(message_text="Wie gaan julie opeten", speler_lijst=[speler for speler in self.player_lijst if speler.rol_display_name != "Weerwolf"],
                                    channel=self.weerwolfen_channel)
            await self.weerwolfen_vote.send_message()


        if self.react_channel.name == "weerwolfen" and self.gameloop_currentrol == "weerwolf":

            pass

    def get_reaction_amount(self,reaction):
        count = 0
        emoji_count = len(reaction.message.reactions)       # Hoeveel emoji's zijn er
        for emoji in reaction.message.reactions:            # ga door alle reacties heen
            count += emoji.count
        count -= emoji_count                                # hier hou je alleen de exstra reacties over
        return count

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "spel"+''.join(choice(chars) for _ in range(size))



client = MyClient()

client.run(load(open("config.json", "r"))["key"])

