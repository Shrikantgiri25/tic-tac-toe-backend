class TicTacToeLogic:
    @staticmethod
    def check_winner(board):
        """Check if there's a winner. Returns 'X', 'O', or None"""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        
        # Check columns
        for col in range(3):
            if (board[0][col] == board[1][col] == board[2][col] 
                and board[0][col] is not None):
                return board[0][col]
        
        # Check diagonals
        if (board[0][0] == board[1][1] == board[2][2] 
            and board[0][0] is not None):
            return board[0][0]
        
        if (board[0][2] == board[1][1] == board[2][0] 
            and board[0][2] is not None):
            return board[0][2]
        
        return None
    
    @staticmethod
    def is_board_full(board):
        """Check if board is full (draw)"""
        return all(cell is not None for row in board for cell in row)
    
    @staticmethod
    def is_valid_move(board, row, col):
        """Check if move is valid"""
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        return board[row][col] is None
    
    @staticmethod
    def position_to_coords(position):
        """Convert position (0-8) to row, col"""
        return position // 3, position % 3
    
    @staticmethod
    def coords_to_position(row, col):
        """Convert row, col to position (0-8)"""
        return row * 3 + col