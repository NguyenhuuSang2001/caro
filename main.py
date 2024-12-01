import streamlit as st
import numpy as np
import random
import math

# Constants
BOARD_SIZE = 15
EMPTY = 0
WHITE = 1
BLACK = 2

# Initialize board and game state
def init_game():
    return {
        "board": np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int),
        "current_turn": BLACK,
        'first': True,
        "game_over": False,
        "winner": None,
        "mode": "Human vs AI",
        "algorithm": "Alpha-Beta"
    }

class Board:
    def __init__(self):
        self.patterns = {
            '11111': 30000000,
            '22222': -30000000,
            '011110': 20000000,
            '022220': -20000000,
            '011112': 50000,
            '211110': 50000,
            '022221': -50000,
            '122220': -50000,
            '01110': 30000,
            '02220': -30000,
            '011010': 15000,
            '010110': 15000,
            '022020': -15000,
            '020220': -15000,
            '001112': 2000,
            '211100': 2000,
            '002221': -2000,
            '122200': -2000,
            '211010': 2000,
            '210110': 2000,
            '010112': 2000,
            '011012': 2000,
            '122020': -2000,
            '120220': -2000,
            '020221': -2000,
            '022021': -2000,
            '01100': 500,
            '00110': 500,
            '02200': -500,
            '00220': -500
        }
    # Kiểm tra thắng
    def win_check(self, Piece_Number, Piece_Colour, board):
        point = self.points_check(board, Piece_Number)
        if point == 30000000:
            Winner = Piece_Colour
            return Winner
        
    def btsConvert(self, board, player):
        temp_board = np.array(board)
        
        cList, rList, dList = [], [], []
        board_col = len(temp_board[0])
        
        bdiag = [temp_board.diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        fdiag = [temp_board[::-1, :].diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        
        for dgd in bdiag:
            bdiagVals = ""
            for point in dgd:
                if point == 0:
                    bdiagVals += "0"
                elif point == player:
                    bdiagVals += "1"
                else:
                    bdiagVals += "2"
            dList.append(bdiagVals)
            
        for dgu in fdiag:
            fdiagVals = ""
            for point in dgu:
                if point == 0:
                    fdiagVals += "0"
                elif point == player:
                    fdiagVals += "1"
                else:
                    fdiagVals += "2"
            dList.append(fdiagVals)
            
        boardT = temp_board.copy().transpose()
        
        for col in boardT:
            colVals = ""
            for point in col:
                if point == 0:
                    colVals += "0"
                elif point == player:
                    colVals += "1"
                else:
                    colVals += "2"
            cList.append(colVals)
            
        for row in board:
            rowVals = ""
            for point in row:
                if point == 0:
                    rowVals += "0"
                elif point == player:
                    rowVals += "1"
                else:
                    rowVals += "2"
            rList.append(rowVals)
            
        return dList+cList+rList

    def points_check(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
        return val
    
    def points(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
        return val
    

# Game Board Class
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # 0: empty, 1: player, 2: AI
        self.history = []  # To track moves for undo
        # self.patterns = {
        #     '11111': 1000000,  # Win for Player
        #     '22222': -1000000, # Win for AI
        #     '011110': 1000,    # Open four (good position for Player)
        #     '022220': -1000,   # Open four (good position for AI)
        # }
        self.patterns = {
            '11111': 30000000,
            '22222': -30000000,
            '011110': 20000000,
            '022220': -20000000,
            '011112': 50000,
            '211110': 50000,
            '022221': -50000,
            '122220': -50000,
            '01110': 30000,
            '02220': -30000,
            '011010': 15000,
            '010110': 15000,
            '022020': -15000,
            '020220': -15000,
            '001112': 2000,
            '211100': 2000,
            '002221': -2000,
            '122200': -2000,
            '211010': 2000,
            '210110': 2000,
            '010112': 2000,
            '011012': 2000,
            '122020': -2000,
            '120220': -2000,
            '020221': -2000,
            '022021': -2000,
            '01100': 500,
            '00110': 500,
            '02200': -500,
            '00220': -500
        }
    
    def reset_board(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.history = []

    def make_move(self, x, y, player):
        if self.board[x, y] == 0:
            self.board[x, y] = player
            self.history.append((x, y))  # Save move for undo
            return True
        return False

    def undo_move(self):
        if self.history:
            x, y = self.history.pop()
            self.board[x, y] = 0
            return True
        return False

    def is_winner(self, player):
        for row in range(self.size):
            for col in range(self.size):
                if self.check_line(row, col, player, (0, 1)) or \
                   self.check_line(row, col, player, (1, 0)) or \
                   self.check_line(row, col, player, (1, 1)) or \
                   self.check_line(row, col, player, (-1, 1)):
                    return True
        return False

    def check_line(self, row, col, player, direction):
        """Check if there's a winning line for the player starting from (row, col) in a given direction."""
        try:
            for i in range(5):
                if self.board[row + direction[0] * i, col + direction[1] * i] != player:
                    return False
            return True
        except IndexError:
            return False

    def evaluate_board(self):
        """Evaluate board for AI move scoring."""
        score = 0
        for pattern, value in self.patterns.items():
            score += self.count_pattern(pattern) * value
        return score

    def count_pattern(self, pattern):
        """Count occurrences of a pattern in the board."""
        str_board = ''.join(map(str, self.board.flatten()))
        return str_board.count(pattern)

    # Kiểm tra thắng
    def win_check(self, Piece_Number, Piece_Colour, board):
        point = self.points_check(board, Piece_Number)
        if point == 30000000:
            Winner = Piece_Colour
            return Winner
        
    def btsConvert(self, board, player):
        temp_board = np.array(board)
        
        cList, rList, dList = [], [], []
        board_col = len(temp_board[0])
        
        bdiag = [temp_board.diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        fdiag = [temp_board[::-1, :].diagonal(i) for i in range(board_col - 5, - board_col + 4, -1)]
        
        for dgd in bdiag:
            bdiagVals = ""
            for point in dgd:
                if point == 0:
                    bdiagVals += "0"
                elif point == player:
                    bdiagVals += "1"
                else:
                    bdiagVals += "2"
            dList.append(bdiagVals)
            
        for dgu in fdiag:
            fdiagVals = ""
            for point in dgu:
                if point == 0:
                    fdiagVals += "0"
                elif point == player:
                    fdiagVals += "1"
                else:
                    fdiagVals += "2"
            dList.append(fdiagVals)
            
        boardT = temp_board.copy().transpose()
        
        for col in boardT:
            colVals = ""
            for point in col:
                if point == 0:
                    colVals += "0"
                elif point == player:
                    colVals += "1"
                else:
                    colVals += "2"
            cList.append(colVals)
            
        for row in board:
            rowVals = ""
            for point in row:
                if point == 0:
                    rowVals += "0"
                elif point == player:
                    rowVals += "1"
                else:
                    rowVals += "2"
            rList.append(rowVals)
            
        return dList+cList+rList

    def points_check(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val = max(val, self.patterns[st])
        return val
    
    def points(self, board, player):  # evaluates
        val = 0
        player1StrArr = self.btsConvert(board, player)
        for i in range(len(player1StrArr)):
            len1 = len(player1StrArr[i])
            for j in range(len1):
                n = j+5
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
            for j in range(len1):
                n = j+6
                if(n <= len1):
                    st = player1StrArr[i][j:n]
                    if st in self.patterns:
                        val += self.patterns[st]
        return val
    
class Algorithms():
    b = Board()
    def __init__(self):
        self.MAX, self.MIN = math.inf, -math.inf
        self.save_point = 0
    
    def getCoordsAround(self, board):
        # print(board)
        temp_board = np.array(board)
        board_size = len(temp_board)
        outTpl = np.nonzero(temp_board)  # return tuple of all non zero points on board
        potentialValsCoord = {}

        for i in range(len(outTpl[0])):
            y = outTpl[0][i]
            x = outTpl[1][i]

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < board_size and 0 <= new_y < board_size and temp_board[new_y][new_x] == 0:
                        potentialValsCoord[(new_x, new_y)] = 1

        finalValsX, finalValsY = [], []
        for key in potentialValsCoord:
            finalValsY.append(key[1])
            finalValsX.append(key[0])
        
        return finalValsX, finalValsY
    
    def getCoordsAroundForGreedy(self, board):
        # print(board)
        temp_board = np.array(board)
        board_size = len(temp_board)
        outTpl = np.nonzero(temp_board)  # return tuple of all non zero points on board
        potentialValsCoord = {}

        for i in range(len(outTpl[0])):
            y = outTpl[0][i]
            x = outTpl[1][i]

            for dy in [-2, -1, 0, 1, 2]:
                for dx in [-2, -1, 0, 1, 2]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < board_size and 0 <= new_y < board_size and temp_board[new_y][new_x] == 0:
                        potentialValsCoord[(new_x, new_y)] = 1

        finalValsX, finalValsY = [], []
        for key in potentialValsCoord:
            finalValsY.append(key[1])
            finalValsX.append(key[0])
        
        return finalValsX, finalValsY

    def getRandomMove(self, board):
        # print(board)
        
        global AI_turn
        boardSize = len(board)
        ctr = 0
        idx = boardSize//2
        while ctr < (idx/2):
            if board[idx+ctr][idx+ctr] == 0:
                AI_turn = False
                return idx+ctr, idx+ctr
            elif board[idx+ctr][idx-ctr] == 0:
                AI_turn = False
                return idx+ctr, idx-ctr
            elif board[idx+ctr][idx] == 0:
                AI_turn = False
                return idx+ctr, idx
            elif board[idx][idx+ctr] == 0:
                AI_turn = False
                return idx, idx+ctr
            elif board[idx][idx-ctr] == 0:
                AI_turn = False
                return idx, idx-ctr
            elif board[idx-ctr][idx] == 0:
                AI_turn = False
                return idx-ctr, idx
            elif board[idx-ctr][idx-ctr] == 0:
                AI_turn = False
                return idx-ctr, idx-ctr
            elif board[idx-ctr][idx+ctr] == 0:
                AI_turn = False
                return idx-ctr, idx+ctr
            ctr += 1
        for i in range(boardSize):
            for j in range(boardSize):
                if board[i][j] == 0:
                    AI_turn = False
                    return i, j

    def otherPlayerStone(self, player):
        return 2 if player==1 else 1

    def greedyAlgorithm(self, board, player):
        # print(board)
        
        bestMoveRow = bestMoveCol = -1
        bestOtherMoveRow = bestOtherMoveCol = -1
        
        mostPoints = float('-inf')
        mostOtherPoints = float('-inf')
        
        potentialValsX, potentialValsY = self.getCoordsAroundForGreedy(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = player
                movePoints = self.b.points(board, player)

                board[potentialValsY[i]][potentialValsX[i]] = self.otherPlayerStone(player)
                moveOtherPoints = self.b.points(board, self.otherPlayerStone(player))
                
                board[potentialValsY[i]][potentialValsX[i]] = 0
                
                if moveOtherPoints > mostOtherPoints:
                    bestOtherMoveRow = potentialValsY[i]
                    bestOtherMoveCol = potentialValsX[i]
                    mostOtherPoints = moveOtherPoints
                
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints

        global AI_turn
        AI_turn = False

        if mostOtherPoints >= mostPoints:
            return bestOtherMoveRow, bestOtherMoveCol
        else:
            return bestMoveRow, bestMoveCol

    def alpha_beta(self, board, isMaximizer, depth, alpha, beta, player):  # alpha, beta
        # print(board)
        
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.alpha_beta(board, False, depth+1, alpha, beta, player)
                    best = max(best, score)
                    alpha = max(alpha, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.alpha_beta(board, True, depth+1, alpha, beta, player)
                    best = min(best, score)
                    beta = min(beta, best)  # best AI Opponent move
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
                    if beta <= alpha:
                        break
            return best

    def alpha_beta_computer(self, board, isComputerFirst):
        # print(board)
        
        mostPoints = float('-inf')
        alpha,beta = self.MIN, self.MAX
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                movePoints = max(mostPoints, self.alpha_beta(
                    board, False, 1, alpha, beta, isComputerFirst))
                alpha = max(alpha, movePoints)
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if beta <= alpha:
                    break
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol
    
    def minimax(self, board, isMaximizer, depth, player):  # alpha, beta
        # print(board)
        
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.minimax(board, False, depth+1, player)
                    best = max(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.minimax(board, True, depth+1, player)
                    best = min(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best

    def minimax_computer(self, board, isComputerFirst):
        # print(board)
        
        mostPoints = float('-inf')
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                movePoints = max(mostPoints, self.minimax(
                    board, False, 1, isComputerFirst))
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if movePoints > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = movePoints

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol
    
    def mcts(self, board, isMaximizer, depth, player):  # alpha, beta
        # print(board)
        
        point = self.b.points(board, player)
        
        if depth == 2:
            return point
        
        if isMaximizer:  # THE MAXIMIZER
            best = self.MIN
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            self.save_point += len(potentialValsX)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    board[potentialValsY[i]][potentialValsX[i]] = player
                    score = self.mcts(board, False, depth+1, player)
                    best = max(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best
        else:  # THE MINIMIZER
            best = self.MAX
            potentialValsX, potentialValsY = self.getCoordsAround(board)
            self.save_point += len(potentialValsX)
            for i in range(len(potentialValsX)):
                if board[potentialValsY[i]][potentialValsX[i]] == 0:
                    otherplayer = self.otherPlayerStone(player)
                    board[potentialValsY[i]][potentialValsX[i]] = otherplayer
                    score = self.mcts(board, True, depth+1, player)
                    best = min(best, score)
                    board[potentialValsY[i]][potentialValsX[i]] = 0  # undoing
            return best

    def mcts_computer(self, board, isComputerFirst):
        # print(board)
        
        mostPoints = float('-inf')
        bestMoveRow = bestMoveCol = -1
        
        potentialValsX, potentialValsY = self.getCoordsAround(board)
        save_x = len(potentialValsX)
        for i in range(len(potentialValsX)):
            if board[potentialValsY[i]][potentialValsX[i]] == 0:
                board[potentialValsY[i]][potentialValsX[i]] = isComputerFirst
                self.save_point = 0
                movePoints = self.mcts(board, False, 1, isComputerFirst)

                ucb = movePoints / self.save_point + 1.4 * math.sqrt(math.log(save_x) / self.save_point)
                board[potentialValsY[i]][potentialValsX[i]] = 0
                if ucb > mostPoints:
                    bestMoveRow = potentialValsY[i]
                    bestMoveCol = potentialValsX[i]
                    mostPoints = ucb

        global AI_turn
        AI_turn = False
        return bestMoveRow, bestMoveCol

# AI Algorithm
def ai_move(board_obj):
    state = st.session_state["game_state"]
    ai = Algorithms()
    board =  board_obj.board
    first = 1
    if state["algorithm"]=="Alpha-Beta":
        return ai.alpha_beta_computer(board, first)
    elif state["algorithm"]=="Minimax":
        return ai.minimax_computer(board, first)
    elif state["algorithm"]=="Greedy":
        return ai.greedyAlgorithm(board, first)
    elif state["algorithm"]=="MCTS":
        return ai.mcts_computer(board, first)
    return random.choice(np.argwhere(board_obj.board == 0))
    
def main():
    # Import the CSS file
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("ĐỒ ÁN CUỐI KỲ")
    
    # st.sidebar.title("Game Settings")
    
    if "board" not in st.session_state:
        st.session_state.board = Board(size=BOARD_SIZE)
        st.session_state.current_player = 1  # 1 for player, 2 for AI
        st.session_state.message = "Your Turn!"
    
    if "start_game" not in st.session_state:
        st.session_state.start_game = False
        
    if "end_game" not in st.session_state:
        st.session_state.end_game = False
    
    end_game = st.session_state.end_game

    board = st.session_state.board
    current_player = st.session_state.current_player
    

        
    with st.sidebar:    
        st.markdown(
            """
            <h3 style="text-align: center;">Trí tuệ nhân tạo_ Nhóm 06CLC</h3>
            <h4 style="text-align: center; border-bottom: 2px solid;margin-bottom: 30px;">Nguyễn Anh Hào - 21110823</h4>
            """,
            unsafe_allow_html=True
        )    

        
        if "game_state" not in st.session_state:
            st.session_state["game_state"] = init_game()

        state = st.session_state["game_state"]

        # Select mode and algorithm
        state["mode"] = st.radio("Game Mode", ["Human vs Human", "Human vs AI"])
        if state["mode"] == "Human vs AI":
            algorithm = st.radio("Algorithm", ["Alpha-Beta", "Minimax", "Greedy", "MCTS"])
            state["first"] = st.radio("First Round of Play", ["Human", "AI"])
            print(algorithm)
            if state["algorithm"] != algorithm:
                state["algorithm"] = algorithm
                st.session_state["game_state"] = state
                st.session_state.start_game = False
                board.reset_board()
                st.session_state.current_player = 1
                st.session_state.end_game = False
                if state["first"] == "AI":
                    st.session_state.current_player = 2
                    st.session_state.message = "AI's Turn"
                                   
                

        if st.session_state.start_game:
            col1, col2 = st.columns(2)
            with col1:
                # Reset button
                if st.button("Restart"):
                    st.session_state["game_state"] = init_game()
                    board.reset_board()
                    st.session_state.current_player = 1
                    st.session_state.end_game = False
                    st.session_state.message = "Your Turn!"
                    print(state)
                    if state["first"] == "AI":
                        st.session_state.current_player = 2
                    st.rerun()
            with col2:
                if st.button("Undo"):
                    if board.undo_move():
                        st.session_state.current_player = 3 - st.session_state.current_player  # Switch player
                        st.session_state.message = "Move undone."
                    else:
                        st.session_state.message = "No moves to undo."
                    st.rerun()
        


    # Game Board
    if st.session_state.start_game:       
        st.write(f"**Status:** {st.session_state.message}")
        
        with st.container():
            for row in range(board.size):
                cols = st.columns(board.size)
                for col in range(board.size):
                    cell = board.board[row, col]
                    symbol = " " if cell == 0 else ("X" if cell == 1 else "O")
                    btn = cols[col].button(symbol, key=f"{row}-{col}")
                    if not end_game and cell ==0 and btn:
                        if current_player == 1:
                            board.make_move(row, col, 1)
                            if board.is_winner(1):
                                st.session_state.message = "You Win!"
                                if state["mode"] != "Human vs AI":
                                    st.session_state.message = "Player 1 Win!"
                                st.session_state.end_game = True
                            else:
                                st.session_state.current_player = 2
                                st.session_state.message = "AI's Turn"
                                if state["mode"] != "Human vs AI":
                                    st.session_state.message = "Player 2 Turn!"
                            st.rerun()
                        if current_player == 2 and state["mode"] != "Human vs AI":
                            board.make_move(row, col, 2)
                            if board.is_winner(2):
                                st.session_state.message = "Player 2 Win!"
                                st.session_state.end_game = True
                            else:
                                st.session_state.current_player = 1
                                st.session_state.message = "Player 1 Turn!"
                            st.rerun()
    else:
        if st.button('Click to Start Playing...', type='primary'):
            st.session_state.start_game = True
            
            
    if "Win!" in st.session_state.message:
            import streamlit.components.v1 as components
            mycode = f"<script>alert('{st.session_state.message}')</script>"
            components.html(mycode, height=0, width=0)
    

    # AI's Turn
    if not end_game and current_player == 2:
        if state["mode"] == "Human vs AI":
            move = ai_move(board)
            if move:
                board.make_move(*move, 2)
                if board.is_winner(2):
                    st.session_state.message = "AI Win!"
                    st.session_state.end_game = True
                else:
                    st.session_state.current_player = 1
                    st.session_state.message = "Your Turn!"
                st.rerun()
        

if __name__ == "__main__":
    main()
