import pygame

class Button:
    NORMAL=0
    MOVE=1
    DOWN=2
    def __init__(self,x,y,text,imgNormal,imgMove=None,imgDown=None,callBackFunc=None,font=None,rgb=(0,0,0)):
        """
        初始化按鈕的相關引數
        :param x: 按鈕在窗體上的x座標
        :param y: 按鈕在窗體上的y座標
        :param text: 按鈕顯示的文字
        :param imgNormal: surface型別,按鈕正常情況下顯示的圖片
        :param imgMove: surface型別,滑鼠移動到按鈕上顯示的圖片
        :param imgDown: surface型別,滑鼠按下時顯示的圖片
        :param callBackFunc: 按鈕彈起時的回撥函式
        :param font: pygame.font.Font型別,顯示的字型
        :param rgb: 元組型別,文字的顏色
        """
        #初始化按鈕相關屬性
        self.imgs=[]
        if not imgNormal:
            raise Exception("請設定普通狀態的圖片")
        self.imgs.append(imgNormal)     #普通狀態顯示的圖片
        self.imgs.append(imgMove)       #被選中時顯示的圖片
        self.imgs.append(imgDown)       #被按下時的圖片
        for i in range(2,0,-1):
            if not self.imgs[i]:
                self.imgs[i]=self.imgs[i-1]

        self.callBackFunc=callBackFunc      #觸發事件
        self.status=Button.NORMAL       #按鈕當前狀態
        self.x=x
        self.y=y
        self.w=imgNormal.get_width()
        self.h=imgNormal.get_height()
        self.text=text
        self.font=font
        #文字表面
        self.textSur=self.font.render(self.text,True,rgb)

    def draw(self,destSuf):
        dx=(self.w/2)-(self.textSur.get_width()/2)
        dy=(self.h/2)-(self.textSur.get_height()/2)
        #先畫按鈕背景
        if self.imgs[self.status]:
            destSuf.blit(self.imgs[self.status], [self.x, self.y])
        #再畫文字
        destSuf.blit(self.textSur,[self.x+dx,self.y+dy])

    def colli(self,x,y):
        #碰撞檢測
        if self.x<x<self.x+self.w and self.y<y<self.y+self.h:
            return True
        else:
            return False

    def getFocus(self,x,y):
        #按鈕獲得焦點時
        if self.status==Button.DOWN:
            return
        if self.colli(x,y):
            self.status=Button.MOVE
        else:
            self.status=Button.NORMAL

    def mouseDown(self,x,y):
        if self.colli(x,y):
            self.status = Button.DOWN

    def mouseUp(self):
        if self.status==Button.DOWN:    #如果按鈕的當前狀態是按下狀態,才繼續執行下面的程式碼
            self.status=Button.NORMAL   #按鈕彈起,所以還原成普通狀態
            if self.callBackFunc:       #呼叫回撥函式
                return self.callBackFunc()


def modePage():
    start1 = False
    start2 = False
    # 初始化pygame
    pygame.init()
    winSur = pygame.display.set_mode([1100, 600])

    # 載入按鈕圖片
    background = pygame.image.load("./button/background.png").convert_alpha()
    surBtnNormal_1 = pygame.image.load("./button/btn_mode1_1.png").convert_alpha()
    # surBtnMove = pygame.image.load("./button/btn_move.png").convert_alpha()
    surBtnDown_1 = pygame.image.load("./button/btn_mode1_2.png").convert_alpha()
    surBtnNormal_2 = pygame.image.load("./button/btn_mode2_1.png").convert_alpha()
    surBtnDown_2 = pygame.image.load("./button/btn_mode2_2.png").convert_alpha()
    

    #按鈕使用的字型
    btnFont = pygame.font.SysFont("lisu", 40)

    # 按鈕的回撥函式
    def btnCallBack1():
        return True

    # 按鈕的回撥函式
    def btnCallBack2():
        return True


    # 建立按鈕1
    btn1 = Button(200, 450, "", surBtnNormal_1, surBtnDown_1, surBtnDown_1, btnCallBack1,btnFont,(255,0,0))

    # 建立按鈕2
    btn2 = Button(600, 450, "", surBtnNormal_2, surBtnDown_2, surBtnDown_2, btnCallBack2,btnFont,(255,0,0))

    # 遊戲主迴圈
    while True:
        mx, my = pygame.mouse.get_pos()  # 獲得滑鼠座標

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:  # 滑鼠移動事件
                # 判斷滑鼠是否移動到按鈕範圍內
                btn1.getFocus(mx, my)
                btn2.getFocus(mx, my)

            elif event.type == pygame.MOUSEBUTTONDOWN:  # 滑鼠按下
                if pygame.mouse.get_pressed() == (1, 0, 0): #滑鼠左鍵按下
                    btn1.mouseDown(mx,my)
                    btn2.mouseDown(mx,my)

            elif event.type == pygame.MOUSEBUTTONUP:  # 滑鼠彈起
                start1 = btn1.mouseUp()
                start2 = btn2.mouseUp()

                if start1 == True:
                    # winSur.blit( loading, [0,0] )
                    pygame.display.flip()
                    mode = 0
                    return mode
                
                elif start2 == True:
                    pygame.display.flip()
                    mode = 1
                    return mode

        pygame.time.delay(16)
        winSur.blit( background, [0,0] )
        #繪製按鈕
        btn1.draw(winSur)
        btn2.draw(winSur)
        #重新整理介面
        pygame.display.flip()

    #pygame.quit()
    return False