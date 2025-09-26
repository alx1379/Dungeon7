import pygame,sys,random
pygame.init()
W,H,T=400,400,100
sc=pygame.display.set_mode((W,H))
clk=pygame.time.Clock()
font=pygame.font.SysFont(None,48)

tiles=list(range(1,16))+[0]
random.shuffle(tiles)
def pos(i): return i%4*T, i//4*T

def draw():
    sc.fill((0,0,0))
    for i,v in enumerate(tiles):
        if v==0: continue
        x,y=pos(i)
        pygame.draw.rect(sc,(100,200,255),(x+5,y+5,T-10,T-10))
        txt=font.render(str(v),1,(0,0,0))
        sc.blit(txt,(x+T//3,y+T//4))
    pygame.display.flip()

def move(dx,dy):
    i=tiles.index(0)
    x,y=i%4,i//4
    nx,ny=x+dx,y+dy
    if 0<=nx<4 and 0<=ny<4:
        ni=ny*4+nx
        tiles[i],tiles[ni]=tiles[ni],tiles[i]

def is_solved(): return tiles==list(range(1,16))+[0]

while True:
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
        elif ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_LEFT: move(1,0)
            if ev.key==pygame.K_RIGHT: move(-1,0)
            if ev.key==pygame.K_UP: move(0,1)
            if ev.key==pygame.K_DOWN: move(0,-1)
    draw()
    if is_solved():
        print("You solved it!")
        pygame.time.wait(2000)
        random.shuffle(tiles)
    clk.tick(30)

