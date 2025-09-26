import pygame,sys,random,math
pygame.init()
W,H=640,480
sc=pygame.display.set_mode((W,H))
clk=pygame.time.Clock()
font=pygame.font.SysFont(None,24)

ph,eh=100,100
cdp,atk=0,0
pfists=[{'r':60,'x':W//2-120,'y':H-80,'state':0},
        {'r':60,'x':W//2+120,'y':H-80,'state':0}]
efists=[{'r':40,'x':W//2-60,'y':H//2+120,'state':0},
        {'r':40,'x':W//2+60,'y':H//2+120,'state':0}]

face_pos={'x':0,'y':0}
face_target={'x':0,'y':0}
face_timer=0
face_shake_x,face_shake_y=0,0
shake_x,shake_y=0,0
shake_fx,shake_fy=0,0

pupil_l_pos={'x':0,'y':0}
pupil_r_pos={'x':0,'y':0}
scratches=[]           # enemy face scratches
screen_scratches=[]    # player screen scratches

def draw():
    offset_x,offset_y=shake_x,shake_y
    sc.fill((0,0,0))
    pygame.draw.rect(sc,(255,0,0),(50+offset_x,30+offset_y,ph*2,20))
    pygame.draw.rect(sc,(0,255,0),(W-250+offset_x,30+offset_y,eh*2,20))
    cx,cy=W//2+face_pos['x']+face_shake_x+offset_x,H//2+face_pos['y']+face_shake_y+offset_y

    # enemy face
    pygame.draw.circle(sc,(255,220,200),(cx,cy),120)
    for sx,sy,l,ang in scratches:
        ex=cx+sx+math.cos(ang)*l
        ey=cy+sy+math.sin(ang)*l
        pygame.draw.line(sc,(150,0,0),(cx+sx,cy+sy),(ex,ey),2)

    ex_shift=face_pos['x']//5
    ey_shift=face_pos['y']//5
    eye_l=(cx-40+ex_shift,cy-40+ey_shift)
    eye_r=(cx+40+ex_shift,cy-40+ey_shift)
    pygame.draw.circle(sc,(0,0,0),eye_l,20)
    pygame.draw.circle(sc,(0,0,0),eye_r,20)
    pygame.draw.circle(sc,(255,255,255),(int(eye_l[0]+pupil_l_pos['x']),int(eye_l[1]+pupil_l_pos['y'])),5)
    pygame.draw.circle(sc,(255,255,255),(int(eye_r[0]+pupil_r_pos['x']),int(eye_r[1]+pupil_r_pos['y'])),5)
    pygame.draw.rect(sc,(0,0,0),(cx-50+ex_shift,cy+40+ey_shift,100,20))

    for f in efists:
        pygame.draw.circle(sc,(200,50,50),(f['x']+offset_x,f['y']+offset_y),f['r'])
    for f in pfists:
        pygame.draw.circle(sc,(200,200,200),(f['x']+offset_x,f['y']+offset_y),f['r'])

    # draw player screen scratches
    for sx,sy,l,ang in screen_scratches:
        ex=sx+math.cos(ang)*l
        ey=sy+math.sin(ang)*l
        pygame.draw.line(sc,(255,50,50),(sx,sy),(ex,ey),3)

    sc.blit(font.render(f"Player:{ph} Enemy:{eh}",1,(255,255,255)),(W//2-70+offset_x,5+offset_y))
    pygame.display.flip()

def punch():
    global face_shake_x,face_shake_y,scratches
    f=random.choice(pfists)
    f['r']=90
    f['x']=W//2+random.randint(-40,40)
    f['y']=H//2+random.randint(-40,40)
    f['state']=1
    face_shake_x=random.randint(-f['r'],f['r'])
    face_shake_y=random.randint(-f['r']//2,f['r']//2)
    scratches.append((random.randint(-100,100),random.randint(-100,100),
                      random.randint(10,40), random.uniform(0,6.28)))

def enemy_attack():
    global ph,shake_fx,shake_fy,screen_scratches
    f=random.choice(efists)
    f['r']=120; f['y']=H//2+30; f['state']=1
    dmg=f['r']//10; ph=max(0,ph-dmg)
    shake_fx=random.randint(-f['r']//2,f['r']//2)
    shake_fy=random.randint(-f['r']//2,f['r']//2)
    # add long scratches across screen
    for _ in range(random.randint(1,3)):
        sx=random.randint(0,W)
        sy=random.randint(0,H)
        l=random.randint(80,200)
        ang=random.uniform(-0.5,0.5)
        screen_scratches.append((sx,sy,l,ang))

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit();sys.exit()
        if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE and cdp==0:
            punch(); cdp=20
    if cdp>0: cdp-=1

    if face_timer==0:
        face_target['x']=random.choice([-30,0,30])
        face_target['y']=random.choice([-20,0,10])
        face_timer=random.randint(20,40)
    else:
        face_pos['x']+=(face_target['x']-face_pos['x'])//10
        face_pos['y']+=(face_target['y']-face_pos['y'])//10
        face_timer-=1

    face_shake_x//=2; face_shake_y//=2
    shake_x+=(-shake_x+shake_fx)//5; shake_y+=(-shake_y+shake_fy)//5
    shake_fx//=2; shake_fy//=2

    pupil_l_pos['x']+=(-face_pos['x']//5 - pupil_l_pos['x'])//5
    pupil_l_pos['y']+=(-face_pos['y']//5 - pupil_l_pos['y'])//5
    pupil_r_pos['x']+=(-face_pos['x']//5 - pupil_r_pos['x'])//5
    pupil_r_pos['y']+=(-face_pos['y']//5 - pupil_r_pos['y'])//5

    for i,f in enumerate(pfists):
        if f['state']==1:
            f['r']-=5; f['y']+=4
            if f['r']<=30:
                dmg=max(5,25-f['r']); eh=max(0,eh-dmg)
                f['state']=0
        else:
            idle_x=W//2-120 if i==0 else W//2+120
            if f['r']<60: f['r']+=2
            if f['y']<H-80: f['y']+=2
            f['x']+=(idle_x-f['x'])//5

    for i,f in enumerate(efists):
        if f['state']==1:
            f['r']-=3; f['y']+=2
            if f['r']<=40: f['state']=0
        else:
            idle_x=W//2-60 if i==0 else W//2+60
            if f['r']<40: f['r']+=2
            if f['y']<H//2+120: f['y']+=2
            f['x']+=(idle_x-f['x'])//5

    atk+=1
    if atk>60: enemy_attack(); atk=0
    draw()

    if ph<=0 or eh<=0:
        msg="You Win!" if eh<=0 else "You Lose!"
        sc.fill((0,0,0)); sc.blit(font.render(msg,1,(255,255,255)),(W//2-40,H//2))
        pygame.display.flip(); pygame.time.wait(2000)
        ph,eh=100,100
        pfists=[{'r':60,'x':W//2-120,'y':H-80,'state':0},
                {'r':60,'x':W//2+120,'y':H-80,'state':0}]
        efists=[{'r':40,'x':W//2-60,'y':H//2+120,'state':0},
                {'r':40,'x':W//2+60,'y':H//2+120,'state':0}]
        face_pos={'x':0,'y':0}
        face_target={'x':0,'y':0}
        face_shake_x,face_shake_y=0,0
        shake_x,shake_y,shake_fx,shake_fy=0,0,0,0
        pupil_l_pos={'x':0,'y':0}
        pupil_r_pos={'x':0,'y':0}
        scratches=[]
        screen_scratches=[]
        atk=0

    clk.tick(30)

