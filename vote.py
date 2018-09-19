from player import Player

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
            if isinstance(speler, player):
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
        if isinstance(target,player):
            await reaction.message.channel.send(self.action_message.format(target.name))
        # goed we gaan er van uit dat als de target geen Player is dat is het het string momenteel is er een manier hoe er een string target zou kunnen komen en dat is de heks als er meer strings komen wat ik betwijfel kan je altijd meer dingen toevoegen
        else:
            await reaction.message.channel.send(self.action_message.format(target))
        return target

    def heks_leven(self, reaction):
        return self.emoji_to_member_dict[reaction.emoji]