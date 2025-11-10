# 7-bag randomizer

import random
from cetragm.tables import pieces

PIECE_BAG = list(pieces.keys())

class Bag:
    def __init__(self, preview_size: int = 5):
        self.preview_size = preview_size
        self.current_bag = random.sample(PIECE_BAG, len(PIECE_BAG))
        self.next_bag = random.sample(PIECE_BAG, len(PIECE_BAG))
    
    def get_piece(self):
        piece = self.current_bag.pop(0)
        if not self.current_bag:
            self.current_bag = self.next_bag
            self.next_bag = random.sample(PIECE_BAG, len(PIECE_BAG))
        return piece
    
    def get_preview(self):
        upcoming = self.current_bag + self.next_bag
        return upcoming[:self.preview_size]
    