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
