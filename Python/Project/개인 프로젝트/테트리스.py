import pygame, random, json, os, time
from gpiozero import Button

WIDTH, HEIGHT = 300, 600
BLOCK = 30
COLS, ROWS = WIDTH // BLOCK, HEIGHT // BLOCK
SCREEN_WIDTH = WIDTH + 150
SCORE_FILE = "highscores.json"

BTN_CFG = {
    'left':  {'pin': 5,  'bounce': 0.1},
    'right': {'pin': 6,  'bounce': 0.1},
    'down':  {'pin': 13, 'bounce': 0.1},
    'rot':   {'pin': 19, 'bounce': 0.1},
    'drop':  {'pin': 26, 'bounce': 0.1},
    'hold':  {'pin': 21, 'bounce': 0.1},
}
btn = {
    name: Button(cfg['pin'], pull_up=True, bounce_time=cfg['bounce'])
    for name, cfg in BTN_CFG.items()
}
last_act = {name: 0 for name in btn}
THRESHOLD = 0.2

COLORS = [(0,255,255),(0,0,255),(255,165,0),(255,255,0),(0,255,0),(128,0,128),(255,0,0)]
SHAPES = [
    [[1,1,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
    [[1,1],[1,1]],
    [[0,1,1],[1,1,0]],
    [[0,1,0],[1,1,1]],
    [[1,1,0],[0,1,1]]
]

class Block:
    def __init__(self, index=None):
        self.x, self.y = 3, 0
        self.index = index if index is not None else random.randrange(len(SHAPES))
        self.shape = SHAPES[self.index]
        self.color = COLORS[self.index]
    def rotate(self):
        self.shape = [list(r) for r in zip(*self.shape[::-1])]

def create_grid(locked):
    grid = [[(0,0,0) for _ in range(COLS)] for _ in range(ROWS)]
    for (x,y), c in locked.items():
        if 0 <= y < ROWS:
            grid[y][x] = c
    return grid

def valid(shape, grid, x, y):
    for i,row in enumerate(shape):
        for j,cell in enumerate(row):
            if cell:
                nx, ny = x + j, y + i
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and grid[ny][nx] != (0,0,0):
                    return False
    return True

def burst_lines(full_rows, anim_grid, screen):
    shards, half = [], BLOCK // 2
    for y in full_rows:
        for x in range(COLS):
            color = anim_grid[y][x]
            if color == (0,0,0): continue
            px, py = x*BLOCK, y*BLOCK
            rects = [
                pygame.Rect(px,py,half,half),
                pygame.Rect(px+half,py,half,half),
                pygame.Rect(px,py+half,half,half),
                pygame.Rect(px+half,py+half,half,half)
            ]
            for r in rects:
                shards.append({
                    'rect': r.copy(),
                    'vel': [random.uniform(-4,4), random.uniform(-8,-4)],
                    'color': color
                })
    clock = pygame.time.Clock()
    for _ in range(12):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
        screen.fill((0,0,0))
        for ry,row in enumerate(anim_grid):
            if ry in full_rows: continue
            for rx,col in enumerate(row):
                if col!=(0,0,0):
                    pygame.draw.rect(screen, col,(rx*BLOCK,ry*BLOCK,BLOCK,BLOCK))
        for s in shards:
            s['vel'][1] += 0.5
            s['rect'].x += int(s['vel'][0])
            s['rect'].y += int(s['vel'][1])
            pygame.draw.rect(screen, s['color'], s['rect'])
        pygame.display.update()
        clock.tick(60)

def clear(grid, locked, screen, score, lines, combo):
    full_rows = [y for y in range(ROWS) if all(c!=(0,0,0) for c in grid[y])]
    removed = len(full_rows)
    if removed > 0:
        anim_grid = [row[:] for row in grid]
        burst_lines(full_rows, anim_grid, screen)
        new_rows = [grid[y] for y in range(ROWS) if y not in full_rows]
        while len(new_rows) < ROWS:
            new_rows.insert(0, [(0,0,0)]*COLS)
        locked.clear()
        for y,row in enumerate(new_rows):
            for x,c in enumerate(row):
                if c!=(0,0,0):
                    locked[(x,y)] = c
        combo += 1
        score += removed * 100 + combo * 50
    else:
        combo = 0
    lines += removed
    return score, lines, combo

def draw_block(screen, color, x, y):
    pygame.draw.rect(screen,(0,0,0),(x,y,BLOCK,BLOCK))
    pygame.draw.rect(screen,color,(x+2,y+2,BLOCK-4,BLOCK-4))

def draw_info(screen, score, lines, pieces, combo):
    font = pygame.font.SysFont("Consolas",20)
    stats = [f"SCORE: {score}",f"LINES: {lines}",f"PIECES: {pieces}",f"COMBO: {combo}"]
    for i,t in enumerate(stats):
        lbl = font.render(t,True,(255,255,255))
        screen.blit(lbl,(WIDTH+10,20+i*30))

def draw_preview(screen, block, x, y):
    if not block: return
    for i,row in enumerate(block.shape):
        for j,cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen,block.color,(x+j*20,y+i*20,20,20))
                pygame.draw.rect(screen,(200,200,200),(x+j*20,y+i*20,20,20),2)

def draw(screen, grid, score, lines, pieces, combo, next_block, hold_block):
    screen.fill((0,0,0))
    for y,row in enumerate(grid):
        for x,c in enumerate(row):
            draw_block(screen,c,x*BLOCK,y*BLOCK)
    for i in range(ROWS+1):
        pygame.draw.line(screen,(40,40,40),(0,i*BLOCK),(WIDTH,i*BLOCK))
    for j in range(COLS+1):
        pygame.draw.line(screen,(40,40,40),(j*BLOCK,0),(j*BLOCK,HEIGHT))
    draw_info(screen,score,lines,pieces,combo)
    draw_preview(screen,next_block,WIDTH+10,150)
    draw_preview(screen,hold_block,WIDTH+10,300)

def load_scores():
    if not os.path.exists(SCORE_FILE): return [] 
    with open(SCORE_FILE,"r") as f: return json.load(f)

def save_scores(scores):
    with open(SCORE_FILE,"w") as f: json.dump(scores[:10],f,ensure_ascii=False,indent=2)

def record_name(screen):
    font=pygame.font.SysFont("Consolas",28)
    clock=pygame.time.Clock()
    name=""
    cx,cy=SCREEN_WIDTH//2,HEIGHT//2
    box=pygame.Rect(cx-100,cy-20,200,40)
    while True:
        screen.fill((30,30,30))
        prompt=font.render("Enter Your Name:",True,(255,255,255))
        screen.blit(prompt,(cx-prompt.get_width()//2,cy-60))
        pygame.draw.rect(screen,(50,50,50),box)
        txt=font.render(name,True,(255,255,255))
        screen.blit(txt,(box.x+5,box.y+5))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit();exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN: return name or "ANON"
                if e.key==pygame.K_BACKSPACE: name=name[:-1]
                elif e.unicode.isprintable() and len(name)<10: name+=e.unicode
        clock.tick(30)

def show_ranking(screen):
    scores=load_scores()
    f1=pygame.font.SysFont("Consolas",36,bold=True)
    f2=pygame.font.SysFont("Consolas",24)
    clock=pygame.time.Clock()
    while True:
        screen.fill((20,20,20))
        title=f1.render("HIGHSCORES",True,(255,200,0))
        screen.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,40))
        for i,e in enumerate(scores):
            txt=f"{i+1:2d}. {e['name'][:10]:<10s} {e['score']:6d}"
            lbl=f2.render(txt,True,(255,255,255))
            screen.blit(lbl,(WIDTH//2-120,100+i*30))
        notice=f2.render("Press any key to continue",True,(180,180,180))
        screen.blit(notice,(SCREEN_WIDTH//2-notice.get_width()//2,HEIGHT-60))
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit();exit()
            if ev.type==pygame.KEYDOWN: return
        clock.tick(30)

def game_over_menu(screen, final_score):
    name=record_name(screen)
    scores=load_scores()
    scores.append({"name":name,"score":final_score})
    scores.sort(key=lambda x:x["score"],reverse=True)
    save_scores(scores)
    show_ranking(screen)
    f1=pygame.font.SysFont("Consolas",48)
    f2=pygame.font.SysFont("Consolas",28)
    clock=pygame.time.Clock()
    while True:
        screen.fill((20,20,20))
        go=f1.render("GAME OVER",True,(255,50,50))
        r =f2.render("Press R to Restart",True,(200,200,200))
        q =f2.render("Press Q to Quit",True,(200,200,200))
        cx=SCREEN_WIDTH//2
        screen.blit(go,(cx-go.get_width()//2,HEIGHT//2-80))
        screen.blit(r ,(cx-r.get_width()//2,HEIGHT//2))
        screen.blit(q ,(cx-q.get_width()//2,HEIGHT//2+40))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit();exit()
            if e.type==pygame.KEYDOWN: return e.key==pygame.K_r
        clock.tick(30)

def main():
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,HEIGHT))
    pygame.display.set_caption("Tetris with GPIO")
    clock=pygame.time.Clock()

    while True:
        current,next_block=Block(),Block()
        hold_block,hold_used=None,False
        locked={}
        fall=score=lines=pieces=combo=0
        start_time=time.time()

        while True:
            grid=create_grid(locked)
            fall+=clock.get_rawtime()
            clock.tick()
            speed=max(0.2,0.5-(time.time()-start_time)/45)

            if fall/1000>speed:
                fall=0
                current.y+=1
                if not valid(current.shape,grid,current.x,current.y):
                    current.y-=1
                    for i,row in enumerate(current.shape):
                        for j,cell in enumerate(row):
                            if cell: locked[(current.x+j,current.y+i)]=current.color
                    grid=create_grid(locked)
                    score,lines,combo=clear(grid,locked,screen,score,lines,combo)
                    pieces+=1
                    current,next_block=next_block,Block()
                    hold_used=False
                    if not valid(current.shape,grid,current.x,current.y):
                        if game_over_menu(screen,score): break
                        else: pygame.quit();return

            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit(); return

            now=time.time()
            if btn['left'].is_pressed   and now-last_act['left']>THRESHOLD:
                last_act['left']=now
                current.x-=1
                if not valid(current.shape,grid,current.x,current.y): current.x+=1
            if btn['right'].is_pressed  and now-last_act['right']>THRESHOLD:
                last_act['right']=now
                current.x+=1
                if not valid(current.shape,grid,current.x,current.y): current.x-=1
            if btn['down'].is_pressed   and now-last_act['down']>THRESHOLD:
                last_act['down']=now
                current.y+=1
                if not valid(current.shape,grid,current.x,current.y): current.y-=1
            if btn['rot'].is_pressed    and now-last_act['rot']>THRESHOLD:
                last_act['rot']=now
                current.rotate()
                if not valid(current.shape,grid,current.x,current.y):
                    for _ in range(3): current.rotate()
            if btn['drop'].is_pressed   and now-last_act['drop']>THRESHOLD:
                last_act['drop']=now
                while valid(current.shape,grid,current.x,current.y+1):
                    current.y+=1
            if btn['hold'].is_pressed   and now-last_act['hold']>THRESHOLD and not hold_used:
                last_act['hold']=now
                hold_used=True
                if hold_block is None:
                    hold_block=Block(current.index)
                    current,next_block=next_block,Block()
                else:
                    current,hold_block=Block(hold_block.index),Block(current.index)
                    current.x,current.y=3,0

            for i,row in enumerate(current.shape):
                for j,cell in enumerate(row):
                    if cell and 0<=current.y+i<ROWS and 0<=current.x+j<COLS:
                        grid[current.y+i][current.x+j]=current.color

            draw(screen,grid,score,lines,pieces,combo,next_block,hold_block)
            pygame.display.update()

if __name__=="__main__":
    main()