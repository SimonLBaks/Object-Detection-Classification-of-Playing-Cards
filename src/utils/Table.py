# Initialize dictionary of card deck and values
card_deck = {
    'Ac': 36, '2c': 4, '3c': 8, '4c': 12, '5c': 16, '6c': 20, '7c': 24, '8c': 28, '9c': 32, '10c': 0, 'Jc': 40, 'Qc': 48, 'Kc': 44,
    'Ad': 37, '2d': 5, '3d': 9, '4d': 13, '5d': 17, '6d': 21, '7d': 25, '8d': 29, '9d': 33, '10d': 1, 'Jd': 41, 'Qd': 49, 'Kd': 45,
    'Ah': 38, '2h': 6, '3h': 10, '4h': 14, '5h': 18, '6h': 22, '7h': 26, '8h': 30, '9h': 34, '10h': 2, 'Jh': 42, 'Qh': 50, 'Kh': 46,
    'As': 39, '2s': 7, '3s': 11, '4s': 15, '5s': 19, '6s': 23, '7s': 27, '8s': 31, '9s': 35, '10s': 3, 'Js': 43, 'Qs': 51, 'Ks': 47,
    }

card_values = {
    'Ac': 10, '2c': 2, '3c': 3, '4c': 4, '5c': 5, '6c': 6, '7c': 7, '8c': 8, '9c': 9, '10c': 10, 'Jc': 10, 'Qc': 10, 'Kc': 10,
    'Ad': 10, '2d': 2, '3d': 3, '4d': 4, '5d': 5, '6d': 6, '7d': 7, '8d': 8, '9d': 9, '10d': 10, 'Jd': 10, 'Qd': 10, 'Kd': 10,
    'Ah': 10, '2h': 2, '3h': 3, '4h': 4, '5h': 5, '6h': 6, '7h': 7, '8h': 8, '9h': 9, '10h': 10, 'Jh': 10, 'Qh': 10, 'Kh': 10,
    'As': 10, '2s': 2, '3s': 3, '4s': 4, '5s': 5, '6s': 6, '7s': 7, '8s': 8, '9s': 9, '10s': 10, 'Js': 10, 'Qs': 10, 'Ks': 10,
}

# Two getters for card string and value
def get_card_string(card_value):
    return {v: k for k, v in card_deck.items()}.get(card_value, None)

def get_card_value(card_string):
    return card_values.get(card_string, None)
