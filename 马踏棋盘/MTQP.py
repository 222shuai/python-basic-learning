"""
递归回溯法：叫称为试探法，按选优条件向前搜索，当搜索到某一步，发现原先选择并不优或达不到目标时，就退回一步重新选择，
比较经典的问题包括骑士巡逻、八皇后和迷宫寻路等。
"""
# 这种退回操作一般就使用嵌套

SIZE = 8
total = 0


# 这个函数在patrol中调用，所以row，col直接引用patrol中的
def print_board(board):
    for row in board:
        for col in row:
            print(str(col).center(4), end='')
        print()


def patrol(board, row, col, step=1):
    if 0 <= row < SIZE and 0 <= col < SIZE and board[row][col] == 0:  # 初始化时将board都设为0了，==0表示没有走过
        board[row][col] = step
        if step == SIZE * SIZE:  # 能够遍历棋盘就打印
            global total
            total += 1
            print(f'第{total}种走法: ')
            print_board(board)
        patrol(board, row - 2, col - 1, step + 1)
        patrol(board, row - 1, col - 2, step + 1)
        patrol(board, row + 1, col - 2, step + 1)
        patrol(board, row + 2, col - 1, step + 1)
        patrol(board, row + 2, col + 1, step + 1)
        patrol(board, row + 1, col + 2, step + 1)
        patrol(board, row - 1, col + 2, step + 1)
        patrol(board, row - 2, col + 1, step + 1)
        board[row][col] = 0  # 消去之前走到这里的痕迹


def main():
    board = [[0] * SIZE for _ in range(SIZE)]  # 初始化棋盘
    patrol(board, SIZE - 1, SIZE - 1)  # 从棋盘右下角开始


if __name__ == '__main__':
    main()