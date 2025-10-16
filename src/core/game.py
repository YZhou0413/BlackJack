######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################
import sys

sys.path.append("../")

from PySide6.QtCore import Signal, QObject
from src.core.player import Player, Dealer
from src.core.cards import Card
import random
import src.core.login_panda as login_panda

# Dummy player used for initialization/testing
dummy_player = Player("dummy")


class Game(QObject):
    # Signals for UI updates and turn progression
    dealer_drawn_card = Signal()
    dealer_finished_turn = Signal()
    card_reveal_signal = Signal()
    test_player_draw_signal = Signal()
    fixed_start = Signal()

    gamer_stat = ["START", "WIN", "LOST", "BUST", "PUSH", "in-game"]

    def __init__(self, user):
        super().__init__()
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.dealer = Dealer()
        self.dealer.hand = []
        self.dealer.status = "START"
        self._dealer_is_busted = False

        self.player = user
        self.player.hand = []
        self.player.status = "START"
        self._player_is_busted = False

        self.bet = 100
        self.ai_play = False
        self.phase = 0

        self.initialize_game()

    # ------------------ Property methods ------------------

    @property
    def player_is_busted(self):
        return self._player_is_busted

    @player_is_busted.setter
    def player_is_busted(self, new_busted_state):
        if not self._player_is_busted and new_busted_state:
            self.card_reveal_signal.emit()
        self._player_is_busted = new_busted_state

    @property
    def dealer_is_busted(self):
        return self._dealer_is_busted

    # ------------------ Debug ------------------

    def test_hand(self, hand_owner, cardRank):
        hand_owner.hand.append(Card(cardRank, "hearts"))
        if type(hand_owner) is Dealer:
            self.dealer_drawn_card.emit()
        else:
            self.test_player_draw_signal.emit()

    # ------------------ Deck ------------------

    def create_deck(self):
        deck = []
        for s in Card.SUITS:
            for r in Card.RANKS:
                deck.append(Card(r, s))
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)
        
    def draw_card(self):
        if self.deck:
            return self.deck.pop()

    # ------------------ Game start/reset ------------------

    def reset_round(self):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.player.hand = []
        self.dealer.hand = []
        self.player.status = "START"
        self.dealer.status = "START"
        self.bet = 100
        self.phase = 0

    def initialize_game(self):
        self.reset_round()

    def start_game(self):
        self.deal_initial_hands(self.player)
        self.deal_initial_hands(self.dealer)
        self.fixed_start.emit()
        self.dealer.status = "in-game"
        self.player.status = "in-game"
        if self.ai_play:
            self.ai_plays()

    def deal_initial_hands(self, hand_owner):
        hand_owner.hand = [self.draw_card(), self.draw_card()]

    # ------------------ Place bets <phase 0> ------------------

    def place_bet(self):
        if self.player.score == 0:
            return
        self.player.score -= self.bet
        self.save_score()
        self.phase_up()
        self.start_game()

    def add_bet(self):
        if self.player.score > self.bet:
            self.bet += 100
        else:
            pass

    def minus_bet(self):
        if self.bet > 100:
            self.bet -= 100
        else:
            pass

    # ------------------ Player actions <phase 1> ------------------

    def btn_hit_on_click(self):
        if self.phase != 1:
            return

        self.player.hand.append(self.draw_card())

        if self.is_bust(self.player):
            self.player_is_busted = True
            self.phase_up()
            self.dealer_finished_turn.emit()
            self.phase_up()
            return

    def btn_stand_on_click(self):
        self.card_reveal_signal.emit()
        self.phase_up()

    # ------------------ Phase 2 Dealer ------------------

    def dealer_draw(self):
        if self.player.status == "BUST":
            self.dealer_finished_turn.emit()
            return

        if self.calculate_hand(self.dealer) > self.calculate_hand(self.player) and self.calculate_hand(self.dealer) > 11:
            self.dealer_finished_turn.emit()
        elif self.calculate_hand(self.dealer) < 17:
            new_card = self.draw_card()
            self.dealer.hand.append(new_card)
            self.dealer_drawn_card.emit()
            if self.is_bust(self.dealer):
                self.update_status(self.dealer, "BUST")
                self._dealer_is_busted = True
                self.dealer_finished_turn.emit()
        else:
            self.dealer_finished_turn.emit()

    # ------------------ AI Plays ------------------

    def toggle_ai(self):
        self.ai_play = (self.ai_play == False)
    
    def ai_play_step(self):
        if getattr(self.player, "status", "") != "in-game":
            return ("noop", None)

        p_score = self.calculate_hand(self.player)

        if p_score < 17:
            card = self.draw_card()
            self.player.hand.append(card)

            if self.is_bust(self.player):
                self.player_is_busted = True
                self.phase_up()
                return ("bust", card)
            return ("hit", card)
        else:
            return ("stand", None)

    # ------------------ Outcome ------------------

    def calculate_hand(self, hand_owner):
        score = 0
        aces = 0
        for c in hand_owner.hand:
            if c.rank == "A":
                score += 11
                aces += 1
            elif c.rank in ["J", "Q", "K"]:
                score += 10
            else:
                score += int(c.rank)

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def is_bust(self, hand_owner):
        if self.calculate_hand(hand_owner) > 21:
            self.update_status(hand_owner, "BUST")
            return True
        return False

    def phase_up(self):
        self.phase += 1

    def update_status(self, hand_owner, status):
        hand_owner.status = status
                
    def calc_winner(self):
        p_total = self.calculate_hand(self.player)
        d_total = self.calculate_hand(self.dealer)

        if p_total > 21:
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            self.save_score()
            return
        
        if d_total > 21:
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            self.save_score()
            return

        if p_total == d_total:
            self.update_status(self.player, "PUSH")
            self.update_status(self.dealer, "PUSH")
            self.player.score += self.bet
            self.save_score()
            return
        
        if p_total > d_total:
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            self.save_score()
            return
        else:
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            self.save_score()
            return

    # ------------------ Users ------------------

    def login_user(self, username, password):
        username = str(username).strip()
        if not username or not password:
            return False

        if login_panda.user_exists(username):
            if login_panda.verify_user(username, password):
                self.player.name = username
                self.player.password = password
                self.player.score = login_panda.get_score(username)
                return True
            return False

        if login_panda.create_user(username, password, start_score=1000):
            self.player.name = username
            self.player.password = password
            self.player.score = login_panda.get_score(username)
            return True
        return False

    def logout_user(self):
        if not getattr(self.player, "name", ""):
            return
        self.save_score()
        self.player.name = "dummy"

    def save_score(self):
        name = getattr(self.player, "name", "")
        if not name:
            return
        try:
            login_panda.set_score(name, int(self.player.score))
        except Exception:
            pass

    def load_all_scores(self):
        try:
            return login_panda.list_scores(as_df=False)
        except Exception:
            return {}


if __name__ == '__main__':
    game = Game(dummy_player)
