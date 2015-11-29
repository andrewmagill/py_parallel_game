import random

SUIT_MAP = {1:'clubs', 2:'diamonds', 3:'hearts', 4:'spades'}
RANK_MAP = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9',
        10:'j', 11:'q', 12:'k', 13:'a'}

NUM_ROUNDS = 3
NUM_PLAYERS = 3

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "\"{} {}\"".format(self.rank, self.suit)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Card):
            return other.rank == self.rank
        return NotImplemented # if trying to compare cards to oranges

class Deck(object):
    def __init__(self):
        self.cards = []
        for i in range(1,4):
            for j in range(2,14):
                suit = SUIT_MAP[i]
                rank = RANK_MAP[j]
                self.cards.append(Card(suit, rank))

    def remove_card(self):
        card = self.cards[0]
        self.cards.remove(card)
        return card

    def add_card(self, card):
        self.cards.append(card)

    def __getitem__(self, index):
        return self.cards[index]

    def __setitem__(self, index, value):
        self.cards[index] = value

    def __delitem__(self, index):
        self.cards.remove(self.cards[index])

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(self.cards)

class GameState(object):
    game_round = 0
    player_count = 0
    deck = None
    winners = []

    @classmethod
    def clear(cls):
        GameState.state = 1

    @classmethod
    def get_deck(cls):
        if not GameState.deck:
            GameState.deck = Deck()
        return GameState.deck

    @classmethod
    def set_deck(cls, deck):
        GameState.deck = deck

    @classmethod
    def winner(cls, player_number):
        record = (GameState.game_round, player_number)
        GameState.winners.append(record)
        print "\nWinner: Round {} winner is player {}".format(record[0], record[1])

class Anima(object):
    def __init__(self):
        pass

    def tell_me_your_state(self):
        print "class: {}, round: {}".format(self.__class__.__name__, GameState.game_round)

class Dealer(Anima):
    def __init__(self):
        pass

    def shuffle(self):
        deck = GameState.get_deck()
        random.shuffle(deck)
        GameState.set_deck(deck)
        print "\n{}: {}".format(self.__class__.__name__, "shuffle")
        print "\nDeck: {}".format(GameState.deck)

    def deal_card(self):
        card = GameState.get_deck().remove_card()
        print "{}: {} {}".format(self.__class__.__name__, "deals card", card)
        return card

class Player(Anima):
    def __init__(self):
        GameState.player_count += 1
        self.player_number = GameState.player_count
        self.cards = []

    def take_card(self, card):
        # print hand, beginning of round, just take card
        if len(self.cards) <= 0:
            self.cards.append(card)
            return

        # print hand
        print "\n{} {}: {} {}".format(self.__class__.__name__, self.player_number, "hand", self.cards)
        # print new card
        print "{} {}: {} {}".format(self.__class__.__name__, self.player_number, "draws", card)

        # check for match
        for old in self.cards:
            if old == card:
                return True # we have a winner

        # adds new card (if we didn't win)
        self.cards.append(card)

        # pick random card from hand
        rand_index = random.randint(0,len(self.cards)-1)
        discard_card = self.cards[rand_index]

        # discard random card from hand
        print "{} {}: {} {}".format(self.__class__.__name__, self.player_number, "discards", discard_card)
        self.cards.remove(discard_card)
        GameState.get_deck().add_card(discard_card)

        # print hand
        print "{} {}: {} {}".format(self.__class__.__name__, self.player_number, "hand", self.cards)

    def return_cards(self):
        for card in self.cards:
            self.cards.remove(card)
            GameState.get_deck().add_card(card)

    def tell_me_your_state(self):
        print "I'm player number {}: ".format(self.player_number),
        super(Player, self).tell_me_your_state()

class Game(object):
    def __init__(self):
        self.dealer = Dealer()
        self.players = []
        for i in range(NUM_PLAYERS):
            self.players.append(Player())

    def deal_cards(self):
        for player in self.players:
            card = self.dealer.deal_card()
            winner = player.take_card(card)

    def play_hand(self):
        game_round = GameState.game_round - 1 # because first round is 1, not 0
        for i in range(game_round, game_round+NUM_PLAYERS):
            player_index = i % NUM_PLAYERS
            player = self.players[player_index]
            card = GameState.get_deck().remove_card()
            winner = player.take_card(card)
            if winner:
                GameState.winner(player.player_number)
                break

    def return_cards(self):
        for player in self.players:
            player.return_cards()

    def play(self):
        print "\n#######  Begin Game  #######\n"
        GameState.clear()
        self.dealer.shuffle()
        for game_round in range(1,NUM_ROUNDS+1):
            GameState.game_round = game_round
            print "\n#######  Game Round: {}  #######\n".format(game_round)

            self.deal_cards()
            self.play_hand()
            self.return_cards()

            if game_round < NUM_ROUNDS:
                self.dealer.shuffle()

        if len(GameState.winners) > 0:
            print "\nWinners:\n"
            for record in GameState.winners:
                print "Player {} won round {}".format(record[0], record[1])
        else:
            print "\nThere were no winners!"

def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()
