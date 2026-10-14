import os
import game_logic
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands, guild, Embed

load_dotenv()

OWNER = os.getenv('SUPA_SECRET_OWNER')
TOKEN = os.getenv('SUPA_SECRET_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot: commands.Bot = commands.Bot(command_prefix='!', intents=intents)

class GamesView(discord.ui.View):
    """imports from discord.ui.View class is necessary to pass interaction.message in order to render buttons
    this one is for choosing a specific game
    """
    @discord.ui.button(label='Black Jack', style=discord.ButtonStyle.blurple, emoji='♣️')
    async def blackjackbutton(self, interaction: discord.Interaction, button: discord.ui.Button,):
        blackjack = game_logic.BlackJack()
        output = blackjack.game_start()
        dealer_hand = output['dealer']
        player_hand = output['player']
        state = output['state']
        Embed = em_gen(title='Black Jack',
                       color=discord.Color.green(),
                       fields=[("Dealer's hand", dealer_hand, True),
                               ("Player's hand", player_hand, True)
                               ])
        try:
            await interaction.response.defer()
            await interaction.edit_original_response(embed=Embed, view=BlackJackView(interaction, blackjack=blackjack))
        except Exception as e:
            print(e)

class BlackJackView(discord.ui.View):
    """imports from discord.ui.View class is necessary to pass interaction.message in order to render buttons
    this one is for blackjack buttons
    """

    def __init__(self, interaction: discord.Interaction, blackjack: game_logic.BlackJack):

        super().__init__()

        self.blackjack = blackjack

    @discord.ui.button(label='Hit', style=discord.ButtonStyle.blurple)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):

        """will progress the game with 1 being passed into turn in order
        to add a card to player deck, grab output, and edit the original response in case of game end
        """
        try:
            blackjack = self.blackjack
            output = blackjack.turn(1)
            dealer_hand = output['dealer']
            player_hand = output['player']
            state = output['state']
            if state == "end":
                await interaction.response.defer()
                await interaction.edit_original_response(embed=game_over_embed_gen(blackjack.game_con, [dealer_hand, player_hand]), view=GameOverView())
            Embed = em_gen(title='Black Jack',
                        color=discord.Color.green(),
                        fields=[("Dealer's hand", dealer_hand, True),
                                ("Player's hand", player_hand, True)
                                ])
            await interaction.response.defer()
            await interaction.edit_original_response(embed=Embed)
        except Exception as e:
            print(e)

    @discord.ui.button(label='Stay', style=discord.ButtonStyle.blurple)
    async def stay(self, interaction: discord.Interaction, button: discord.ui.Button):
        """will progress the game with 0 being passed into turn in order
        to keep player deck as is until someone has one, grab output, and edit the original response.
        """
        try:
            blackjack = self.blackjack
            while blackjack.game_state != "end":
                output = blackjack.turn(0)
            dealer_hand = output['dealer']
            player_hand = output['player']
            await interaction.response.defer()
            await interaction.edit_original_response(
                embed=game_over_embed_gen(blackjack.game_con, [dealer_hand, player_hand]), view=GameOverView())

        except Exception as e:
            print(e)

class GameOverView(discord.ui.View):
    """imports from discord.ui.View class is necessary to pass interaction.message in order to render buttons
    this one is for game over screen buttons
    """

    @discord.ui.button(label='Again!', style=discord.ButtonStyle.blurple)
    async def again(self, interaction: discord.Interaction, button: discord.ui.Button):
        blackjack = game_logic.BlackJack()
        output = blackjack.game_start()
        dealer_hand = output['dealer']
        player_hand = output['player']
        state = output['state']
        Embed = em_gen(title='Black Jack',
                       color=discord.Color.green(),
                       fields=[("Dealer's hand", dealer_hand, True),
                               ("Player's hand", player_hand, True)
                               ])
        try:
            await interaction.response.defer()
            await interaction.edit_original_response(embed=Embed, view=BlackJackView(interaction, blackjack=blackjack))
        except Exception as e:
            print(e)


    @discord.ui.button(label='Cut ur losses!', style=discord.ButtonStyle.blurple)
    async def nah(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = em_gen(title='Main Screen', color=discord.Color.green(),
                           fields=('SELECT YOUR GAME', '♣️♣️♣️♣️♣️', True))
            await interaction.response.send_message(embed=embed, view=GamesView(), ephemeral=True)
        except discord.Forbidden as e:
            print(e)
        except Exception as e:
            print(f"{e}")

def game_over_embed_gen(wl, final_hand):
    """was needed as mutiple different games can refer to the same gen later if I add them"""
    if wl == 'win':
        Embed = em_gen(title='Black Jack',
                   color=discord.Color.green(),
                   fields=[("Luck seems to be on your side", '', True),
                           ("Good stuff", final_hand, True),
                           ("Try again?", '', False)
                           ])
        return Embed
    elif wl == 'draw':
        Embed = em_gen(title='Black Jack',
                       color=discord.Color.green(),
                       fields=[("Could've gone worse could've gone better", '', True),
                               ("You walk away unscathed", final_hand, True),
                               ("Try again?", '', False)
                               ])
        return Embed
    else:
        Embed = em_gen(title='Black Jack',
                       color=discord.Color.green(),
                       fields=[("Can't end it on a loss! Come on!", '', True),
                               ("You sure you want to see this?", final_hand, True),
                               ("Try again?", '', False)
                               ])
        return Embed

def em_gen(title: str,
           color: object|int,
           fields: list[tuple[str, str, bool]] | tuple[str, str, bool]) -> discord.Embed:
    """
    I just wanted this to avoid boilerplater code in other area's of my code the only thing
    it really does to help remove clutter and improve readability is add fields depending on how many fields you
    give it which is handy because otherwise we would have to repeat embed.add_field() everytime we wanted to add an
    element
    """

    try:
        embed = discord.Embed(title=title, color=color)
        if isinstance(fields, tuple):
            embed = embed.add_field(name=fields[0], value=fields[1], inline=fields[2])
        else:
            for i in fields:
                embed = embed.add_field(name=i[0], value=i[1], inline=i[2])

        return embed
    except Exception as e:
        print(f"embed generator function broke sound the alarm \n {e}")
        return discord.Embed(title='Critical error contact developers!')



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.tree.command(name='main-screen', description='It\'s just the main screen....')
async def mainscreen(interaction: discord.Interaction):
    """serves you the main screen of the bot pending your choice of game """
    try:
        embed = em_gen(title='Main Screen', color=discord.Color.green(), fields=('SELECT YOUR GAME', '♣️♣️♣️♣️♣️', True))
        await interaction.response.send_message(embed=embed, view=GamesView(), ephemeral=True)
    except discord.Forbidden as e:
        print(e)
    except Exception as e:
        print(f"{e}")




@bot.tree.command()
async def sync(ctx):
    owner_userid = OWNER
    """in case of updates to the bot this function is necessary in order to sync the bot tree slash commands
    whenever a new one is added without this the new commands won't appear in the slash path
    """
    print("sync command")
    if ctx.author.id == owner_userid:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

if __name__ == '__main__':

    try:
        bot.run(TOKEN)
    except discord.Forbidden:
        print(discord.Forbidden)
    except Exception as e:
        print(e)