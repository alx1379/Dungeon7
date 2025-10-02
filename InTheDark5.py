import random,pygame
pygame.init()
W,H=800,600;T=10
Wc,Hc=W//T,H//T
s=pygame.display.set_mode((W,H))
clock=pygame.time.Clock()
CH,CW=60,80;C=(0,0,0)

def gen_chunk(cx,cy):
    m=[[1 if random.random()<0.45 else 0 for x in range(CW)] for y in range(CH)]
    for _ in range(5):
        nm=[[0]*CW for _ in range(CH)]
        for y in range(CH):
            for x in range(CW):
                cnt=sum(m[yy][xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2)
                        if 0<=xx<CW and 0<=yy<CH)
                nm[y][x]=1 if cnt>=5 else 0
        m=nm
    mons=[]
    for _ in range(random.randint(1,4)):
        while True:
            x,y=random.randrange(CW),random.randrange(CH)
            if m[y][x]==0:
                mons.append((cx*CW+x,cy*CH+y));break
    return m,mons

chunks={};monsters=[]
def get_tile(gx,gy):
    cx,cy=gx//CW,gy//CH
    lx,ly=gx%CW,gy%CH
    if (cx,cy) not in chunks:
        m,mons=gen_chunk(cx,cy)
        chunks[(cx,cy)]=m
        monsters.extend(mons)
    return chunks[(cx,cy)][ly][lx]

px,py=0,0;r=80
tick=0

def move_monster(x,y):
    if abs(px-x)<8 and abs(py-y)<8:
        dx=1 if px>x else -1 if px<x else 0
        dy=1 if py>y else -1 if py<y else 0
        if get_tile(x+dx,y+dy)==0:return x+dx,y+dy
    return (x,y)

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:pygame.quit();exit()
    k=pygame.key.get_pressed();dx=dy=0
    if k[pygame.K_LEFT]:dx=-1
    if k[pygame.K_RIGHT]:dx=1
    if k[pygame.K_UP]:dy=-1
    if k[pygame.K_DOWN]:dy=1
    if get_tile(px+dx,py+dy)==0:px+=dx;py+=dy

    tick+=1
    if tick%2==0:  # монстры двигаются медленнее
        monsters=[move_monster(x,y) for x,y in monsters]

    if any(mx==px and my==py for mx,my in monsters):  # проверка смерти
        print("GAME OVER!")
        pygame.quit();exit()

    camx,camy=px-Wc//2,py-Hc//2
    s.fill(C)
    for y in range(Hc):
        for x in range(Wc):
            gx,gy=camx+x,camy+y
            if get_tile(gx,gy)==0:
                pygame.draw.rect(s,(200,200,200),(x*T,y*T,T,T))
    for mx,my in monsters:
        if camx<=mx<camx+Wc and camy<=my<camy+Hc:
            pygame.draw.circle(s,(255,0,0),((mx-camx)*T+T//2,(my-camy)*T+T//2),3)

    mask=pygame.Surface((W,H));mask.fill((0,0,0));mask.set_alpha(220)
    pygame.draw.circle(mask,(0,0,0,0),(W//2,H//2),r)
    s.blit(mask,(0,0))
    pygame.draw.circle(s,(255,255,0),(W//2,H//2),4)
    pygame.display.flip();clock.tick(10)

