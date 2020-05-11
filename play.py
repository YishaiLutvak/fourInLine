import game

board=game.game()
game.create(board)
print("Initial Game")
game.printState(board)
game.decideWhoIsFirst(board)
while not game.isFinished(board):
    print("continue game")
    score = 0
    if game.isHumTurn(board):
        game.inputMove(board)

    else:
        score,board= game.inputComputer(board)
    game.printState(board)
    print(f"score: {score}")

print("Game Over:")
