import cv2
import numpy as np
import kociemba

import constants

state = {
    'up':['white','white','white','white','white','white','white','white','white',],
    'right':['white','white','white','white','white','white','white','white','white',],
    'front':['white','white','white','white','white','white','white','white','white',],
    'down':['white','white','white','white','white','white','white','white','white',],
    'left':['white','white','white','white','white','white','white','white','white',],
    'back':['white','white','white','white','white','white','white','white','white',]
}

checkState = []
solution = []
solved = False

camera = cv2.VideoCapture(0)
cv2.namedWindow("Cube Solver")

def draw_stickers(frame, stickers, name):
    for x,y in stickers[name]:
        cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)

def draw_preview_stickers(frame, stickers):
    stick=['front','back','left','right','up','down']
    for name in stick:
        for x,y in stickers[name]:
            cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)

def fill_stickers(frame, stickers, sides): 
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(frame,(x,y),(x+40,y+40),constants.colorCodes[colors[num]],-1)
            num+=1

def text_on_preview_stickers(frame, stickers):
    stick=['front','back','left','right','up','down']
    for name in stick:
        for x,y in stickers[name]:
            sym,x1,y1 = constants.onScreenSignifiers[name][0][0],constants.onScreenSignifiers[name][0][1],constants.onScreenSignifiers[name][0][2]
            cv2.putText(preview, sym, (x1,y1), constants.FONT,1,(0, 0, 0), 1, cv2.LINE_AA)  
            sym,col,x1,y1=constants.onScreenSignifiers[name][1][0],constants.onScreenSignifiers[name][1][1],constants.onScreenSignifiers[name][1][2],constants.onScreenSignifiers[name][1][3]             
            cv2.putText(preview, sym, (x1,y1), constants.FONT,0.5,col, 1, cv2.LINE_AA) 
            
def color_detect(h, s, v):
    if h < 5 and s>5 :
        return 'red'
    elif h <10 and h>=3:
        return 'orange'
    elif h <= 25 and h>10:
        return 'yellow'
    elif h>=70 and h<= 85 and s>100 and v<180:
        return 'green'
    elif h <= 130 and s>70:
        return 'blue'
    elif h <= 100 and s<10 and v<200:
        return 'white'

    return 'white'

def solve(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=constants.signLegend[j]
    return kociemba.solve(raw)

def rotate(side):
    main=state[side]
    front=state['front']
    left=state['left']
    right=state['right']
    up=state['up']
    down=state['down']
    back=state['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=down[0],down[1],down[2],left[8],left[5],left[2],up[6],up[7],up[8],right[6],right[3],right[0] 
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=front[0],front[1],front[2],left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8],left[6],left[7],left[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=up[2],up[1],up[0],right[2],right[5],right[8],down[8],down[7],down[6],left[0],left[3],left[6] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=up[0],up[3],up[6],front[0],front[3],front[6],down[6],down[3],down[0],back[8],back[5],back[2]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=down[2],down[5],down[8],back[6],back[3],back[0],up[8],up[5],up[2],front[2],front[5],front[8]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[6],main[3],main[0],main[7],main[4],main[1],main[8],main[5],main[2]

def revrotate(side):
    main=state[side]
    front=state['front']
    left=state['left']
    right=state['right']
    up=state['up']
    down=state['down']
    back=state['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=up[8],up[7],up[6],right[0],right[3],right[6],down[2],down[1],down[0],left[2],left[5],left[8]
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2],left[0],left[1],left[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=front[6],front[7],front[8],left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=down[6],down[7],down[8],left[6],left[3],left[0],up[0],up[1],up[2],right[8],right[5],right[2] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=down[0],down[3],down[6],back[8],back[5],back[2],up[0],up[3],up[6],front[0],front[3],front[6]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=up[2],up[5],up[8],front[2],front[5],front[8],down[8],down[5],down[2],back[6],back[3],back[0]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[2],main[5],main[8],main[1],main[4],main[7],main[0],main[3],main[6]


def process(operation):
    replace={
                "F":[rotate,'front'],
                "F2":[rotate,'front','front'],
                "F'":[revrotate,'front'],
                "U":[rotate,'up'],
                "U2":[rotate,'up','up'],
                "U'":[revrotate,'up'],
                "L":[rotate,'left'],
                "L2":[rotate,'left','left'],
                "L'":[revrotate,'left'],
                "R":[rotate,'right'],
                "R2":[rotate,'right','right'],
                "R'":[revrotate,'right'],
                "D":[rotate,'down'],
                "D2":[rotate,'down','down'],
                "D'":[revrotate,'down'],
                "B":[rotate,'back'],
                "B2":[rotate,'back','back'],
                "B'":[revrotate,'back']           
    }    
    a=0
    for i in operation:
        for j in range(len(replace[i])-1):
            replace[i][0](replace[i][j+1])
        cv2.putText(preview, i, (700,a+50), constants.FONT,1,(0,255,0), 1, cv2.LINE_AA)  
        fill_stickers(preview,constants.stickerLocation,state)
        solution.append(preview)
        cv2.imshow('solution',preview)
        cv2.waitKey()
        cv2.putText(preview, i, (700,50), constants.FONT,1,(0,0,0), 1, cv2.LINE_AA)  

if __name__ == "__main__":
    preview = np.zeros((700,800,3), np.uint8)
    while True:
        hsv = []
        currentState = []
        ret, img = camera.read()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)
        
        draw_stickers(img, constants.stickerLocation, 'main')
        draw_stickers(img, constants.stickerLocation, 'current')
        draw_preview_stickers(preview, constants.stickerLocation)
        fill_stickers(preview, constants.stickerLocation, state)
        text_on_preview_stickers(preview, constants.stickerLocation)
        
        for i in range(9):
            hsv.append(frame[constants.stickerLocation['main'][i][1]+10][constants.stickerLocation['main'][i][0]+10])
            
        a=0
        for x,y in constants.stickerLocation['current']:
            color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
            cv2.rectangle(img,(x,y),(x+30,y+30),constants.colorCodes[color_name],-1)
            a+=1
            currentState.append(color_name)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k ==ord('u'):
            state['up']=currentState
            checkState.append('u')
        elif k ==ord('r'):
            checkState.append('r')
            state['right']=currentState
        elif k ==ord('l'):
            checkState.append('l')
            state['left']=currentState
        elif k ==ord('d'):
            checkState.append('d')
            state['down']=currentState       
        elif k ==ord('f'):
            checkState.append('f')
            state['front']=currentState       
        elif k ==ord('b'):
            checkState.append('b')
            state['back']=currentState       
        elif k == ord('\r'):
            # process(["R","R'"])
            if len(set(checkState))==6:    
                try:
                    solved=solve(state)
                    if solved:
                        operation=solved.split(' ')
                        process(operation)
                except:
                    print("error in side detection ,you may do not follow sequence or some color not detected well.Try again")
            else:
                print("all side are not scanned check other window for finding which left to be scanned?")
                print("left to scan:",6-len(set(checkState)))
        cv2.imshow('preview',preview)
        cv2.imshow('frame',img[0:500,0:500])

    cv2.destroyAllWindows()