import random

class BlackJack():

    def __init__(self):
        self.player_input = None
        self.game_output = None
        self.game_con = 'undetermined'
        self.game_state = ''
        self.deck: list[int] = []
        self.dealer_hand: list[int] = []
        self.player_hand: list[int] = []


    @staticmethod
    def generate_deck():
        """
        using a flat list allow me to use random shuffle and pop() with ease
        """
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

        return deck

    def game_start(self):

        """
        a method to initialize game state
        this is only necessary because it is the only 'unique' round
        every turn aside from the beginning plays exactly the same
        aside from what cards you have in your hand
        the start is the only round in the game where you draw 2 cards
        """
        self.set_game_state()
        self.deck = self.generate_deck()
        random.shuffle(self.deck)
        deck = self.deck
        self.dealer_hand = [deck.pop()]
        self.player_hand = [deck.pop() for i in range(2)]
        self.deck = deck
        self.check_win()
        self.set_game_state()
        self.game_output = {'dealer' : self.dealer_hand, 'player' : self.player_hand, 'state' : self.game_state}
        return self.game_output

    def turn(self, player_input):

        """
        checks the player input attribute if it's a 1 or
        0 which the turn method treats as a bool
        this is useful because we can determine what action to take
        in 2 very small if statements

        this is the heart of game logic just progress's game state
        by one turn and calls necessary methods and sets
        the right attributes to do so

        we add to the dealers deck if below 17 because that's the risk
        threshold most casinos
        """
        self.player_input = player_input
        deck = self.deck

        if self.player_input:
            self.player_hand.append(deck.pop())

        if sum(self.dealer_hand) < 17:
            self.dealer_hand.append(deck.pop())


        self.deck = deck
        self.check_win()
        self.set_game_state()
        self.game_output = {'dealer': self.dealer_hand, 'player': self.player_hand, 'state': self.game_state}
        return self.game_output

    def check_win(self):

        """
        sets the game condition based on the sum of the player
        it's just a set of if else statements the same steps
        a dealer would take after each round to determine a win
        or loss
        """
        player_score = self.hand_sum(self.player_hand)
        dealer_score = self.hand_sum(self.dealer_hand)

        if player_score > 21:
            self.game_con = 'lose'
        elif player_score < 21 and dealer_score < 17:
            self.game_con = 'undetermined'
        elif player_score < dealer_score <= 21:
            self.game_con = 'lose'
        elif player_score == 21 and dealer_score == 21:
            self.game_con = 'draw'
        else:
            self.game_con = 'win'

    def hand_sum(self, hand):
        """calculates sum prevents repeat code from having to refer
        to this same snippet multiple times in the code

        there is a small bit of extra logic to handle 1's or 'aces' because in black jack
        when you acquire and ace the value of the ace changes depending on whether you will bust with
        1 sum vs the other this additional logic is needed
        """
        score = sum(hand)
        if 1 in hand and score + 10 <= 21:
            score += 10
        return score

    def set_game_state(self):
        """
        it does 1 thing set game state to either ongoing or end
        required to simplify game flow the specfics don't matter
        when the next match is in limbo this is the only way
        the discord client bot knows when to progress to the end screen
        """
        if self.game_con == 'undetermined':
            self.game_state = 'ongoing'
        else:
            self.game_state = 'end'