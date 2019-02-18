

def compute_answer(game, hand):
    game_rest = []
    hand_rest = []
    fullmatch = 0
    colormatch = 0

    for i, h in enumerate(hand):
        if game[i] == h:
            fullmatch += 1
        else:
            game_rest.append(game[i])
            hand_rest.append(h)

    for h in hand_rest:
        for i, _ in enumerate(game_rest):
            if h == game_rest[i]:
                colormatch += 1
                game_rest[i] = -1
                break

    return fullmatch, colormatch
