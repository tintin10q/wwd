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
from time import sleep

class Player():
    def __init__(self,member):
        self.member = member
        self.rol = None
        self.rol_display_name = None
        self.levend = True
        self.burgermeester = False

    def __str__(self):
        return "Speler: {}\nHij/zij is {}\n----------------".format(self.member.name,self.rol_display_name)

class Vote():
    pass

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('----------------')
        print(self.guilds)
        self.init = False



    async def on_message(self, message):

        self.message_channel = message.channel
        self.server = message.guild
        self.bericht_text = message.content.split()

        if message.author != client.user:
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

                for i in self.weerwolfen_category.channels:
                    await i.set_permissions(target=self.server.default_role, read_messages=False)
                await self.het_plein_channel.set_permissions(target=self.weerwolfen_spel_rol,send_messages=True,read_messages=True)
                await self.dag_channel.set_permissions(target=self.weerwolfen_spel_rol,connect=True, speak=True, use_voice_activation=True,read_messages=True)


                for i in self.server.members:
                    await i.add_roles(self.weerwolfen_spel_rol)

                return
            # Start commando
            if self.bericht_text[0] == "!start":
                self.player_lijst = []
                self.weerwolfen_rol = [i for i in self.server.roles if i.name == "spel Weerwolfen"][0]

                for member in self.weerwolfen_rol.members:
                    self.player_lijst.append(Player(member))
                    await message.channel.send(member.name)
                shuffle(self.player_lijst)
                self.player_hoeveelheid = len(self.player_lijst)
                if self.player_hoeveelheid < 7:
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
                            await speler.member.send(embed=discord.Embed(description="Jij bent {}".format(speler.rol_display_name),colour=discord.Colour(value=1412412)),delete_after=30)

                    for i in self.player_lijst:
                        if i.rol_display_name == "Burger":
                            continue
                        await self.channel_dict[i.rol_display_name].set_permissions(target=i.rol,read_messages=True,send_messages=True)
                        if i.rol_display_name == "Weerwolf":
                            await self.nacht_channel.set_permissions(target=i.rol,connect=True,speak=True,use_voice_activation=True)

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

            if self.bericht_text[0] == "!test":
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

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "spel"+''.join(choice(chars) for _ in range(size))

client = MyClient()
client.run("NDg0MzIxNDAyMTcwNzY5NDE4.DmgTcQ.x9jzBwYQC1OR3rHd9Grqw527nT0")

