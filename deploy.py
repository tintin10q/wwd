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
Maak een dictionary met random rol namen

------------------------------------------------------------------------------------------------------------------------
'''

description = 'HENRY!!!!'

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(discord.__version__)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.server = self.get_guild(215328190858657792)
        print(self.guilds)

    async def on_message(self, message):
        self.message_channel = message.channel
        self.bericht_text = message.content.split()
        if message.author != client.user:
            self.bericht_text = message.content.split()

            #Add text channels
            if self.bericht_text[0] == "!init":
                self.weerwolfen_category = await self.server.create_category("Weerwolfen")

                self.het_plein_channel = await self.server.create_text_channel("Het plein",
                                                                               category=self.weerwolfen_category)
                self.cupido_channel = await self.server.create_text_channel("Cupido",
                                                                               category=self.weerwolfen_category)
                self.ziener_channel = await self.server.create_text_channel("Ziener",
                                                                               category=self.weerwolfen_category)
                self.weerwolfen_channel = await self.server.create_text_channel("Weerwolfen Chat",
                                                                               category=self.weerwolfen_category)
                self.heks_channel = await self.server.create_text_channel("Heks",
                                                                               category=self.weerwolfen_category)
                self.geliefde_channel = await self.server.create_text_channel("Geliefde chat",
                                                                               category=self.weerwolfen_category)

                await self.server.create_role(name="Weerwolfen spel",mentionable=True)


            # exit remove text channels
            if self.bericht_text[0] == "!exit":
                for i in self.server.channels:
                    if i.category != None and i.category.name == "Weerwolfen":
                        await i.delete()

                for i in self.server.categories:
                    if i.name == "Weerwolfen":
                        await i.delete()

                for i in self.server.roles:
                    if i.name in ("Weerwolfen spel"):
                        await i.delete()

client = MyClient()
client.run("NDg0MzIxNDAyMTcwNzY5NDE4.DmgTcQ.x9jzBwYQC1OR3rHd9Grqw527nT0")
