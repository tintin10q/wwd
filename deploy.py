''''
To do:
    weerwolfen hebben geen acces tot nacht chat
    maar voice channel permissions
------------------------------------------------------------------------------------------------------------------------
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



import discord
from random import shuffle, choice
import string
from json import load
import re

description = 'Testing...'

class Player():
    # Dit is een player class van iemand die meedoet
    def __init__(self, member):
        self.member = member
        self.name = self.member.name
        self.rol = None
        self.rol_display_name = None
        self.in_love = False
        self.levend = True
        self.burgermeester = False

    def __str__(self):
        return self.name

    async def die(self, dood_rol):
        await self.member.remove_roles(self.rol)
        await self.member.add_roles(dood_rol)
        self.levend = False

        # remove rols
        # kill cupido


class Vote():
    emoji_lijst = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "💟", "☮", "✝", "☪", "🕉", "☸",
                   "✡", "🕎", "☯", "☦", "🛐", "⛎", "♈", "♉", "⚛", "♋", "♌", "♍", "♎", "♏", "♐", "🈚", "♒", "♓", "🆔",
                   "⚛"]

    def __init__(self, speler_lijst, message_text, channel, action_message="None"):
        self.action_message = action_message
        self.message_text = message_text + '\n'
        self.speler_lijst = speler_lijst  # Dit moet eigenlijk data heten
        self.channel = channel
        self.member_aantal = len(speler_lijst)
        self.vote = {}
        self.emoji_to_member_dict = {}
        self.member_to_emoji_dict = {}
        for speler, emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            self.member_to_emoji_dict[speler] = emoji
        for speler, emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            self.emoji_to_member_dict[emoji] = speler


    def add_vote(self,save,key):
        self.vote[save] = key
    async def send_message(self):
        # stuur de message
        # add reactions

        for speler, emoji in zip(self.speler_lijst, Vote.emoji_lijst):
            if isinstance(speler, Player):
                self.message_text += "{}    -   {}\n".format(emoji, speler.name)
            else:
                self.message_text += "{}    -   {}\n".format(emoji, speler)
        self.message = await self.channel.send(self.message_text)

        for speler in self.speler_lijst:
            await self.message.add_reaction(self.member_to_emoji_dict[speler])

    async def cupido(self, channel):
        geliefden = [self.emoji_to_member_dict[i.emoji] for i in self.vote] # maak tuple van dict
        await channel.set_permissions(target=geliefden[0].member, read_messages=True, send_messages=True)
        await channel.set_permissions(target=geliefden[1].member, read_messages=True, send_messages=True)

        geliefden[0].in_love = geliefden[1]  # zet elkaar in elkaars player class
        geliefden[1].in_love = geliefden[0]  # zet elkaar in elkaars players class
        await self.channel.send(
            "{} en {} zijn intens verlieft op elkaar geworden".format(geliefden[0].name, geliefden[1].name))
        return

    async def ziener(self, reaction):
        target = self.emoji_to_member_dict[reaction.emoji]
        await reaction.message.channel.send("{} is {}".format(target.name, target.rol_display_name))
        return target

    # dit zou in 1 kunnen
    async def normal_action(self, reaction):
        target = self.emoji_to_member_dict[reaction.emoji]
        if isinstance(target,Player):
            await reaction.message.channel.send(self.action_message.format(target.name))
        # goed we gaan er van uit dat als de target geen Player is dat is het het string momenteel is er een manier hoe er een string target zou kunnen komen en dat is de heks als er meer strings komen wat ik betwijfel kan je altijd meer dingen toevoegen
        else:
            await reaction.message.channel.send(self.action_message.format(target))
        return target

    def heks_leven(self, reaction):
        return self.emoji_to_member_dict[reaction.emoji]


class MyClient(discord.Client):
    # Dit is de custom bot class van de rewrite
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('----------------')
        print(self.guilds)
        self.init = False
        self.gameloop_currentrol = None

    def return_member(self,mention):
        mention = mention[2:len(mention)-1]
        if mention.isdigit():
            mention = int(mention)
        return self.server.get_member(mention)

    async def on_message(self, message):
        # dit triggert als er een message komt
        self.server = message.guild  # van welke server kwam de message
        self.bericht_text = message.content.split()  # split de bericht text

        if message.author != client.user:  # check of auteur niet bot is zodat je niet dood gespamt wordt
            self.bericht_text = message.content.split()

            # Add text channels
            if self.bericht_text[0] == "!init":
                self.join_message = False
                # if self.init == True:
                #     return
                # self.init = True
                self.weerwolfen_spel_rol = await self.server.create_role(name="spel Weerwolfen", mentionable=True)
                self.weerwolfen_category = await self.server.create_category("Weerwolfen")

                self.het_plein_channel = await self.server.create_text_channel("Het plein",
                                                                               category=self.weerwolfen_category)
                self.cupido_channel = await self.server.create_text_channel("Cupido", category=self.weerwolfen_category)
                self.ziener_channel = await self.server.create_text_channel("Ziener", category=self.weerwolfen_category)
                self.weerwolfen_channel = await self.server.create_text_channel("Weerwolfen",
                                                                                category=self.weerwolfen_category)
                self.heks_channel = await self.server.create_text_channel("Heks", category=self.weerwolfen_category)
                self.geliefde_channel = await self.server.create_text_channel("Geliefde chat",
                                                                              category=self.weerwolfen_category)
                self.jager_channel = await self.server.create_text_channel("Jager", category=self.weerwolfen_category)
                # voice
                self.dag_channel = await self.server.create_voice_channel("🌞 Dag", category=self.weerwolfen_category)
                self.nacht_channel = await self.server.create_voice_channel("🌙 Nacht",
                                                                            category=self.weerwolfen_category)

                self.channel_dict = {"Het plein:": self.het_plein_channel,
                                     "Cupido": self.cupido_channel,
                                     "Ziener": self.ziener_channel,
                                     "Weerwolf": self.weerwolfen_channel,
                                     "Heks": self.heks_channel,
                                     "Geliefde": self.geliefde_channel,
                                     "Jager": self.jager_channel,
                                     "Dag": self.dag_channel,
                                     "Nacht": self.nacht_channel}


                self.dood_rol = await self.server.create_role(name="Dood", mentionable=True)

                # set permissions op de channels
                for i in self.weerwolfen_category.channels:
                    await i.set_permissions(target=self.server.default_role, read_messages=False)
                await self.het_plein_channel.set_permissions(target=self.weerwolfen_spel_rol, send_messages=True,
                                                             read_messages=True)
                await self.dag_channel.set_permissions(target=self.weerwolfen_spel_rol, connect=False, speak=True,
                                                       use_voice_activation=True, read_messages=True)

            # Start commando
            print(message.content)
            if self.bericht_text[0] == "!start":
                self.player_lijst = []

                for member in self.weerwolfen_spel_rol.members:
                    self.player_lijst.append(Player(member))
                shuffle(self.player_lijst)
                self.players_levend_list = [i for i in self.player_lijst if i.levend]
                self.player_hoeveelheid = len(self.player_lijst)
                if self.player_hoeveelheid < 6:
                    await message.channel.send("Te weinig spelers doen mee.\nGeef meer leden de Weerwolf spel rol")
                    return

                self.rollen_lijst = await self.get_game_rollen(self.player_hoeveelheid)
                if len(self.rollen_lijst) == self.player_hoeveelheid:
                    for speler, rol in zip(self.player_lijst, self.rollen_lijst):
                        speler.rol = rol  # Doe rol object in de player class
                        await speler.member.add_roles(rol)  # Voeg rol toe aan member
                        speler.rol_display_name = rol.name  # Voeg display name toe aan member
                        await rol.edit(name=id_generator())  # Verander rol naam in random string
                        # await message.channel.send(str(speler))

                        if not speler.member.bot and self.bericht_text[1] != "no":  # Als speler niet bot stuur dan bericht met info
                            await speler.member.send(delete_after=30, embed=discord.Embed(
                                description="You are {}".format(speler.rol_display_name),
                                colour=discord.Colour(value=1412412)))

                    for i in self.player_lijst:
                        if i.rol_display_name == "Burger":
                            continue
                        await self.channel_dict[i.rol_display_name].set_permissions(target=i.rol, read_messages=True,
                                                                                    send_messages=True)
                        if i.rol_display_name == "Weerwolf":
                            await self.nacht_channel.set_permissions(target=i.rol, read_messages=True, connect=True,
                                                                     speak=True, use_voice_activation=True)


                    # Eerste nacht
                    self.gameloop_currentrol = "cupido"

                    # heks stuff
                    self.levendrankje = True
                    self.dooddrankje = True

                    self.dag = 1

                    await self.het_plein_channel.send("Het is nacht cupido wordt wakker en wijst 2 geliefde aan")
                    self.cupido_vote = Vote(message_text="Cupido wijst 2 gelefde aan", speler_lijst=self.player_lijst,
                                            channel=self.cupido_channel)
                    await self.cupido_vote.send_message()

                return

            # !Clean
            if self.bericht_text[0] == "!clean":
                await self.clean()


            #!vote

            if self.bericht_text[0] == "!stem" and message.channel.name == "het-plein" and self.gameloop_currentrol == "burgermeester":
                if len(self.bericht_text) == 1:
                    await message.delete()
                    return

                stem = self.return_member(mention=self.bericht_text[1])
                if message.author == stem:
                    await message.delete()
                    await self.het_plein_channel.send("{} Je kan niet op jezelf stemmen".formate(message.author.mention),delete_after=4)
                    return
                if not isinstance(stem,discord.Member):
                    await message.delete()
                    return
                if stem not in self.players_levend_list_members:
                    await message.channel.send("Je kan niet op iemand stemmen die dood is",delete_after=4)
                    await message.delete()
                    return
                self.stemming[message.author] = self.bericht_text[1] # Zet autor in de dict
                stemming_resultaat = {}
                for i in list(self.stemming.items()):                   # zet alle votes in de nieuwe dict tot 1
                    stemming_resultaat[i[1]] = 0
                for i in list(self.stemming.items()):                   # plus 1 voor elke keer dat vote voorkomt
                    stemming_resultaat[i[1]] += 1
                output = []
                for i in list(stemming_resultaat.items()):
                    if i[1] == 1:
                        output.append("{} stem voor {} ".format(i[1], i[0]))
                    else:
                        output.append("{} stemmen voor {} ".format(i[1], i[0]))
                    output.sort()
                await self.stemming_bericht.edit(
                    content="@here nu gaan we stemmen op wie burgermeester moet worden\n\nStemming:\n{}".format("\n".join(output)))
                if len(self.stemming) == 2: #self.players_levend:
                    hoogste = (None,-1)      # maak lege hoogste
                    for i in list(stemming_resultaat.items()):
                        if i[1] > hoogste[1]: # vergelijk de stemmen van die user met de hoogste stemmen
                            hoogste = i                 #evalutionaire algoritme??
                    if list(stemming_resultaat.values()).count(hoogste[1]) > 1: # als stemming meer and 1 keer voor komt
                        await self.stemming_bericht.edit(
                            content="@here nu gaan we stemmen op wie burgermeester moet worden\n\nStemming:\n{}\n\nHet staat momenteel gelijk".format("\n".join(output)))
                        await message.delete()
                        return
                    else:
                        winning_player = next((player for player in self.player_lijst if player.name == self.return_member(mention=hoogste[0]).name))
                        winning_player.burgermeester = True
                        self.burgermeester = winning_player.member
                        self.stemming = {}
                        self.gameloop_currentrol = "stemming"
                        await message.delete()
                        await self.stemming_bericht.delete()
                        await self.het_plein_channel.send(embed=discord.Embed(description="{} heeft gewonnen en is burgermeester".format(hoogste[0],colour=discord.Colour(value=2195054))))
                        self.stemming_bericht = await self.het_plein_channel.send("@here We gaan nu stemmen op de persoon die wordt vermoord\n\nStemming:")
                else:
                    await message.delete()

                        # nu moet de hele vote nog een keer voor wie er dood moet je boy stem
            if self.bericht_text[0] == "!stem" and message.channel.name == "het-plein" and self.gameloop_currentrol == "stemming":
                if len(self.bericht_text) == 1:
                    await message.delete()
                    return
                stem = self.return_member(mention=self.bericht_text[1])
                if message.author == stem:
                    await message.delete()
                    await self.het_plein_channel.send("{} Je kan niet op jezelf stemmen".format(message.author.mention),delete_after=4)
                    return
                if not isinstance(stem,discord.Member):
                    await message.delete()
                    return
                if stem not in self.players_levend_list_members:
                    await message.channel.send("Je kan niet op iemand stemmen die dood is",delete_after=4)
                    await message.delete()
                    return
                self.stemming[message.author] = self.bericht_text[1] # Zet autor in de dict
                stemming_resultaat = {}
                for i in list(self.stemming.items()):                   # zet alle votes in de nieuwe dict tot 1
                    stemming_resultaat[i[1]] = 0
                for i in list(self.stemming.items()):                   # plus 1 voor elke keer dat vote voorkomt
                    if i == self.burgermeester:                         # als burgermeester voeg 2 toe
                        stemming_resultaat[i[1]] += 2
                    else:
                        stemming_resultaat[i[1]] += 1
                output = []
                for i in list(stemming_resultaat.items()):
                    if i[1] == 1:
                        output.append("{} stem voor {} ".format(i[1], i[0]))
                    else:
                        output.append("{} stemmen voor {} ".format(i[1], i[0]))
                    output.sort()
                await self.stemming_bericht.edit(
                    content="@here We gaan nu stemmen op de persoon die wordt vermoord\n\nStemming:\n{}".format("\n".join(output)))
                if len(self.stemming) == 2: # Er is dus evenveel stemmen als de win condition
                    hoogste = (None,0)
                    for i in list(stemming_resultaat.items()):
                        if i[1] > hoogste[1]:
                            hoogste = i                 #evalutionaire algoritme??
                    if list(stemming_resultaat.values()).count(hoogste[1]) > 1: # als stemming meer and 1 keer voor komt
                        await self.stemming_bericht.edit(
                            content="@here We gaan nu stemmen op de persoon die wordt vermoord\n\nStemming:\n{}\n\nHet staat momenteel gelijk".format("\n".join(output)))
                        await message.delete()
                        return
                    else: # de stemming is goed gegaan dan gaat dit:
                        if await self.win_check():
                            return
                        await message.delete()
                        await self.stemming_bericht.delete()
                        winning_player = next((player for player in self.player_lijst if player.name == self.return_member(mention=hoogste[0]).name))
                        await self.het_plein_channel.send(embed=discord.Embed(
                            description="{} is gekozen en wordt vermoord\n{} was {}".format(hoogste[0],hoogste[0],winning_player.rol_display_name),
                                                                                 colour=discord.Colour(value=2195054)))
                        await winning_player.die(self.dood_rol)
                        self.players_levend_list = [i for i in self.player_lijst if i.levend]
                        self.players_levend_list_member = [i.member for i in self.player_lijst if i.levend]
                        if self.ziener_levend == True:
                            self.gameloop_currentrol = "ziener"
                            await self.het_plein_channel.send(
                                "De ziener wordt wakker en bekijkt iemands persoonlijkheid")
                            self.ziener_vote = Vote(message_text="Wie wil de ziener bekijken",
                                                    speler_lijst=self.players_levend_list,
                                                    channel=self.ziener_channel)
                            await self.ziener_vote.send_message()
                        else:
                            self.gameloop_currentrol = "weerwolfen"
                            await self.het_plein_channel.send(
                                "De weerwolfen worden wakker opzoek naar een midnight snack")
                            self.weerwolfen_vote = Vote(message_text="Wie gaan julie opeten",
                                                        speler_lijst=[speler for speler in self.player_lijst if
                                                                      speler.rol_display_name != "Weerwolf" and speler.levend == True],
                                                        channel=self.weerwolfen_channel)
                            await self.weerwolfen_vote.send_message()
                            self.killed = []
                else:
                    await message.delete()


            # !join all
            if self.bericht_text[0] == "!join" and len(self.bericht_text) == 1:
                if self.join_message:
                    await self.join_message.delete()
                self.join_message = await message.channel.send("**Join weerwolfen** {} \n{} wil een weerwolfen potje beginnen, click op de emoji om mee te doen".format(self.weerwolfen_spel_rol.mention,message.author.mention))
                await self.join_message.add_reaction("🐺")

            if self.bericht_text[0] == "!join" and self.bericht_text[1] == "all":
                for i in self.server.members:
                    await i.add_roles(self.weerwolfen_spel_rol)
                await message.channel.send("Done", delete_after=2)
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
                    if i.name[:4] == "spel" or i.name == "Dood":
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
                        hoeveel_messages = int(self.bericht_text[1]) + 1

                    await message.channel.purge(limit=hoeveel_messages)
                except ValueError:
                    await message.channel.send("Geen getal gegeven", delete_after=7)
                return
            if self.bericht_text[0] == "!tes":
                pass

    async def on_reaction_remove(self,reaction,user):
        if user == client.user:
            return
        if reaction.emoji == "🐺":
            self.react_channel = reaction.message.channel

            if reaction.message.content[:19] == "**Join weerwolfen**" and reaction.emoji == "🐺" and reaction.message.author.bot:
                await user.remove_roles(self.weerwolfen_spel_rol)

    async def on_reaction_add(self, reaction, user):

        if user == client.user:
            return

        self.react_channel = reaction.message.channel

        if reaction.message.content[:19] == "**Join weerwolfen**"and reaction.emoji == "🐺" and reaction.message.author.bot:
            await user.add_roles(self.weerwolfen_spel_rol)

        # cupido
        if self.react_channel.name == "cupido" and self.gameloop_currentrol == "cupido":

            self.cupido_vote.vote[reaction] = 1
            if len(self.cupido_vote.vote) == 2:  # look for 2 reactions and they should have a count of 2
                await self.cupido_vote.cupido(channel=self.geliefde_channel)
                del self.cupido_vote



                await reaction.message.delete()

                # we gaan nu naar ziener


                self.gameloop_currentrol = "ziener"
                await self.het_plein_channel.send("De ziener wordt wakker en bekijkt iemands persoonlijkheid")
                self.ziener_vote = Vote(message_text="Wie wil de ziener bekijken", speler_lijst=self.players_levend_list,
                                        channel=self.ziener_channel)
                await self.ziener_vote.send_message()



        # Ziener
        if self.react_channel.name == "ziener" and self.gameloop_currentrol == "ziener":
            print("go go go")
            await self.ziener_vote.ziener(reaction=reaction)
            del self.ziener_vote
            await reaction.message.delete()

            # we gaan nu over naar weerwolfen
            self.gameloop_currentrol = "weerwolf"
            await self.het_plein_channel.send("De weerwolfen worden wakker opzoek naar een midnight snack")
            self.weerwolfen_vote = Vote(message_text="Wie gaan julie opeten",
                                        speler_lijst=[speler for speler in self.players_levend_list if
                                                      speler.rol_display_name != "Weerwolf" and speler.levend == True],
                                        channel=self.weerwolfen_channel,action_message="{} is opgegeten")
            await self.weerwolfen_vote.send_message()
            self.killed = []

        # weerwolfen
        if self.react_channel.name == "weerwolfen" and self.gameloop_currentrol == "weerwolf":
            self.killed.append(await self.weerwolfen_vote.normal_action(reaction=reaction))
            del self.weerwolfen_vote
            await reaction.message.delete()

            # begin met Heks
            self.gameloop_currentrol = "heks"
            self.heks_response = 0

            if self.levendrankje == True or self.dooddrankje == True:
                await self.het_plein_channel.send("De heks wordt wakker")
                if self.levendrankje:
                    self.heks_leven_vote = Vote(
                        message_text="**Levensdrankje**\n{} is dood wil je hem/haar redden".format(self.killed[0].name),
                        speler_lijst=("Nee", "Ja"), channel=self.heks_channel)
                    await self.heks_leven_vote.send_message()
                else:
                    self.heks_response += 1
                if self.dooddrankje:
                    heks_lijst = [i for i in self.players_levend_list]
                    heks_lijst.append("**NIEMAND**")
                    self.heks_dood_vote = Vote(message_text="**Dodendrankje**\nWil je iemand vermoorden",
                                               speler_lijst=heks_lijst, channel=self.heks_channel,action_message="Je hebt {} vergiftigt")
                    await self.heks_dood_vote.send_message()
                else:
                    self.heks_response += 1
            else:
                await self.het_plein_channel.send("De heks kan niks meer doen")
                await self.switch_to_day()

        # Heks
        if self.react_channel.name == "heks" and self.gameloop_currentrol == "heks":
            if "Dodendrankje" in reaction.message.content:
                self.heks_response += 1
                gebruikt = await self.heks_dood_vote.normal_action(reaction=reaction)
                self.killed.append(gebruikt)
                del self.heks_dood_vote
                await reaction.message.delete()
                if gebruikt != "**NIEMAND**":
                    self.dooddrankje = False

            if "Levensdrankje" in reaction.message.content:
                self.heks_response += 1
                keuze = self.heks_leven_vote.heks_leven(reaction=reaction)
                del self.heks_leven_vote
                await reaction.message.delete()
                if keuze == "Ja":
                    await reaction.message.channel.send("Je hebt {} weer tot leven gewekt".format(self.killed[0].name))
                    self.killed.remove(self.killed[0])
                    self.levendrankje = False
                else:
                    return

            if self.heks_response == 2:
                # Ga naar dag
                try:
                    self.killed.remove("**NIEMAND**")
                except:
                    pass
                for speler in [i for i in self.killed]:
                    if speler.in_love:
                        await self.het_plein_channel.send(embed=discord.Embed(description="{} was instens verlieft op {} en pleegt zelfmoord".format(speler.in_love.name,speler.name),
                                colour=discord.Colour(value=16732324)))
                        self.killed.append(speler.in_love)

                if len(self.killed) > 1:
                    await reaction.message.channel.send(
                    "{} zijn gestorven deze nacht".format(" en ".join([str(speler.name) for speler in self.killed])))
                if len(self.killed) == 1:
                    await reaction.message.channel.send(
                    "{} is gestorven deze nacht".format("".join([str(speler.name) for speler in self.killed])))
                jager = [speler for speler in self.killed if speler.rol_display_name == "Jager"]
                if len(jager) == 1:
                    jager = jager[0]
                    self.gameloop_currentrol = "jager"
                    await self.het_plein_channel.send("{} is de jager hij kiest nu wie hij wil vermoorden".format(jager.name))
                    self.jager_vote = Vote(message_text="Wie wil je doodschieten",
                                           speler_lijst=[i for i in self.players_levend_list if i not in self.killed],
                                           channel=self.jager_channel,action_message="{} is doodgeschoten")
                    await self.jager_vote.send_message()
                else:
                    await self.switch_to_day()

        if self.react_channel.name == "jager" and self.gameloop_currentrol == "jager":
            self.killed.append(await self.jager_vote.normal_action(reaction=reaction))
            del self.jager_vote
            await reaction.message.delete()

            await self.switch_to_day()


    async def switch_to_day(self):
        if len(self.killed):
            for speler in self.killed:
                if speler.rol_display_name == "ziener":
                    self.ziener_levend = False
                else:
                    self.ziener_levend = True
                await speler.die(self.dood_rol)
            self.players_levend = len([speler for speler in self.player_lijst if speler.levend])
            self.players_levend_list_members =[speler.member for speler in self.player_lijst if speler.levend]
            self.players_levend_list =[speler for speler in self.player_lijst if speler.levend]

        # win check, zijn er alleen nog maar weerwolfen
        await self.win_check()

        if len(self.killed) > 1:
            await self.het_plein_channel.send("{} hebben de nacht niet overleeft".format(" en ".join([str(speler.name) for speler in self.killed])))
        elif len(self.killed) == 1:
            await self.het_plein_channel.send(
                "{} heeft de nacht niet overleeft".format(" en ".join([str(speler.name) for speler in self.killed])))
        else:
            await self.het_plein_channel.send("Iedereen heeft de nacht overleeft")

        for speler in self.killed:
            await self.het_plein_channel.send(embed=discord.Embed(description="{} was {}".format(speler.name,speler.rol_display_name),
                                colour=discord.Colour(value=2195054)))
        self.stemming = {}
        await self.het_plein_channel.send(embed=discord.Embed(
            description="Stem met !stem @naam",
            colour=discord.Colour(value=1412412))) # geef stem syntax
        if self.dag == 1:
            self.gameloop_currentrol = "burgermeester"
            self.stemming_bericht = await self.het_plein_channel.send("@here nu gaan we stemmen op wie burgermeester moet worden\n\nStemming:")
            self.dag += 1
        else:
            self.gameloop_currentrol = "stemming"
            self.stemming_bericht = await self.het_plein_channel.send("@here We gaan nu stemmen op de persoon die wordt vermoord\n\nStemming:")
            self.dag += 1

    def get_reaction_amount(self, reaction):
        count = 0
        emoji_count = len(reaction.message.reactions)  # Hoeveel emoji's zijn er
        for emoji in reaction.message.reactions:  # ga door alle reacties heen
            count += emoji.count
        count -= emoji_count  # hier hou je alleen de exstra reacties over
        return count

    async def get_game_rollen(self, player_hoeveelheid):
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

    async def clean(self):
        delete_lijst = []
        for i in self.server.roles:
            if i.name != "spel Weerwolfen":

                if i.name in ("Jager", "Weerwolf", "Cupido", "Ziener", "Heks", "Burger") or i.name[:4] == "spel":
                    delete_lijst.append(i)
        for i in delete_lijst:
            await i.delete()
        return

    async def win_check(self):
        weerwolf_win = True
        burger_win = True

        for player in self.players_levend_list:
            print(player.rol_display_name)
            if player.rol_display_name != "Weerwolf":
                weerwolf_win = False
            if player.rol_display_name == "Weerwolf":
                burger_win = False
        if weerwolf_win or burger_win:
            for channel in self.weerwolfen_category.channels:  # delete all channels
                if isinstance(channel, discord.TextChannel):
                    await channel.purge(after=channel.created_at)
            await self.clean()
            if weerwolf_win:
                await self.het_plein_channel.send("weewolfen hebben gewonnen")
            if burger_win:
                await self.het_plein_channel.send("Burgers hebben gewonnen")
            return True
        else:
            return False

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "spel" + ''.join(choice(chars) for _ in range(size))


client = MyClient()

client.run(load(open("config.json", "r"))["key"])

"to do https://trello.com/b/fEsaY7iA/weerwolfen"