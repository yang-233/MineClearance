import pygame
import sys
import random
import pygame.transform
import pygame.locals

class window(object):
    def __init__(self):
        # 用int表示游戏状态
        self.gameState = 0
        # 用二位数组模拟地图
        self.gameMap = []
        # 用二维数组表示每个位置状态
        self.mapState = []
        # 地图宽度
        self.mapWidth = 20
        # 地图高度
        self.mapHeigth = 15
        # 炸弹个数
        self.numOfMine = 30
        # 单位长度大小
        self.unitSize = 30
        # 数字图片
        self.image = []
        # 第几套图片
        self.imgPath = "Image1"
        # 状态部分
        # 炸弹用-1表示
        self.mine = -1
        # 点击过后
        self.known = 1
        # 无状态用0表示
        self.unknown = 0
        # 标记为未知时用2表示
        self.problem = 2
        # 标记为炸弹时
        self.isMine = 3
        # 窗口大小
        self.windowSize = (self.mapWidth * self.unitSize, self.mapHeigth * self.unitSize)
        # self.windowSize = (500, 250)
        # 窗口背景颜色S
        self.backgroundColor = (135, 135, 135)
        # 窗口标题
        self.title = "扫雷"

        # pygame初始化
        pygame.init()

        # 画窗口
        self.screen = pygame.display.set_mode(self.windowSize, 0, 32)
        # 填充背景色
        self.screen.fill(self.backgroundColor)
        # 设置标题
        pygame.display.set_caption(self.title)

        # 初始化游戏
        self.load_image()
        self.init_game()
        # 游戏开始
        self.launch()

    def load_image(self):
        # 加载图片
        for i in range(0, 14):
            # 打开相应图片
            temp = pygame.image.load(self.imgPath + "/" + str(i) + ".jpg").convert()
            # 设置为指定大小
            temp = pygame.transform.scale(temp, (self.unitSize, self.unitSize))
            # 添加到list中
            self.image.append(temp)

    def init_game(self):
        # 初始化游戏状态
        self.gameState = 0
        # 初始化地图
        for i in range(0, self.mapHeigth):
            self.gameMap.append([])
            self.mapState.append([])
            for j in range(0, self.mapWidth):
                self.gameMap[i].append(0)
                self.mapState[i].append(self.unknown)
        # 随机生成地雷
        t = 0
        while (t < self.numOfMine):
            x = random.randint(0, self.mapWidth - 1)
            y = random.randint(0, self.mapHeigth - 1)
            if self.gameMap[y][x] != self.mine:
                self.gameMap[y][x] = self.mine
                t += 1
        # 周围8个格子
        dire = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # 生成map
        for i in range(0, self.mapHeigth):
            for j in range(0, self.mapWidth):
                if self.gameMap[i][j] != self.mine:
                    for k in range(0, 8):
                        self.gameMap[i][j] += self.has_mine(i + dire[k][0], j + dire[k][1])
        self.init_draw()

    # 计算该点是否有地雷
    def draw(self, y, x, id):
        self.screen.blit(self.image[id], (x * self.unitSize, y * self.unitSize))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (x * self.unitSize, y * self.unitSize, self.unitSize, self.unitSize),1)
        # pygame.display.update()

    def init_draw(self):
        for i in range(0, self.mapHeigth):
            for j in range(0, self.mapWidth):
                self.draw(i, j, 9)

    def bfs(self, y, x):
        dire = ((-1, 0), (1, 0), (0, -1), (0, 1))
        que = []
        que.append((y, x))
        while len(que) > 0:
            yy, xx = que[0]
            que.pop(0)
            self.draw(yy, xx, 0)
            for i in range(0, 4):
                if 0 <= yy + dire[i][0] < self.mapHeigth \
                        and 0 <= xx + dire[i][1] < self.mapWidth \
                        and self.mapState[yy + dire[i][0]][xx + dire[i][1]] == self.unknown \
                        and self.gameMap[yy + dire[i][0]][xx + dire[i][1]] == 0:
                    que.append((yy + dire[i][0], xx + dire[i][1]))
                    self.mapState[yy + dire[i][0]][xx + dire[i][1]] = self.known

    def has_mine(self, y, x):
        if 0 <= x < self.mapWidth and 0 <= y < self.mapHeigth and self.gameMap[y][x] == self.mine:
            return 1
        return 0

    def option(self, x, y, val):
        if val == 1 and self.mapState[y][x] == self.unknown:  # 按下左键
            if self.gameMap[y][x] == self.mine:  # 踩雷
                self.draw(y, x, 11)

            elif self.gameMap[y][x] == 0:
                self.bfs(y, x)
            else:  # 显示数字
                self.draw(y, x, self.gameMap[y][x])
            # 状态已知
            self.mapState[y][x] = self.known
        if val == 3:  # 按下右键
            if self.mapState[y][x] == self.unknown:
                self.draw(y, x, 12)
                self.mapState[y][x] = self.isMine
            elif self.mapState[y][x] == self.isMine:
                self.draw(y, x, 13)
                self.mapState[y][x] = self.problem
            elif self.mapState[y][x] == self.problem:
                self.draw(y, x, 9)
                self.mapState[y][x] = self.unknown

    def launch(self):
        # 程序进行
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit()
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x //= self.unitSize
                    y //= self.unitSize
                    self.option(x, y, event.button)
                pygame.display.update()

def test():
    pygame.init()
    screen = pygame.display.set_mode((600, 400), 0, 32)
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (100, 100, 50, 50), 1)
    pygame.display.update()

if __name__ == "__main__":
    window()
