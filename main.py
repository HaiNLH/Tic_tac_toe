import time
class Board():
    def __init__(self):
        self.player= ['x','o']
        self.empty_sq = '.'
        self.size = 7
        self.current_player = 'x'
        #make it unchangeable
        self.winScore = 10000000
        self.board = [[self.empty_sq for j in range(self.size)] for i in range(self.size)]

    def print_board(self):
        for row in range(self.size):
            for col in range(self.size):
                print(self.board[row][col], end='|')
            print()
        print()

    def print_move(self, moves):
        print('Making moves: X = {}, y = {}'.format(moves[0] + 1, moves[1] + 1))
    def calcNextMove(self, depth):
        #applying threat space search to get the best move first then using ABminmax
        board = self.get_matrix_board()
        bestMove = self.searchWinningMove(board) #optimal strat to win
        badMove = self.searchLoseMove(board) #strat to get defense

        move = [0, 0]
        if bestMove[1] is not None and bestMove[2] is not None:
            move[0] = bestMove[1]
            move[1] = bestMove[2]
            print('Best move')
            return move
        if badMove[1] is not None and badMove[2] is not None:
            move[0] = badMove[1]
            move[1] = badMove[2]
            print('Def move')
            return move
        else:
            bestMove = self.minimaxSearchAB(depth, board, True, -1.0, self.winScore)
            if bestMove[1] is None:
                move = None
            else:
                move[0] = bestMove[1]
                move[1] = bestMove[2]
            print('AB move')
            return move

    def playNextMove(self, board, move, isUserTurn): #get nextmove matrix
        i, j = move[0], move[1]
        row, col = len(board), len(board[0])
        newBoard = [[0] * col for _ in range(row)]
        for h in range(row):
            for k in range(col):
                newBoard[h][k] = board[h][k]
        newBoard[i][j] = 2 if isUserTurn else 1
        return newBoard

    #search for possible winning move based on evaluation winning score
    def searchWinningMove(self, matrix):
        allPossibleMoves = self.generateMoves(matrix)
        winningMove = [None, None, None]

        for move in allPossibleMoves:
            dummyBoard = self.playNextMove(matrix, move, False)

            if self.getScore(dummyBoard, False, False) >= self.winScore:
                winningMove[1] = move[0]
                winningMove[2] = move[1]
                return winningMove

        return winningMove

    def searchLoseMove(self, matrix):
        allPossibleMoves = self.generateMoves(matrix)
        print(len(allPossibleMoves))

        losingMove = [None, None, None]

        for move in allPossibleMoves:
            dummyBoard = self.playNextMove(matrix, move, True)

            # If the black player has a winning score in that temporary board, return the move.
            if self.getScore(dummyBoard, True, False) >= self.winScore:
                losingMove[1] = move[0]
                losingMove[2] = move[1]
                return losingMove

        return losingMove

    def minimaxSearchAB(self, depth, board, max_player, alpha, beta):
        if depth == 0:
            return [self.evaluateBoardForWhite(board, not max_player), None, None]

        allPossibleMoves = self.generateMoves(board)

        if len(allPossibleMoves) == 0:
            return [self.evaluateBoardForWhite(board, not max_player), None, None]

        bestMove = [None, None, None]

        if max_player:
            bestMove[0] = -100000000

            for move in allPossibleMoves:
                # Play current move
                dummyBoard = self.playNextMove(board, move, False)

                tempMove = self.minimaxSearchAB(depth - 1, dummyBoard, not max_player, alpha, beta)

                # Update alpha
                if tempMove[0] > alpha:
                    alpha = tempMove[0]
                # Beta pruning
                if tempMove[0] >= beta:
                    return tempMove
                if tempMove[0] > bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]

        else:
            bestMove[0] = 100000000.0
            bestMove[1] = allPossibleMoves[0][0]
            bestMove[2] = allPossibleMoves[0][1]

            for move in allPossibleMoves:
                dummyBoard = self.playNextMove(board, move, True)

                tempMove = self.minimaxSearchAB(depth - 1, dummyBoard, not max_player, alpha, beta)

                # Update beta
                if tempMove[0] < beta:
                    beta = tempMove[0]
                # Alpha pruning
                if tempMove[0] <= alpha:
                    return tempMove
                if tempMove[0] < bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]

        return bestMove

    def evaluateBoardForWhite(self, board, userTurn): #GET EVALUATION RATIO X winning/ O winning white
        blackScore = self.getScore(board, True, userTurn)
        whiteScore = self.getScore(board, False, userTurn)

        if blackScore == 0:
            blackScore = 1.0

        return whiteScore / blackScore

    def generateMoves(self, boardMatrix): #Creating domain knowledge for AI
        moveList = []

        # Tìm những tất cả những ô trống nhưng có đánh XO liền kề
        for i in range(self.size):
            for j in range(self.size):
                if boardMatrix[i][j] > 0:
                    continue
                if i > 0:
                    if j > 0:
                        if boardMatrix[i - 1][j - 1] > 0 or boardMatrix[i][j - 1] > 0:
                            move = [i, j]
                            moveList.append(move)
                            continue
                    if j < self.size - 1:
                        if boardMatrix[i - 1][j + 1] > 0 or boardMatrix[i][j + 1] > 0:
                            move = [i, j]
                            moveList.append(move)
                            continue
                    if boardMatrix[i - 1][j] > 0:
                        move = [i, j]
                        moveList.append(move)
                        continue
                if i < self.size - 1:
                    if j > 0:
                        if boardMatrix[i + 1][j - 1] > 0 or boardMatrix[i][j - 1] > 0:
                            move = [i, j]
                            moveList.append(move)
                            continue
                    if j < self.size - 1:
                        if boardMatrix[i + 1][j + 1] > 0 or boardMatrix[i][j + 1] > 0:
                            move = [i, j]
                            moveList.append(move)
                            continue
                    if boardMatrix[i + 1][j] > 0:
                        move = [i, j]
                        moveList.append(move)
                        continue
        return moveList



    def getScore(self, board, forX, blacksTurn):
        return self.evaluateHorizontal(board, forX, blacksTurn) + \
            self.evaluateVertical(board, forX, blacksTurn) + \
            self.evaluateDiagonal(board, forX, blacksTurn)

    def evaluateHorizontal(self, boardMatrix, forX, playersTurn):
        consecutive = 0
        blocks = 2
        score = 0

        for i in range(len(boardMatrix)):
            for j in range(len(boardMatrix[0])):
                if boardMatrix[i][j] == (2 if forX else 1):
                    # 2. Đếm...
                    consecutive += 1
                # gặp ô trống
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        # Ra: Ô trống ở cuối sau khi đếm. Giảm block rồi bắt đầu tính điểm sau đó reset lại ban đầu
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        # 1. Vào reset lại blocks = 1 rồi bắt đầu đếm
                        blocks = 1
                # gặp quân địch
                elif consecutive > 0:
                    # 2.Ra:  Ô bị chặn sau khi đếm. Tính điểm sau đó reset lại.
                    score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    # 1. Vào: reset lại blocks = 2 rồi bắt đầu đếm
                    blocks = 2

            # 3. Ra: nhưng lúc này đang ở cuối. Nếu liên tục thì vẫn tính cho đến hết dòng
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)

            # reset lại để tiếp tục chạy cho dòng tiếp theo
            consecutive = 0
            blocks = 2

        return score

    def evaluateVertical(self, boardMatrix, forX, playersTurn):
        consecutive = 0
        blocks = 2
        score = 0

        for j in range(len(boardMatrix[0])):
            for i in range(len(boardMatrix)):
                if boardMatrix[i][j] == (2 if forX else 1):
                    consecutive += 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
            consecutive = 0
            blocks = 2

        return score

    def evaluateDiagonal(self, boardMatrix, forX, playersTurn):
        consecutive = 0
        blocks = 2
        score = 0
        # Diagonal /
        for k in range(0, 2 * (len(boardMatrix) - 1) + 1):
            iStart = max(0, k - len(boardMatrix) + 1)
            iEnd = min(len(boardMatrix) - 1, k)
            for i in range(iStart, iEnd + 1):
                j = k - i
                if boardMatrix[i][j] == (2 if forX else 1):
                    consecutive += 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
            consecutive = 0
            blocks = 2

        # Diagonal \
        for k in range(1 - len(boardMatrix), len(boardMatrix)):
            iStart = max(0, k)
            iEnd = min(len(boardMatrix) + k - 1, len(boardMatrix) - 1)
            for i in range(iStart, iEnd + 1):
                j = i - k

                if boardMatrix[i][j] == (2 if forX else 1):
                    consecutive += 1
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, forX == playersTurn)
            consecutive = 0
            blocks = 2

        return score

    def getConsecutiveSetScore(self, count, blocks, currentTurn):
        winGuarantee = 1000000
        if blocks == 2 and count <= 5:
            return 0
        if count == 5:
            return self.winScore
        elif count == 4:
            if currentTurn:
                return winGuarantee
            else:
                if blocks == 0:
                    return winGuarantee // 4
                else:
                    return 200
        elif count == 3:
            if blocks == 0:
                if currentTurn:
                    return 50000
                else:
                    return 200
            else:
                if currentTurn:
                    return 10
                else:
                    return 5
        elif count == 2:
            if blocks == 0:
                if currentTurn:
                    return 7
                else:
                    return 5
            else:
                return 3
        elif count == 1:
            return 1
        return self.winScore * 2
    def game_loop(self):
        #print(self)
        self.print_board()
        while True:
            if self.current_player == 'x':
                user_input = input('> ')

                if user_input == 'exit': break

                if user_input == '': continue

                row = int(user_input.split(' ')[0]) - 1
                col = int(user_input.split(' ')[1]) - 1

                if self.is_valid(row, col):
                    move = [row, col]
                    self.print_move(move)
                    self.board[row][col] = 'x'
                    self.current_player = 'o'
                    self.print_board()
                    if self.getWinner():
                        break
                    continue
                else:
                    print('Invalid move: try again!')
                    continue
            if self.current_player == 'o':
                nextMoveX = 0
                nextMoveY = 0
                bestMove = self.calcNextMove(1)
                if bestMove is not None:
                    nextMoveX = bestMove[0]
                    nextMoveY = bestMove[1]
                    self.print_move(bestMove)
                self.board[nextMoveX][nextMoveY] = 'o'
                self.current_player = 'x'
                self.print_board()
                if self.getWinner():
                    break
                continue

    def is_valid(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        elif self.board[x][y] != self.empty_sq:

            return False
        else:
            return True

    def getWinner(self):
        player_turn = False
        if self.current_player == 'o':
            player_turn = True
        if(self.getScore(self.get_matrix_board(), True, player_turn) >= self.winScore):
            print('Player X has won!!!')
            return True
        if(self.getScore(self.get_matrix_board(),False, player_turn) >= self.winScore):
            print('Player O: AI has won !!!!!')
            return True
    def get_matrix_board(self):
        matrix =[[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'x':
                    matrix[i][j] = 2
                if self.board[i][j] == 'o':
                    matrix[i][j] = 1
        return matrix

    # create board instance
board = Board()
    # start game loop
board.game_loop()
