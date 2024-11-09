import datetime
import json
import random
import disnake
from disnake.ext import commands

def GetCards():
    numbers = [2, 3, 4, 5, 6, 7, 8, 9] + [10] * 4  
    card = random.choice(numbers)
    return card

class MyView(disnake.ui.View):
    def __init__(self, initial_sum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_sum = initial_sum

    @disnake.ui.button(label="Hit", style=disnake.ButtonStyle.primary)
    async def hit_button_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        hit = GetCards()
        self.current_sum += hit
        if self.current_sum > 21:
            menu = disnake.Embed(
                title="♠ Blackjack ♠",
                description=f"You were dealt a {hit} (Total: {self.current_sum}) \n **You got a Bust**",
                color=0xFF0000,
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.edit_message(embed=menu, view=None)
        else:
            menu = disnake.Embed(
                title="♠ Blackjack ♠",
                description=f"You were dealt a {hit} **(Total: {self.current_sum})** \n Do you want to take another hit?",
                color=0xFFFFFF,
                timestamp=datetime.datetime.utcnow()
            )
            await interaction.response.edit_message(embed=menu, view=self)

    @disnake.ui.button(label="Stand", style=disnake.ButtonStyle.secondary)
    async def stand_button_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        dealer_cards = [GetCards(), GetCards()]
        dcards = sum(dealer_cards)
        while dcards < 17:
            dcard = GetCards()
            dealer_cards.append(dcard)
            dcards = sum(dealer_cards)
        
        if dcards > 21 or dcards < self.current_sum:
            menu = disnake.Embed(
                title="♠ Blackjack ♠",
                description=f"**You won with a total of {self.current_sum} 👑** \n Dealer got a Bust (Dealer Total: {dcards})",
                color=0x00FF00,
                timestamp=datetime.datetime.utcnow()
            )
        elif dcards > self.current_sum:
            menu = disnake.Embed(
                title="♠ Blackjack ♠",
                description=f"**The Dealer won with a total of {dcards} 👑** (Cards: {dealer_cards}) \n You chose to stand with a total of {self.current_sum}.",
                color=0xFF0000,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            menu = disnake.Embed(
                title="♠ Blackjack ♠",
                description=f"**It's a tie!** \n Both you and the dealer have a total of {self.current_sum}.",
                color=0xFFFF00,
                timestamp=datetime.datetime.utcnow()
            )
        await interaction.response.edit_message(embed=menu, view=None)

class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def blackjack(self, inter: disnake.ApplicationCommandInteraction, bet: int):
        if bet <= 0:
                await inter.send(f"{inter.author.mention}, please enter a positive bet.", ephemeral=True)
                return
        user_id = str(inter.author.id)
        with open("data/dollars.json", "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                    data = {}
                
            
            if user_id in data:
                user_dollars = data[user_id]
                if 100 > user_dollars:
                    await inter.send(f"You don't have enough dollars to play this Game. You need 100 Dollars to unlock Blackjack!", ephemeral=True)
                    return
                if bet > user_dollars:
                    await inter.send(f"You don't have enough dollars to make this bet.", ephemeral=True)
                    return
            else:
                await inter.send(f"You don't have enough dollars to make this bet.", ephemeral=True)
        card1 = GetCards()
        card2 = GetCards()
        initial_sum = card1 + card2
        view = MyView(initial_sum)
        menu = disnake.Embed(
            title="♠ Blackjack ♠",
            description=f"You were dealt a {card1} and a {card2} **(Total: {initial_sum})**\n Do you want to take another hit?",
            color=0xFFFFFF,
            timestamp=datetime.datetime.utcnow()
        )
        await inter.response.send_message(embed=menu, view=view)
        

def setup(bot):
    bot.add_cog(BlackjackCog(bot))
