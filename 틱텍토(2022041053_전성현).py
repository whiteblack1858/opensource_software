import random
import time

class TicTacToe:
    def __init__(self):
        # 3x3 게임판 초기화 (빈 공간은 ' '로 표시)
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # 사람은 X, 컴퓨터는 O
        
    def print_board(self):
        """게임판 출력"""
        print("\n  0 1 2")
        for i in range(3):
            print(f"{i} ", end="")
            for j in range(3):
                print(f"{self.board[i][j]}", end="")
                if j < 2:
                    print("|", end="")
            print()
            if i < 2:
                print("  -+-+-")
                
    def is_valid_move(self, row, col):
        """유효한 이동인지 확인"""
        # 범위 내에 있고 빈 칸인지 확인
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' '
    
    def make_move(self, row, col):
        """이동 수행"""
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self):
        """승자 확인"""
        # 행 확인
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
        
        # 열 확인
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        
        # 대각선 확인
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None  # 승자 없음
    
    def is_board_full(self):
        """게임판이 가득 찼는지 확인"""
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def switch_player(self):
        """플레이어 전환"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_empty_cells(self):
        """빈 칸 찾기"""
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells
    
    def computer_move(self):
        """컴퓨터 자동 이동"""
        print("\n컴퓨터가 생각하는 중...")
        time.sleep(1)  # 생각하는 척 잠시 대기
        
        # 1. 우승 가능한 위치 찾기
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'O'
            if self.check_winner() == 'O':
                return row, col
            self.board[row][col] = ' '  # 원상복구
        
        # 2. 사람이 우승하는 것 막기
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'X'
            if self.check_winner() == 'X':
                self.board[row][col] = 'O'
                return row, col
            self.board[row][col] = ' '  # 원상복구
        
        # 3. 중앙 위치 선호
        if self.board[1][1] == ' ':
            return 1, 1
        
        # 4. 모서리 위치 선호
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if self.board[corner[0]][corner[1]] == ' ']
        if available_corners:
            return random.choice(available_corners)
        
        # 5. 나머지 빈 칸 중 랜덤 선택
        empty_cells = self.get_empty_cells()
        return random.choice(empty_cells)
    
    def play_game(self):
        """게임 실행"""
        print("틱택토 게임을 시작합니다.")
        print("사람(X)과 컴퓨터(O)가 번갈아 가며 진행합니다.")
        print("위치는 '행 열' 형식으로 입력하세요. (예: '1 2')")
        
        while True:
            self.print_board()
            
            # 사람 차례
            if self.current_player == 'X':
                try:
                    row, col = map(int, input("\n위치 입력 (행 열): ").split())
                    if not self.make_move(row, col):
                        print("유효하지 않은 위치입니다. 다시 입력해주세요.")
                        continue
                except ValueError:
                    print("유효한 숫자 형식으로 입력해주세요. (예: '1 2')")
                    continue
            
            # 컴퓨터 차례
            else:
                row, col = self.computer_move()
                self.make_move(row, col)
                print(f"컴퓨터는 ({row}, {col}) 위치에 놓았습니다.")
            
            # 승자 확인
            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == 'X':
                    print("\n축하합니다! 당신이 이겼습니다!")
                else:
                    print("\n컴퓨터가 이겼습니다.")
                break
            
            # 무승부 확인
            if self.is_board_full():
                self.print_board()
                print("\n무승부입니다!")
                break
            
            # 다음 플레이어로 전환
            self.switch_player()

# 게임 실행
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()