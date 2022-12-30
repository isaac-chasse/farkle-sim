import random
from typing import Optional, List, Tuple


def filter_tuples(tuples):
    filtered_tuples = []
    for t in tuples: 
        if t[0]:    # Check if the first element of the tuple is True
            filtered_tuples.append(t)
    return filtered_tuples


def flatten_list(lst):
    flat_list = []
    for sublist in lst:
        for item in sublist:
            flat_list.append(item)
    return flat_list


class Dice:
    def __init__(self, sides: Optional[int]=6) -> None:
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class Farkle:
    """Scoring methods: 
    1: 100 points
    5: 50 points
    Three 1's: 300 points
    Three 2's: 200 points
    Three 3's: 300 points
    Three 4's: 400 points
    Three 4's: 500 points
    Three 4's: 600 points
    Four of a kind: 1000 points 
    Three pairs: 1500 points
    1-6 straight: 1500 points
    Five of a kind: 2000 points
    Two triples: 2500 points
    Six of a kind: 3000 points
    """
    def __init__(self) -> None:
        pass

    def is_straight(self, arr: List[int]):
        """Straight 1-6"""
        return (arr == [1, 2, 3, 4, 5, 6], 1500, 6)

    def is_six_of_anything(self, arr: List[int]):
        """Six of a kind"""
        return (arr.count(arr[0]) == 6, 3000, 6)

    def is_five_of_anything(self, arr: List[int]):
        """Five of a kind"""
        return (any(arr.count(uniq) == 5 for uniq in set(arr)), 2000, 1)

    def is_four_of_anything(self, arr: List[int]):
        """Four of a kind"""
        return (any(arr.count(uniq) == 4 for uniq in set(arr)), 1000, 2)

    def is_three_of_anything(self, arr: List[int]):
        """Three of a kind. Strictly three occurences, does not consider two triplets"""
        occurences = []
        for uniq in set(arr):
            occurences.append((arr.count(uniq) == 3, uniq * 100, 3))    
        true_occurences = filter_tuples(occurences)
        if len(true_occurences) == 1:
            return tuple(flatten_list(true_occurences))
        else:
            return (False, 0)

    def is_double_triple(self, arr: List[int]):
        """Two occurences of three of a kind"""
        return (all(arr.count(uniq) == 3 for uniq in set(arr)), 2500, 6)

    def is_triple_double(self, arr: List[int]):
        """Three occurences of two of a kind"""
        return (all(arr.count(uniq) == 2 for uniq in set(arr)), 1500, 6)

    def is_containing_one(self, arr: List[int]):
        """Roll containing at least one One TODO: implement a 'put at least one away' scoring"""
        return (arr.count(1) >= 1, arr.count(1) * 100, 6-arr.count(1))

    def is_containing_five(self, arr: List[int]):
        """Roll containing at least one Five TODO: implement a 'put at least one away' scoring"""
        return (arr.count(5) >= 1, arr.count(5) * 50, 6-arr.count(5))

    def verbose_scoring(self, arr: List[int]):
        """Runs a match-case for relevant scoring based on num_die. Reduces runtime"""
        match len(arr):
            case 0:
                return False
            case 1 | 2:
                return [
                    self.is_containing_five(arr), 
                    self.is_containing_one(arr)
                ]
            case 3:
                return [
                    self.is_containing_five(arr), 
                    self.is_containing_one(arr), 
                    self.is_three_of_anything(arr)
                ]
            case 4:
                return [
                    self.is_containing_five(arr), 
                    self.is_containing_one(arr), 
                    self.is_three_of_anything(arr),
                    self.is_four_of_anything(arr)
                ]
            case 5:
                return [
                    self.is_containing_five(arr), 
                    self.is_containing_one(arr), 
                    self.is_three_of_anything(arr),
                    self.is_four_of_anything(arr),
                    self.is_five_of_anything(arr)
                ]
            case 6:
                return [
                    self.is_containing_five(arr), 
                    self.is_containing_one(arr), 
                    self.is_three_of_anything(arr),
                    self.is_four_of_anything(arr),
                    self.is_five_of_anything(arr),
                    self.is_triple_double(arr),
                    self.is_double_triple(arr),
                    self.is_six_of_anything(arr),
                    self.is_straight(arr)
                ]
            case _:
                return ValueError

    def score(self, rolled):
        possible_outcomes = filter_tuples(self.verbose_scoring(rolled))
        return possible_outcomes
            

class Player:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.turn_counter = 0
        self.roll_history = []
        self.score_history = []

    def greedy_strategy(self, rolled_scores: List[Tuple[bool, int]]):
        score = max(rolled_scores, key=lambda val: val[1])
        return score

    def roll_die(self, turn_score: Optional[int]=0, num_die: Optional[int]=6):
        # if turn_score <= 500:
        #     self.roll_die(turn_score, num_die)
        die_in_hand = [Dice() for _ in range(num_die)]
        rolls = sorted([dice.roll() for dice in die_in_hand])
        scores = Farkle().score(rolls)

        match self.strategy:
            case "greedy":
                _, score, num_die = self.greedy_strategy(scores)
                turn_score += score
        return rolls, turn_score