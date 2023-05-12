import copy
import random
import time

class TicTacToeAI:
    def __init__(self, player):
        self.player = player
        self.winScore = 10000000
        self.empty_sq = ' '
        self.board =[]
        self.size = 0
    def calc_next_move(self, depth):
        #applying threat space search to get the best move first then using ABminmax
        board = self.get_matrix_board(self.size)
        attMove = self.search_winning_move(board) #optimal strat to win

        defMove = self.search_lose_move(board) #strat to get defense

        move = [0, 0]
        if attMove[1] is not None and attMove[2] is not None:
            move[0] = attMove[1]
            move[1] = attMove[2]
            print('Att move')
            return move
        if defMove[1] is not None and defMove[2] is not None:
            move[0] = defMove[1]
            move[1] = defMove[2]
            print('Def move')
            return move
        else:
            attMove = self.minimax_search_ab(depth, board, True, -1.0, self.winScore)
            if attMove[1] is None:
                move = None
            else:
                move[0] = attMove[1]
                move[1] = attMove[2]
            print('AB move')
            return move

        #Getting board with next move simulator
    def next_move_sim(self, board, move, isUserTurn):  # get nextmove matrix
        i, j = move[0], move[1]
        row, col = len(board), len(board[0])
        newBoard = [[0] * col for _ in range(row)]
        for h in range(row):
            for k in range(col):
                newBoard[h][k] = board[h][k]
        newBoard[i][j] = 2 if isUserTurn else 1
        return newBoard



    # search for possible winning move based on evaluation winning score
    def search_winning_move(self, matrix):
        allPossibleMoves = self.generate_moves(matrix)
        winning_move = [None, None, None]

        for move in allPossibleMoves:
            temp_board = self.next_move_sim(matrix, move, False)
            print(self.get_score(temp_board, False, False))
            if self.get_score(temp_board, False, False) >= self.winScore:
                winning_move[1] = move[0]
                winning_move[2] = move[1]
                print(self.get_score(temp_board, False, False) + 'move: ' + winning_move)
                return winning_move

        return winning_move

    def search_lose_move(self, matrix):
        allPossibleMoves = self.generate_moves(matrix)
        print('Possible Moves: ', len(allPossibleMoves))

        losingMove = [None, None, None]

        for move in allPossibleMoves:
            temp_board = self.next_move_sim(matrix, move, True)

            # If the black player has a winning score in that temporary board, return the move.
            if self.get_score(temp_board, True, False) >= self.winScore:
                losingMove[1] = move[0]
                losingMove[2] = move[1]
                return losingMove

        return losingMove
    def generate_moves(self, board): #Creating domain knowledge for AI
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:  # Check if the cell is empty
                    # Check for adjacent stones in all four directions vertical horizontal diagonal \/
                    if i > 0 and j > 0 and board[i - 1][j - 1] != 0:
                        moves.append((i, j))
                    elif i > 0 and board[i - 1][j] != 0:
                        moves.append((i, j))
                    elif i > 0 and j < self.size - 1 and board[i - 1][j + 1] != 0:
                        moves.append((i, j))
                    elif j > 0 and board[i][j - 1] != 0:
                        moves.append((i, j))
                    elif j < self.size - 1 and board[i][j + 1] != 0:
                        moves.append((i, j))
                    elif i < self.size - 1 and j > 0 and board[i + 1][j - 1] != 0:
                        moves.append((i, j))
                    elif i < self.size - 1 and board[i + 1][j] != 0:
                        moves.append((i, j))
                    elif i < self.size - 1 and j < self.size - 1 and board[i + 1][j + 1] != 0:
                        moves.append((i, j))
        return moves
    def minimax_search_ab(self, depth, board, max_player, alpha, beta):
        if depth == 0:
            return [self.evaluate_board(board, not max_player), None, None]

        all_possible_moves = self.generate_moves(board)

        if len(all_possible_moves) == 0:
            return [self.evaluate_board(board, not max_player), None, None]

        bestMove = [None, None, None]

        if max_player:
            bestMove[0] = -100000000

            for move in all_possible_moves:
                # Play current move
                temp_board = self.next_move_sim(board, move, False)

                tempMove = self.minimax_search_ab(depth - 1, temp_board, not max_player, alpha, beta)

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
            bestMove[1] = all_possible_moves[0][0]
            bestMove[2] = all_possible_moves[0][1]

            for move in all_possible_moves:
                temp_board = self.next_move_sim(board, move, True)

                tempMove = self.minimax_search_ab(depth - 1, temp_board, not max_player, alpha, beta)

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
        # print(self.evaluate_board(board, not max_player))
        return bestMove
    def evaluate_board(self, board, userTurn): #GET EVALUATION RATIO O winning white/ X winning
        x_score = self.get_score(board, True, userTurn)
        o_score = self.get_score(board, False, userTurn)

        if x_score == 0:
            x_score = 1.0

        return o_score / x_score
    def get_score(self, board, forX, x_turn):
        return self.horizontal_score(board, forX, x_turn) + \
            self.vertical_score(board, forX, x_turn) + \
            self.diagonal_score(board, forX, x_turn)
    def horizontal_score(self, board_matrix, forX, playersTurn):
        consecutive = 0
        blocks = 2
        score = 0

        for i in range(len(board_matrix)):
            for j in range(len(board_matrix[0])):
                if board_matrix[i][j] == (2 if forX else 1):
                    # 2. Đếm...
                    consecutive += 1
                # gặp ô trống
                elif board_matrix[i][j] == 0:
                    if consecutive > 0:
                        # Ra: Ô trống ở cuối sau khi đếm. Giảm block rồi bắt đầu tính điểm sau đó reset lại ban đầu
                        blocks -= 1
                        score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        # 1. Vào reset lại blocks = 1 rồi bắt đầu đếm
                        blocks = 1
                # gặp quân địch
                elif consecutive > 0:
                    # 2.Ra:  Ô bị chặn sau khi đếm. Tính điểm sau đó reset lại.
                    score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    # 1. Vào: reset lại blocks = 2 rồi bắt đầu đếm
                    blocks = 2

            # 3. Ra: nhưng lúc này đang ở cuối. Nếu liên tục thì vẫn tính cho đến hết dòng
            if consecutive > 0:
                score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)

            # reset lại để tiếp tục chạy cho dòng tiếp theo
            consecutive = 0
            blocks = 2

        return score

    def vertical_score(self, boardMatrix, forX, playersTurn):
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
                        score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
            consecutive = 0
            blocks = 2

        return score

    def diagonal_score(self, boardMatrix, forX, playersTurn):
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
                        score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
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
                        score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else:
                        blocks = 1
                elif consecutive > 0:
                    score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else:
                    blocks = 2

            if consecutive > 0:
                score += self.get_consecutive_set_score(consecutive, blocks, forX == playersTurn)
            consecutive = 0
            blocks = 2

        return score

    def get_consecutive_set_score(self, count, blocks, currentTurn):
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
    def get_matrix_board(self, size):
        matrix =[[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'x':
                    matrix[i][j] = 2
                if self.board[i][j] == 'o':
                    matrix[i][j] = 1
        return matrix
    def get_move(self, board, size):
        # Find all available positions on the board
        self.board = board
        self.size = size
        size = int(size)
        available_moves = []

        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    available_moves.append((i, j))
        start = time.time()
        bestMove = self.calc_next_move(3)
        end = time.time()
        if bestMove is not None:
            print('Evaluation time: {}s'.format(round(end - start, 7)))
            move = (bestMove[0], bestMove[1])
            return move
        # If there are no available moves, return None
        # Choose a random available move
        return available_moves[random.randint(0, len(available_moves) - 1)]
