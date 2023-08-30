from pygame.locals import *
import pygame
import sys
import numpy as np
import random
import time

pygame.init()
GameLoop=False
#画面表示-----------------
Scale=0.7##########################画面に合わせてサイズ調整
Sc_height=950
Sc_width=Sc_height/2
n_h=20          #高さN数
n_w=10  #横N数
#-------------------------
#フォントサイズ---------------------
fontsize=50
font = pygame.font.Font(None,fontsize)
#ブロック----------------
b_h=Sc_height/n_h
b_w=Sc_width/n_w
b_n=4 #回転用(ブロック正方形1辺長さ)
block_color=((10,0,0))

#スタート画面--------------
screen    = pygame.display.set_mode((int(Scale*(Sc_width*2+600)),int(Scale*(Sc_height+50)))) #ゲーム画面 
screen.fill((10,10,100))
fonts = pygame.font.Font(None,int(Scale*(250)))
texts = fonts.render('TETORIS',True,(200,55,55))
screen.blit(texts,[int(Scale*(350)),int(Scale*(300))])      

fontss = pygame.font.Font(None,int(Scale*(100)))
textss = fontss.render('vs COMPUTER',True,(255,255,255))
screen.blit(textss,[int(Scale*(500)),int(Scale*(500+100))])   


#back_color=(240,255,240)#背景色
back_color=(100,100,100)#背景色
pygame.display.update()

# 初期設定----------------
i,j=int(n_w/3),1
i_me,j_me=int(n_w/3),1
i_pc,j_pc=int(n_w/3),1

#block_choice=1
block_N=6 #ブロックの種類
hold_time=0

# ①ブロック
BlockLoca=np.zeros([n_h+2,n_w+2])
BlockLoca_me=np.zeros([n_h+2,n_w+2])
BlockLoca_pc=np.zeros([n_h+2,n_w+2])
# ②ブロック(1ターン進行)
BlockLoca_pro=np.zeros([n_h+2,n_w+2])
BlockLoca_pro_me=np.zeros([n_h+2,n_w+2])
BlockLoca_pro_pc=np.zeros([n_h+2,n_w+2])
# ③背景
BackDisp=np.zeros([n_h+2,n_w+2]) 
BackDisp[:,0]=1
BackDisp[:,n_w+1]=1
BackDisp[n_h+1,:]=1
BackDisp_me=np.zeros([n_h+2,n_w+2]) 
BackDisp_me[:,0]=1
BackDisp_me[:,n_w+1]=1
BackDisp_me[n_h+1,:]=1
BlockLoca_drop_laca_me=np.zeros([n_h+2,n_w+2]) 
BackDisp_pc=np.zeros([n_h+2,n_w+2]) 
BackDisp_pc[:,0]=1
BackDisp_pc[:,n_w+1]=1
BackDisp_pc[n_h+1,:]=1
BackDisp_pro_pc=np.zeros([n_h+2,n_w+2]) 
# ④表示用(背景+ブロック)
ShowDisp=np.zeros([n_h+2,n_w+2])
ShowDisp_me=np.zeros([n_h+2,n_w+2])
ShowDisp_pc=np.zeros([n_h+2,n_w+2])

Block_small=np.zeros([b_n,b_n])
Block_small_rotate=np.zeros([b_n,b_n])
Block_small_pc=np.zeros([b_n,b_n])
Block_small_rotate_pc=np.zeros([b_n,b_n])
Block_small_me=np.zeros([b_n,b_n])
Block_small_rotate_me=np.zeros([b_n,b_n])

me=False
me_GameOver=False
FirstStage_Clear=False
SecondStage_Clear=False
FinalStage_Clear=False
PredeterStage_Clear=False
stage=0
DL_me=0
DL_pc=0
block_put_me=False
block_put_pc=False
delete_me=False
delete_pc=False
counter_me=False
counter_pc=False

#行列 初期状態
i_me,j_me=int(n_w/3),2
i_pc,j_pc=int(n_w/3),2
block_choice_now_me=random.randint(1,block_N)
block_choice_next_me=random.randint(1,block_N)
block_choice_hold_me=0
block_choice_hold_me_pre=0
hold_times_me=0
 
block_choice_now_pc=random.randint(1,block_N)
block_choice_next_pc=random.randint(1,block_N)
block_choice_hold_pc=0
hold_times_pc=0

 
#ini_block_me(block_choice_now_me)
#ini_block_pc(block_choice_now_pc,i_pc,j_pc)

line_me,point_me,line_pc,point_pc=0,0,0,0
delay_me=500
#---------------------------

def ini_block_pc(block_choice_pc,i_pc,j_pc):   
    # L字型
    if block_choice_pc==1:
        BlockLoca_pc[j_pc][i_pc+1]=1.01
        BlockLoca_pc[j_pc+1][i_pc+1]=1.01
        BlockLoca_pc[j_pc+2][i_pc+1]=1.01
        BlockLoca_pc[j_pc+2][i_pc+2]=1.01
    # o字型  
    if block_choice_pc==2:   
        BlockLoca_pc[j_pc+1][i_pc+1]=1.02
        BlockLoca_pc[j_pc+2][i_pc+1]=1.02
        BlockLoca_pc[j_pc+2][i_pc+2]=1.02
        BlockLoca_pc[j_pc+1][i_pc+2]=1.02
    # I字型 
    if block_choice_pc==3:
        BlockLoca_pc[j_pc+2][i_pc]=1.03
        BlockLoca_pc[j_pc+2][i_pc+1]=1.03
        BlockLoca_pc[j_pc+2][i_pc+2]=1.03
        BlockLoca_pc[j_pc+2][i_pc+3]=1.03
    # 逆Z字型
    if block_choice_pc==4:
        BlockLoca_pc[j_pc][i_pc+1]=1.04
        BlockLoca_pc[j_pc+1][i_pc+1]=1.04
        BlockLoca_pc[j_pc+1][i_pc+2]=1.04
        BlockLoca_pc[j_pc+2][i_pc+2]=1.04
    # Z字型
    if block_choice_pc==5:
        BlockLoca_pc[j_pc][i_pc+2]=1.05
        BlockLoca_pc[j_pc+1][i_pc+2]=1.05
        BlockLoca_pc[j_pc+1][i_pc+1]=1.05
        BlockLoca_pc[j_pc+2][i_pc+1]=1.05
    # T字型
    if block_choice_pc==6:
        BlockLoca_pc[j_pc][i_pc+1]=1.06
        BlockLoca_pc[j_pc+1][i_pc]=1.06
        BlockLoca_pc[j_pc+1][i_pc+1]=1.06
        BlockLoca_pc[j_pc+1][i_pc+2]=1.06 
        
def ini_block_me(block_choice_me):   
    # L字型
    if block_choice_me==1:
        BlockLoca_me[j_me][i_me+1]=1.01
        BlockLoca_me[j_me+1][i_me+1]=1.01
        BlockLoca_me[j_me+2][i_me+1]=1.01
        BlockLoca_me[j_me+2][i_me+2]=1.01
    # o字型
    if block_choice_me==2:   
        BlockLoca_me[j_me+1][i_me+1]=1.02
        BlockLoca_me[j_me+2][i_me+1]=1.02
        BlockLoca_me[j_me+2][i_me+2]=1.02
        BlockLoca_me[j_me+1][i_me+2]=1.02
    # I字型
    if block_choice_me==3:
        BlockLoca_me[j_me][i_me+2]=1.03
        BlockLoca_me[j_me+1][i_me+2]=1.03
        BlockLoca_me[j_me+2][i_me+2]=1.03
        BlockLoca_me[j_me+3][i_me+2]=1.03
    # 逆Z字型
    if block_choice_me==4:
        BlockLoca_me[j_me][i_me+1]=1.04
        BlockLoca_me[j_me+1][i_me+1]=1.04
        BlockLoca_me[j_me+1][i_me+2]=1.04
        BlockLoca_me[j_me+2][i_me+2]=1.04
    # Z字型
    if block_choice_me==5:
        BlockLoca_me[j_me][i_me+2]=1.05
        BlockLoca_me[j_me+1][i_me+2]=1.05
        BlockLoca_me[j_me+1][i_me+1]=1.05
        BlockLoca_me[j_me+2][i_me+1]=1.05
    # T字型
    if block_choice_me==6:
        BlockLoca_me[j_me][i_me+1]=1.06
        BlockLoca_me[j_me+1][i_me+1]=1.06
        BlockLoca_me[j_me+1][i_me+2]=1.06
        BlockLoca_me[j_me+2][i_me+1]=1.06


def move_state_pc():
 right,left,down,p_rotate,m_rotate=False,False,False,False,False    
 d_n=4
 if d_n==1: right=True #右進行
 if d_n==2: left=True #左進行 
# if d_n==3: down=True #下進行  
 if d_n==4: p_rotate=True #右回転  
 if d_n==5: m_rotate=True #左回転
 return right,left,down,p_rotate,m_rotate
     
def move_state_me():
 right_me,left_me,down_me,drop_me,p_rotate_me,m_rotate_me=False,False,False,False,False,False      
 if event.key==pygame.K_RIGHT: right_me=True #右進行
 if event.key==pygame.K_LEFT: left_me=True #左進行 
 if event.key==pygame.K_DOWN: down_me=True #下進行  
 if event.key==pygame.K_UP: drop_me=True #急落下
 if event.key==pygame.K_f: p_rotate_me=True #右回転  
 if event.key==pygame.K_s: m_rotate_me=True #左回転
 return right_me,left_me,down_me,drop_me,p_rotate_me,m_rotate_me
 
def block_90deg_rotate_pc(i_pc,j_pc,b_n,BlockLoca_pc):#右回転
 if i_pc<n_w-(b_n-2) and i_pc>0 and j_pc<n_h-(b_n-2):#壁判定   
  Block_small_pc[0:b_n,0:b_n]=BlockLoca_pc[j_pc:j_pc+b_n,i_pc:i_pc+b_n]#small行列抽出
  for k in range (0,b_n,1):
   Block_small_rotate_pc[k,:]=Block_small_pc[::-1,k]

  BlockLoca_pro_pc[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro_pc[j_pc:j_pc+b_n,i_pc:i_pc+b_n]=Block_small_rotate_pc[:,:]
  if np.all((BlockLoca_pro_pc[:,:]+BackDisp_pc[:,:])<2):
   BlockLoca_pc[:,:]=BlockLoca_pro_pc[:,:]
 return BlockLoca_pc

def block_m90deg_rotate_pc(i_pc,j_pc,b_n,BlockLoca_pc):#左回転
 if i_pc<n_w-(b_n-2) and i_pc>0 and j_pc<n_h-(b_n-2):   
  Block_small_pc[0:b_n,0:b_n]=BlockLoca_pc[j_pc:j_pc+b_n,i_pc:i_pc+b_n]
  for k in range (0,b_n,1):
   Block_small_rotate_pc[:,k]=Block_small_pc[k,::-1]
   
  BlockLoca_pro_pc[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro_pc[j_pc:j_pc+b_n,i_pc:i_pc+b_n]=Block_small_rotate_pc[:,:]
  if np.all((BlockLoca_pro_pc[:,:]+BackDisp_pc[:,:])<2):
   BlockLoca_pc[:,:]=BlockLoca_pro_pc[:,:]
 return BlockLoca_pc

def block_90deg_rotate_me(i_me,j_me,b_n_me):#右回転
# if block_choice_me==6:
#  b_n=3
 Block_small_me=np.zeros([b_n_me,b_n_me])
 Block_small_rotate_me=np.zeros([b_n_me,b_n_me])
 if i_me<n_w-(b_n_me-2) and i_me>0 and j_me<n_h-(b_n_me-2):   
  Block_small_me[0:b_n_me,0:b_n_me]=BlockLoca_me[j_me:j_me+b_n_me,i_me:i_me+b_n_me]
  for k in range (0,b_n_me,1):
    Block_small_rotate_me[k,:]=Block_small_me[::-1,k]
  BlockLoca_pro_me[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro_me[j_me:j_me+b_n_me,i_me:i_me+b_n_me]=Block_small_rotate_me[:,:]
  if np.all((BlockLoca_pro_me[:,:]+BackDisp_me[:,:])<2): 
   BlockLoca_me[:,:]=BlockLoca_pro_me[:,:]
 return BlockLoca_me 
 
def block_m90deg_rotate_me(i_me,j_me,b_n_me):#左回転
 #if block_choice_me==6:
 # b_n=3
 Block_small_me=np.zeros([b_n_me,b_n_me])
 Block_small_rotate_me=np.zeros([b_n_me,b_n_me])
 if i_me<n_w-(b_n_me-2) and i_me>0 and j_me<n_h-(b_n_me-2):   
  Block_small_me[0:b_n_me,0:b_n_me]=BlockLoca_me[j_me:j_me+b_n_me,i_me:i_me+b_n_me]
  for k in range (0,b_n_me,1):
   Block_small_rotate_me[:,k]=Block_small_me[k,::-1]
  BlockLoca_pro_me[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro_me[j_me:j_me+b_n_me,i_me:i_me+b_n_me]=Block_small_rotate_me[:,:]
  if np.all((BlockLoca_pro_me[:,:]+BackDisp_me[:,:])<2): 
   BlockLoca_me[:,:]=BlockLoca_pro_me[:,:]
 return BlockLoca_me 
 
 
def block_move_pc(i_pc,j_pc,right_pc,left_pc,down_pc,n_h,n_w):
 i_pc_new,j_pc_new = i_pc,j_pc
 BlockLoca_pro_pc=np.zeros([n_h+2,n_w+2])     
# print(BlockLoca_me)
 #1マス移動---------------------
 if right_pc==True:i_pc_new=i_pc+1
 if left_pc==True: i_pc_new=i_pc-1
 if down_pc==True: j_pc_new=j_pc+1
  #ブロックを仮に移動
 for m in range (1,n_w+1,1):
  for n in range (1,n_h+1,1): 
   if int(BlockLoca_pc[n][m])==1:
    BlockLoca_pro_pc[n+(j_pc_new-j_pc)][m+(i_pc_new-i_pc)]=BlockLoca_pc[n][m]

 for k in range (0,n_h+2,1):
  if max(BlockLoca_pro_pc[k,:]+BackDisp_pc[k,:])>=2:
   i_pc_new,j_pc_new = i_pc,j_pc
   BlockLoca_pro_pc[:,:]=BlockLoca_pc[:,:]
   break
 #print(BlockLoca_pro_me)
# BlockLoca_pro_me[:,:]
 return i_pc_new,j_pc_new,BlockLoca_pro_pc



def block_move_me(i_me,j_me,right_me,left_me,down_me,drop_me,n_h,n_w): 
 i_me_new,j_me_new = i_me,j_me
 BlockLoca_pro_me=np.zeros([n_h+2,n_w+2])     
# print(BlockLoca_me)
 #ドロップ----------------------
 if drop_me==True:
  #ブロックを仮に移動   
  for pro in range (1,n_h+2,1):
   BlockLoca_pro_me[0+pro:n_h+2,:]=BlockLoca_me[0:n_h+2-pro,:]
   if np.any((BlockLoca_pro_me+BackDisp_me)>=2):
     BlockLoca_pro_me=np.zeros([n_h+2,n_w+2]) 
     BlockLoca_pro_me[0+(pro-1):n_h+2,:]=BlockLoca_me[0:n_h+2-(pro-1),:]
     i_me_new,j_me_new=i_me,j_me+pro-1
     break
    
 #1マス移動---------------------
 if right_me==True: i_me_new=i_me+1
 if left_me==True: i_me_new=i_me-1
 if down_me==True: j_me_new=j_me+1
  #ブロックを仮に移動
 for m in range (1,n_w+1,1):
  for n in range (1,n_h+1,1): 
   if BlockLoca_me[n][m]>=1:
    BlockLoca_pro_me[n+(j_me_new-j_me)][m+(i_me_new-i_me)]=BlockLoca_me[n][m]

 for k in range (0,n_h+2,1):
  if max(BlockLoca_pro_me[k,0:n_w+2]+BackDisp_me[k,0:n_w+2])>=2:
   i_me_new,j_me_new = i_me,j_me
   BlockLoca_pro_me[:,:]=BlockLoca_me[:,:]
   break

 return i_me_new,j_me_new,BlockLoca_pro_me


def block_drop_pc(BlockLoca_pc,BackDisp_pc,i_pc,j_pc):
 BlockLoca_pro_pc=np.zeros([n_h+2,n_w+2])
 for pro in range (1,n_h+1,1):
  BlockLoca_pro_pc[0+pro:n_h+2,:]=BlockLoca_pc[0:n_h+2-pro,:]
  if np.any((BlockLoca_pro_pc+BackDisp_pc)>=2):
     BlockLoca_pc=np.zeros([n_h+2,n_w+2]) 
     BlockLoca_pc[0:n_h+1,:]=BlockLoca_pro_pc[1:n_h+2,:]
     break
 return BlockLoca_pc



#色定義
#L
color_L1=(150,50,0)
color_L2=(200,85,0)
color_L3=(100,30,0)
#O
color_O1=(150,150,0)
color_O2=(200,200,0)
color_O3=(100,100,0)
#I
color_I1=(0,150,150)
color_I2=(0,200,200)
color_I3=(0,100,100)
#逆Z
color_Z1=(150,10,0)
color_Z2=(200,15,0)
color_Z3=(100,10,0)
#Z
color_oZ1=(10,150,0)
color_oZ2=(15,200,0)
color_oZ3=(30,100,0)
#T
color_T1=(150,50,150)
color_T2=(200,85,200)
color_T3=(100,30,100)
#ダメージ
color_d1=(100,100,100)
color_d2=(150,150,150)
color_d3=(20,20,20)
def show_display_me(line_me,point_me,block_choice_next_me,block_choice_hold_me):
    
#プレイ画面背景
 #back_color=((0,0,70)) 
 screen_left  = pygame.draw.rect(screen,(back_color),(int(Scale*150),int(Scale*25),int(Scale*Sc_width),int(Scale*Sc_height)))          # 左プレイ画面

#線描画
 #line_color=(150,150,150)
 for l in range (0,n_w+1,1):
     pygame.draw.line(screen,line_color, (int(Scale*(b_w*l+150)),int(Scale*25)), (int(Scale*(b_w*l+150)),int(Scale*(Sc_height+25))),1)#左縦線
 for k in range (0,n_h+1,1):
     pygame.draw.line(screen,line_color, (int(Scale*150),int(Scale*(b_h*k+25))), (int(Scale*(Sc_width+150)),int(Scale*(b_h*k+25))),1)#左横線

 
#ブロック描画

 ShowDisp_me[:,:]=BackDisp_me[:,:]+BlockLoca_me[:,:]
 thick=3


 #左ブロック
 for k in range (1,n_h+1,1):
   for l in range (1,n_w+1,1):
    ##落下位置表示
    rakkaichi=False       
    if BlockLoca_drop_laca_me[k][l]==1.01:#L
       color_2=color_L2
       rakkaichi=True
    elif BlockLoca_drop_laca_me[k][l]==1.02:#O
       color_2=color_O2
       rakkaichi=True
    elif BlockLoca_drop_laca_me[k][l]==1.03:#I
       color_2=color_I2
       rakkaichi=True
    elif BlockLoca_drop_laca_me[k][l]==1.04:#Z
       color_2=color_Z2
       rakkaichi=True
    elif BlockLoca_drop_laca_me[k][l]==1.05:#逆Z
       color_2=color_oZ2
       rakkaichi=True
    elif BlockLoca_drop_laca_me[k][l]==1.06:#T
       color_2=color_T2
       rakkaichi=True
    if rakkaichi==True:
        pygame.draw.rect(screen,color_2,pygame.Rect(int(Scale*((l-1)*b_w+150)),int(Scale*((k-1)*b_h+25)),int(Scale*b_w),int(Scale*b_h)),int(Scale*4))#コア
    ##ブロック表示   
    draw_block_me=False
    if ShowDisp_me[k][l]==1.01:      
        color_1=color_L1
        color_2=color_L2  
        color_3=color_L3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.02:
        color_1=color_O1
        color_2=color_O2
        color_3=color_O3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.03:
        color_1=color_I1
        color_2=color_I2
        color_3=color_I3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.04:
        color_1=color_Z1
        color_2=color_Z2  
        color_3=color_Z3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.05:
        color_1=color_oZ1
        color_2=color_oZ2  
        color_3=color_oZ3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.06:
        color_1=color_T1
        color_2=color_T2  
        color_3=color_T3
        draw_block_me=True
    
    elif ShowDisp_me[k][l]==1.07:
        color_1=color_d1
        color_2=color_d2  
        color_3=color_d3
        draw_block_me=True  
       
    if draw_block_me==True:  
       pygame.draw.rect(screen,color_1,pygame.Rect(int(Scale*(150+(l-1)*b_w)),int(Scale*((k-1)*b_h+25)),int(Scale*b_w),int(Scale*b_h)))#コア
       pygame.draw.rect(screen,color_2,pygame.Rect(int(Scale*(150+(l-1)*b_w)),int(Scale*((k-1)*b_h+25)),int(Scale*b_w),int(Scale*thick)))#上辺
       pygame.draw.rect(screen,color_2,pygame.Rect(int(Scale*(150+(l-1)*b_w)),int(Scale*((k-1)*b_h+25)),int(Scale*thick),int(Scale*b_h)))#左辺
       pygame.draw.rect(screen,color_3,pygame.Rect(int(Scale*(150+(l-0)*b_w-thick)),int(Scale*((k-1)*b_h+25)),int(Scale*thick),int(Scale*b_h)))#右辺
       pygame.draw.rect(screen,color_3,pygame.Rect(int(Scale*(150+(l-1)*b_w)),int(Scale*((k-0)*b_h+25-thick)),int(Scale*b_w),int(Scale*thick)))#下辺



#得点
 font1 = pygame.font.Font(None,int(Scale*40))
 font2 = pygame.font.Font(None,int(Scale*60))
 #me得点
 pygame.draw.rect(screen,back_color,(int(Scale*(Sc_width+170)),int(Scale*(Sc_height-125)),int(Scale*110),int(Scale*150)))#左
 text_me1 = font1.render("Lines:",True,(255,255,255))
 text_me2 = font2.render(str(line_me),True,(255,255,255))
 text_me3 = font1.render("Points:",True,(255,255,255))
 text_me4 = font2.render(str(point_me),True,(255,255,255))
 screen.blit(text_me1,[int(Scale*(Sc_width+170)),int(Scale*(Sc_height-125))])
 screen.blit(text_me2,[int(Scale*(Sc_width+170)),int(Scale*(Sc_height-100))])
 screen.blit(text_me3,[int(Scale*(Sc_width+170)),int(Scale*(Sc_height-50))])
 screen.blit(text_me4,[int(Scale*(Sc_width+170)),int(Scale*(Sc_height-25))])
 
 next_left1  =   pygame.draw.rect(screen,(back_color),(int(Scale*(Sc_width+170)),int(Scale*100),int(Scale*110),int(Scale*150))) 
 text_left1  =   font1.render("Next",True,(255,255,255))
 screen.blit(text_left1, [int(Scale*(Sc_width+170)),int(Scale*100)])
 if block_choice_next_me==1:
    text_left11=font1.render("L",True,(255,255,255))
 elif block_choice_next_me==2:
    text_left11=font1.render("O",True,(255,255,255))    
 elif block_choice_next_me==3:
    text_left11=font1.render("I",True,(255,255,255))    
 elif block_choice_next_me==4:
    text_left11=font1.render("opZ",True,(255,255,255))    
 elif block_choice_next_me==5:
    text_left11=font1.render("Z",True,(255,255,255))    
 elif block_choice_next_me==6:
    text_left11=font1.render("T",True,(255,255,255))    
 screen.blit(text_left11, [int(Scale*(Sc_width+170)),int(Scale*150)])

 #block_hold
 hold_left2  =   pygame.draw.rect(screen,(back_color),(int(Scale*(170-150)),int(Scale*100),int(Scale*110),int(Scale*150))) 
 text_left2  =   font1.render("Hold",True,(255,255,255))
 screen.blit(text_left2, [int(Scale*(170-150)),int(Scale*100)])
 if block_choice_hold_me==1:
    text_left22=font1.render("L",True,(255,255,255))     
 elif block_choice_hold_me==2:
    text_left22=font1.render("O",True,(255,255,255))  
 elif block_choice_hold_me==3:
    text_left22=font1.render("I",True,(255,255,255)) 
 elif block_choice_hold_me==4:
    text_left22=font1.render("opZ",True,(255,255,255))  
 elif block_choice_hold_me==5:
    text_left22=font1.render("Z",True,(255,255,255))   
 elif block_choice_hold_me==6:
    text_left22=font1.render("T",True,(255,255,255))   
 elif block_choice_hold_me==0:
    text_left22=font1.render(" ",True,(255,255,255)) #無し 
 screen.blit(text_left22, [int(Scale*(170-150)),int(Scale*150)])

 pygame.display.update()



def show_display_pc(line_pc,point_pc,block_choice_next_pc,block_choice_hold_pc):

#プレイ画面背景
 #back_color=((0,0,70))
 screen_right = pygame.draw.rect(screen,(back_color),(int(Scale*(Sc_width+450)),int(Scale*25),int(Scale*Sc_width),int(Scale*Sc_height))) # 右プレイ画面

#線描画
 #line_color=(150,150,150)

 for l in range (0,n_w+1,1):
     pygame.draw.line(screen,line_color,(int(Scale*(b_w*l+450+Sc_width)),int(Scale*25)),(int(Scale*(b_w*l+450+Sc_width)),int(Scale*(Sc_height+25))),1)#右縦線
 for k in range (0,n_h+1,1):
     pygame.draw.line(screen,line_color,(int(Scale*(450+Sc_width)),int(Scale*(b_h*k+25))),(int(Scale*(Sc_width+Sc_width+450)),int(Scale*(b_h*k+25))),1)#右横線

#ブロック描画
 ShowDisp_pc[:,:]=BackDisp_pc[:,:]+BlockLoca_pc[:,:]

 thick=3

 #右ブロック
 for k in range (1,n_h+1,1):
  for l in range (1,n_w+1,1):
   draw_block=False
   if ShowDisp_pc[k][l]==1.01:      
    color_1=color_L1
    color_2=color_L2  
    color_3=color_L3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.02:
    color_1=color_O1
    color_2=color_O2
    color_3=color_O3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.03:
    color_1=color_I1
    color_2=color_I2  
    color_3=color_I3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.04:
    color_1=color_Z1
    color_2=color_Z2  
    color_3=color_Z3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.05:
    color_1=color_oZ1
    color_2=color_oZ2  
    color_3=color_oZ3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.06:
    color_1=color_T1
    color_2=color_T2  
    color_3=color_T3
    draw_block=True
    
   elif ShowDisp_pc[k][l]==1.07:
    color_1=color_d1
    color_2=color_d2  
    color_3=color_d3
    draw_block=True  
       
   if draw_block==True:  
       pygame.draw.rect(screen,color_1,pygame.Rect(int(Scale*((l-1)*b_w+Sc_width+450)),int(Scale*((k-1)*b_h+25)),int(Scale*b_w),Scale*b_h))#コア
       pygame.draw.rect(screen,color_2,pygame.Rect(int(Scale*((l-1)*b_w+Sc_width+450)),int(Scale*((k-1)*b_h+25)),int(Scale*b_w),Scale*thick))#上辺
       pygame.draw.rect(screen,color_2,pygame.Rect(int(Scale*((l-1)*b_w+Sc_width+450)),int(Scale*((k-1)*b_h+25)),int(Scale*thick),Scale*b_h))#左辺
       pygame.draw.rect(screen,color_3,pygame.Rect(int(Scale*((l-0)*b_w+Sc_width+450-thick)),int(Scale*((k-1)*b_h+25)),int(Scale*thick),Scale*b_h))#右辺
       pygame.draw.rect(screen,color_3,pygame.Rect(int(Scale*((l-1)*b_w+Sc_width+450)),int(Scale*((k-0)*b_h+25-thick)),int(Scale*b_w),Scale*thick))#下辺

#得点
 font1 = pygame.font.Font(None,int(Scale*40))
 font2 = pygame.font.Font(None,int(Scale*60))

 #pc得点
 pygame.draw.rect(screen,back_color,pygame.Rect(int(Scale*(Sc_width*2+300+170)),int(Scale*(Sc_height-125)),int(Scale*110),int(Scale*150)))#右
 text_pc1 = font1.render("Lines:",True,(255,255,255))
 text_pc2 = font2.render(str(line_pc),True,(255,255,255))
 text_pc3 = font1.render("Points:",True,(255,255,255))
 text_pc4 = font2.render(str(point_pc),True,(255,255,255))
 screen.blit(text_pc1,[int(Scale*(Sc_width*2+300+170)),int(Scale*(Sc_height-125))])
 screen.blit(text_pc2,[int(Scale*(Sc_width*2+300+170)),int(Scale*(Sc_height-100))])
 screen.blit(text_pc3,[int(Scale*(Sc_width*2+300+170)),int(Scale*(Sc_height-50))])
 screen.blit(text_pc4,[int(Scale*(Sc_width*2+300+170)),int(Scale*(Sc_height-25))])

 next_right1 =   pygame.draw.rect(screen,(back_color),(int(Scale*(Sc_width*2+300+170)),int(Scale*100),int(Scale*110),int(Scale*150)))
 text_right1 =   font1.render("Next",True,(255,255,255))
 screen.blit(text_right1, [int(Scale*(Sc_width*2+300+170)),int(Scale*100)])
 if block_choice_next_pc==1:
    text_right11=font1.render("L",True,(255,255,255))
 elif block_choice_next_pc==2:
    text_right11=font1.render("O",True,(255,255,255))    
 elif block_choice_next_pc==3:
    text_right11=font1.render("I",True,(255,255,255))    
 elif block_choice_next_pc==4:
    text_right11=font1.render("opZ",True,(255,255,255))    
 elif block_choice_next_pc==5:
    text_right11=font1.render("Z",True,(255,255,255))    
 elif block_choice_next_pc==6:
    text_right11=font1.render("T",True,(255,255,255))    
 screen.blit(text_right11, [int(Scale*(Sc_width*2+300+170)),int(Scale*150)])

 #block_hold
 hold_right2 =   pygame.draw.rect(screen,(back_color),(int(Scale*(Sc_width+300+170-150)),int(Scale*100),int(Scale*110),int(Scale*150)))
 text_right2 =   font1.render("Hold",True,(255,255,255))
 screen.blit(text_right2, [int(Scale*(Sc_width+300+170-150)),int(Scale*100)])
 if block_choice_hold_pc==1:
    text_right22=font1.render("L",True,(255,255,255))     
 elif block_choice_hold_pc==2:
    text_right22=font1.render("O",True,(255,255,255))  
 elif block_choice_hold_pc==3:
    text_right22=font1.render("I",True,(255,255,255)) 
 elif block_choice_hold_pc==4:
    text_right22=font1.render("opZ",True,(255,255,255))  
 elif block_choice_hold_pc==5:
    text_right22=font1.render("Z",True,(255,255,255))   
 elif block_choice_hold_pc==6:
    text_right22=font1.render("T",True,(255,255,255))   
 elif block_choice_hold_pc==0:
    text_right22=font1.render(" ",True,(255,255,255)) #無し 
 screen.blit(text_right22, [int(Scale*(Sc_width+300+170-150)),int(Scale*150)])

 pygame.display.update() 



def escape():
  pygame.quit()
  sys.exit()

def damage(DL_me,DL_pc):       
 if DL_me-DL_pc>0:#0 PCダメージ
              UP_pc=DL_me-DL_pc              
             #  delete_pc=True
             #  counter_me=True
              for k in range (1,n_w+1,1):
               BackDisp_pc[0:n_h-UP_pc+1,k]=BackDisp_pc[UP_pc:n_h+1,k]  
               BackDisp_pc[n_h+1-UP_pc:n_h+1,k]=1.07
              kk=int(random.randint(1,n_w)) 
              BackDisp_pc[n_h+1-UP_pc:n_h+1,kk]=0
              if np.any((BackDisp_pc+BlockLoca_pc)>2):
               for k in range (1,n_w+1,1):
                BlockLoca_pc[0:n_h-UP_pc+1,k]=BlockLoca_pc[UP_pc:n_h+1,k]
             # print("DL_me,DL_pc,UP_me,UP_pc",DL_me,DL_pc,0,UP_pc)
             

 if DL_pc-DL_me>0:#0 Meダメージ
            UP_me=DL_pc-DL_me    
            for k in range (1,n_w+1,1):
             BackDisp_me[0:n_h-UP_me+1,k]=BackDisp_me[UP_me:n_h+1,k]  
             BackDisp_me[n_h+1-UP_me:n_h+1,k]=1.07        
            k=int(random.randint(1,n_w)) 
            BackDisp_me[n_h+1-UP_me:n_h+1,k]=0
            if np.any((BackDisp_me+BlockLoca_me)>2):
              for k in range (1,n_w+1,1):
               BlockLoca_me[0:n_h-UP_me+1,k]=BlockLoca_me[UP_me:n_h+1,k]
            #print("DL_me,DL_pc,UP_me,UP_pc",DL_me,DL_pc,UP_me,0)
 counter_me,counter_pc,delete_me,delete_pc=False,False,False,False
 if DL_me>0 or DL_pc>0:DL_me,DL_pc=0,0
 return DL_me,DL_pc,counter_me,counter_pc,delete_me,delete_pc 

def init():
 BackDisp_pc[:,:]=np.zeros([n_h+2,n_w+2])
 BackDisp_pc[:,0]=1
 BackDisp_pc[:,n_w+1]=1
 BackDisp_pc[n_h+1,:]=1
 BlockLoca_pro_pc[:,:]=np.zeros([n_h+2,n_w+2])
 BlockLoca_pc[:,:]=np.zeros([n_h+2,n_w+2])

 BackDisp_me[:,:]=np.zeros([n_h+2,n_w+2])
 BackDisp_me[:,0]=1
 BackDisp_me[:,n_w+1]=1
 BackDisp_me[n_h+1,:]=1
 BlockLoca_pro_me[:,:]=np.zeros([n_h+2,n_w+2])
 BlockLoca_me[:,:]=np.zeros([n_h+2,n_w+2])

 i_me,j_me=int(n_w/3),2
 i_pc,j_pc=int(n_w/3),2
 block_choice_now_me=random.randint(1,block_N)
 block_choice_next_me=random.randint(1,block_N)
 block_choice_hold_me=0
 hold_times_me=0
 block_choice_now_pc=random.randint(1,block_N)
 block_choice_next_pc=random.randint(1,block_N)
 block_choice_hold_pc=0
 hold_times_pc=0
 ini_block_me(block_choice_now_me)
 ini_block_pc(block_choice_now_pc,i_pc,j_pc)



# メインプログラム--------------------------------------------------------------------

while True:
    
  #screen.fill((10,10,100))  
  #meゲームオーバー画面--------------    
  if me_GameOver==True:
    screen.fill((10,10,100))  
    font = pygame.font.Font(None,int(Scale*(100)))
    text = font.render(str(point_me),True,(255,255,255))
    screen.blit(text,[int(Scale*(700)),int(Scale*(370))])

    fonts = pygame.font.Font(None,int(Scale*(100)))
    texts = fonts.render('Your Score',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-100))])

    fonts = pygame.font.Font(None,int(Scale*(50)))
    texts = fonts.render('You lose...play again',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-200))])         
    line_me,point_me,line_pc,point_pc=0,0,0,0
    me_GameOver=False

  #1stStageクリア画面--------------
  elif FirstStage_Clear==True:
    screen.fill((10,60,10))  
    font = pygame.font.Font(None,int(Scale*(100)))
    text = font.render(str(point_me),True,(255,255,255))
    screen.blit(text,[int(Scale*(700)),int(Scale*(370))])

    fonts = pygame.font.Font(None,int(Scale*(100)))
    texts = fonts.render('Your Score',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-100))])

    fonts = pygame.font.Font(None,int(Scale*(50)))
    texts = fonts.render('GooD!!',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-100)),int(Scale*(370-200))])      
    FirstStage_Clear=False
    
  #2ndStageクリア画面--------------
  elif SecondStage_Clear==True:
    screen.fill((60,10,10))  
    font = pygame.font.Font(None,int(Scale*(100)))
    text = font.render(str(point_me),True,(255,255,255))
    screen.blit(text,[int(Scale*(700)),int(Scale*(370))])

    fonts = pygame.font.Font(None,int(Scale*(100)))
    texts = fonts.render('Your Score',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-100))])

    fonts = pygame.font.Font(None,int(Scale*(50)))
    texts = fonts.render('GreaThhh!!',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-120)),int(Scale*(370-200))])             
    SecondStage_Clear=False

  #FinalStageクリア画面--------------
  elif FinalStage_Clear==True:
    screen.fill((60,60,10))  
    fonts = pygame.font.Font(None,int(Scale*(100)))
    texts = fonts.render('Your Score',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-100))])

    fonts = pygame.font.Font(None,int(Scale*(50)))
    texts = fonts.render('ExcellentTTThhhh!!GameClear!!!',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-200))])      
    FinalStage_Clear=False

  #プレデターモード画面--------------
  elif PredeterStage_Clear==True:
    screen.fill((60,10,60))  
    font = pygame.font.Font(None,int(Scale*(100)))
    text = font.render(str(point_me),True,(255,255,255))
    screen.blit(text,[int(Scale*(700)),int(Scale*(370))])
    
    fonts = pygame.font.Font(None,int(Scale*(100)))
    texts = fonts.render('Your Score',True,(255,255,255))
    screen.blit(texts,[int(Scale*(700-150)),int(Scale*(370-100))])

    fontss = pygame.font.Font(None,int(Scale*(50)))
    textss = fontss.render('UnbelievableEEEEEEE!!!',True,(255,255,255))
    screen.blit(textss,[int(Scale*(700-150)),int(Scale*(370-200))])         
    PredeterStage_Clear=False


  pygame.display.update()     

  hold_times_pc=0
  hold_times_me=0
  block_choice_hold_pc=0
  block_choice_hold_me=0

  #stage=3 ################################
  for event in pygame.event.get():
   if event.type == KEYDOWN:
    init()   
    if event.key == K_SPACE:#ゲームスタート
        #ゲーム画面背景-----------------------------
        if stage==0:
          screen.fill((10,10,100))    
          back_color=((0,0,30))  
          line_color=((150,150,150)) 
          font01 = pygame.font.Font(None,int(Scale*(60)))
          text01 = font01.render("STAGE1",True,(255,255,255),back_color)
          screen.blit(text01,[int(Scale*(Sc_width+230)),int(Scale*(Sc_height/2))])
           
        elif stage==1:
          screen.fill((10,60,10)) 
          back_color=((0,0,30))      
          line_color=((150,150,150))
          font01 = pygame.font.Font(None,int(Scale*(60)))
          text01 = font01.render("STAGE2",True,(255,255,255),back_color)
          screen.blit(text01,[int(Scale*(Sc_width+230)),int(Scale*(Sc_height/2))])
          
        elif stage==2:
          screen.fill((60,10,10))  
          back_color=((0,0,30))  
          line_color=((200,130,0))            
          font01 = pygame.font.Font(None,int(Scale*(60)))
          text01 = font01.render("FINAL STAGE",True,(250,0,0),back_color)
          screen.blit(text01,[int(Scale*(Sc_width+170)),int(Scale*(Sc_height/2))])

          
        elif stage>=3:
          screen.fill((60,10,60))            
          back_color=((0,0,30))  
          line_color=((180,180,180))            
          font01 = pygame.font.Font(None,int(Scale*(60)))
          text01 = font01.render("EXTRA STAGE",True,(0,200,200),back_color)
          screen.blit(text01,[int(Scale*(Sc_width+150)),int(Scale*(Sc_height/2))])

        font02 = pygame.font.Font(None,int(Scale*(80)))
        text_me = font02.render("YOU",True,line_color)
        screen.blit(text_me,[int(Scale*(10)),0])

        font03 = pygame.font.Font(None,int(Scale*(80)))
        text_pc = font03.render("COM",True,line_color)
        screen.blit(text_pc,[int(Scale*(Sc_width+300)),0])



        show_display_me(line_me,point_me,block_choice_next_me,block_choice_hold_me)
        show_display_pc(line_pc,point_pc,block_choice_next_pc,block_choice_hold_pc)  

        GameLoop=True
    if event.type == QUIT or event.key == K_ESCAPE: escape()

    
  while GameLoop==True:
      
     time=pygame.time.get_ticks()

     #ブロック落下位置表示----------
     for pro in range (1,n_h+2,1):
        BlockLoca_drop_laca_me[0+pro:n_h+2,:]=BlockLoca_me[0:n_h+2-pro,:]
        if np.any((BlockLoca_drop_laca_me+BackDisp_me)>=2):
           BlockLoca_drop_laca_me=np.zeros([n_h+2,n_w+2]) 
           BlockLoca_drop_laca_me[0+(pro-1):n_h+2,:]=BlockLoca_me[0:n_h+2-(pro-1),:]
           break                         

    #meブロック自動落下(操作は別途下)-------------------- 
     if stage<3:interval=1100-stage*300    
     if stage>=3:interval=400
     if np.mod(time,interval)==0:     
       right_me,left_me,down_me,drop_me,p_rotate_me,m_rotate_me=False,False,True,False,False,False  
       i_me_new,j_me_new,BlockLoca_pro_me= block_move_me(i_me,j_me,right_me,left_me,down_me,drop_me,n_h,n_w)
       i_me,j_me=i_me_new,j_me_new
       BlockLoca_me[:,:]=BlockLoca_pro_me[:,:]  
       #ブロック置き---------------
#       BlockLoca_me,BackDisp_me=block_put_me_(BlockLoca_me,BackDisp_me)
       block_put_me=False
       for k in range(n_h,1,-1):
          for l in range(1,n_w+1,1):   
           if BlockLoca_me[k,l]>=1 and BackDisp_me[k+1,l]>=1:
            #背景にブロック書く
            if np.mod(time,delay_me)==0 or drop_me==True:   
             BackDisp_me=BackDisp_me+BlockLoca_me 
             #初期化
             i_me,j_me,i_me_new,j_me_new=int(n_w/2),2,int(n_w/2),2   
             BlockLoca_me=np.zeros([n_h+2,n_w+2])

             block_choice_now_me=block_choice_next_me
             block_choice_next_me=random.randint(1,block_N)
             hold_times_me=0
             
             ini_block_me(block_choice_now_me)
             block_put_me=True
             if delete_pc==True:counter_me=True
             break
          if  block_put_me==True:break

       #ブロック消し---------------
       delete_lines_me=0    
       for k in range (1,n_h+1,1):        
          if np.all(BackDisp_me[k,1:n_w+1]>1):
            BackDisp_me[1:k+1,1:n_w+1]=BackDisp_me[0:k,1:n_w+1]
            delete_lines_me=delete_lines_me+1
            delete_me=True
       line_me=line_me+delete_lines_me
       point_me=point_me+(delete_lines_me**2)*10
       #-----------------------------
       show_display_me(line_me,point_me,block_choice_next_me,block_choice_hold_me)
       #ゲームオーバー---------------
       if np.any((BackDisp_me[1,1:n_w+1])>0): 
          me_GameOver=True
          stage=0
          GameLoop=False
          


    #pcブロック落とし
     if stage==0:interval_pc=2000
     if stage==1:interval_pc=1500
     if stage==2:interval_pc=1000
     if stage>=3:interval_pc=800
     if np.mod(time,interval_pc)==0: #秒置きに      
       #ブロック落とし方評価------------------------------
      List      =np.zeros([(n_w)*4*2,13]) #ブロック位置(=n_w)*rotate_N(=4)*hold(=2),評価値13個
      value_List=np.zeros([(n_w)*4*2])
      value=0
      deadspace=0
      takasa=np.zeros([n_w+1])

      for hold in range(0,2):#hold有無
        if hold==0:#0:holdなし
          block_choice_pc=block_choice_now_pc
        if hold==1:#1:holdあり
          if hold_times_pc==0:  
            if block_choice_hold_pc==0:
               block_choice_pc=block_choice_next_pc
            if block_choice_hold_pc>0:
               block_choice_pc=block_choice_hold_pc
          if hold_times_pc==1:
             block_choice_pc=block_choice_now_pc

        for move_N in range(0,n_w):#ブロック位置
             for rotate_N in range(0,4):#ブロック回転
               value=0
               BlockLoca_pc=np.zeros([n_h+2,n_w+2])
               i_pc,j_pc=int(n_w/3),2
               ini_block_pc(block_choice_pc,i_pc,j_pc)

               for k in range(0,rotate_N+1): 
                 BlockLoca_pro_pc[:,:]=block_90deg_rotate_pc(i_pc,j_pc,b_n,BlockLoca_pc)

               i_pc_ini,j_pc_ini=i_pc,j_pc
               i_pc,j_pc=1*move_N,2

               d_i_pc=i_pc-i_pc_ini
               d_j_pc=j_pc-j_pc_ini
               BlockLoca_pc=np.zeros([n_h+2,n_w+2])
               
               for m in range (1,n_w+1,1):
                 for n in range (1,n_h+1,1):
                   if BlockLoca_pro_pc[n][m]>=1:
                     if n+d_j_pc>=0 and n+d_j_pc<=n_h+1 and \
                        m+d_i_pc>=0 and m+d_i_pc<=n_w+1:  
                        BlockLoca_pc[n+d_j_pc][m+d_i_pc]=BlockLoca_pro_pc[n][m]
                        i_pc=i_pc_ini+d_i_pc
                        j_pc=j_pc_ini+d_j_pc
                     else:
                         BlockLoca_pc=BlockLoca_pro_pc  
                         i_pc=i_pc_ini
                         j_pc=j_pc_ini

               #仮にドロップさせる--------------
               BlockLoca_pc[:,:] =block_drop_pc(BlockLoca_pc,BackDisp_pc,i_pc,j_pc)
               BackDisp_pro_pc[:,:]=BlockLoca_pc[:,:]+BackDisp_pc[:,:]

              #評価---------------
               delete_lines=0
               for k in range (1,n_h+1,1):        
                if np.all(BackDisp_pro_pc[k,:]>=1):
                 delete_lines=delete_lines+1
                 BackDisp_pro_pc[1:k+1,1:n_w+1]=BackDisp_pro_pc[0:k,1:n_w+1]
               value_delete=(delete_lines**3)*1 #F1:ブロック消し加点

               sukima=0
               hikusa=0  
               for m in range (1,n_w+1,1):                
                for n in range (1,n_h+1,1): 
                 if BlockLoca_pc[n][m]>=1:
                  if BackDisp_pc[n+1][m]>=1:sukima=sukima+1#F2:隙間少なさ加点
                  if BackDisp_pc[n][m+1]>=1:sukima=sukima+1
                  if BackDisp_pc[n][m-1]>=1:sukima=sukima+1
                  hikusa=hikusa+n#F3:低さ加点


               tetoris_bonus=0 #F4:テトリスボーナス            
               for n in range (4,n_h+1-4,1): 
                if np.all(BackDisp_pro_pc[n,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+1,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+2,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+3,1:n_w+1]>=1):
                  tetoris_bonus=1
 

               deadspace=0
               #F11:deadspace
               for m in range (1,n_w+1,1):
                for n in range (n_h,1,-1):
                 if BackDisp_pro_pc[n][m]==0:
                   i=n  
                   d_deadspace=0 
                   while BackDisp_pro_pc[i][m]==0:  
                     d_deadspace=d_deadspace+1
                     if i<1:
                         d_deadspace=0
                         break
                     i=i-1
                   deadspace=deadspace+d_deadspace  

                       
               for m in range (1,n_w+1,1):#F22:突出列の数 
                for n in range (1,n_h+1,1):
                 if BackDisp_pro_pc[n][m]==1:
                   takasa[m]=n_h-n+1
                   break 
               takasa_sum=sum(takasa)
               
               takasa_ave=takasa_sum/n_w
               tosyutsu=0 
               for m in range (1,n_w+1,1): 
                    for n in range (1,n_h-int(takasa_ave+4)+1,1): 
                     if BackDisp_pro_pc[n][m]==1:
                         tosyutsu=tosyutsu+1

                         
               takasa_migi=np.zeros([n_w+1])
               takasa_migi[0:n_w]=takasa[1:n_w+1]
               koteisa=np.zeros([n_w])                     
               koteisa[:]=abs(takasa_migi[0:n_w]-takasa[0:n_w])#F33:高低差
               koteisa_sum=sum(koteisa[1:n_w+1])

               four_mizo=0 #F44:左右に 4 マスの溝を作成できる
               for n in range (4,(n_h+1)-3,1):
                #右端に溝/左端に溝              
                if np.all(BackDisp_pro_pc[n,1:n_w]==1) and BackDisp_pro_pc[n,n_w]==0 and \
                   np.all(BackDisp_pro_pc[n+1,1:n_w]==1) and BackDisp_pro_pc[n+1,n_w]==0 and \
                   np.all(BackDisp_pro_pc[n+2,1:n_w]==1) and BackDisp_pro_pc[n+2,n_w]==0 and  \
                   np.all(BackDisp_pro_pc[n+3,1:n_w]==1) and BackDisp_pro_pc[n+3,n_w]==0 or \
                   BackDisp_pro_pc[n,1]==0 and np.all(BackDisp_pro_pc[n,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+1,1]==0 and np.all(BackDisp_pro_pc[n+1,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+2,1]==0 and np.all(BackDisp_pro_pc[n+2,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+3,1]==0 and np.all(BackDisp_pro_pc[n+3,2:n_w+1]==1):
                   four_mizo=1
               
               #F1:ブロック消し加点
               #F2:隙間少なさ加点
               #F3:低さ加点    
               #F4:テトリスボーナス   

               #F11:デッドスペースの数
               #F22:突出列の数    
               #F33:高低差
               #F44:左右に 4 マスの溝を作成できる
                            
               F1=value_delete
               F2=sukima
               F3=hikusa
               F4=tetoris_bonus

               F11=deadspace
               F22=tosyutsu    
               F33=koteisa_sum
               F44=four_mizo
               
               #a1,a2,a3,a4=90,20,20,1000000
               a1,a2,a3,a4=200,0,50,0
               a11,a22,a33,a44=-80,-10,-10,5
               #a11,a22,a33,a44=0,0,0,0

               value=a1*F1+a2*F2+a3*F3+a4*F4+a11*F11+a22*F22+a33*F33+a44*F44 

               if np.any((BlockLoca_pc[:,:]+BackDisp_pc[:,:])>=2):value=-10000000 #重複防止

               #評価値リスト               
               List[move_N+rotate_N*n_w+hold*4*n_w][0]=i_pc
               List[move_N+rotate_N*n_w+hold*4*n_w][1]=rotate_N
               List[move_N+rotate_N*n_w+hold*4*n_w][2]=int(value)
               List[move_N+rotate_N*n_w+hold*4*n_w][3]=value_delete
               List[move_N+rotate_N*n_w+hold*4*n_w][4]=sukima 
               List[move_N+rotate_N*n_w+hold*4*n_w][5]=hikusa
               List[move_N+rotate_N*n_w+hold*4*n_w][6]=tetoris_bonus
               List[move_N+rotate_N*n_w+hold*4*n_w][7]=deadspace
               List[move_N+rotate_N*n_w+hold*4*n_w][8]=tosyutsu
               List[move_N+rotate_N*n_w+hold*4*n_w][9]=koteisa_sum   
               List[move_N+rotate_N*n_w+hold*4*n_w][10]=four_mizo
               List[move_N+rotate_N*n_w+hold*4*n_w][11]=hold #hold有無
               List[move_N+rotate_N*n_w+hold*4*n_w][12]=block_choice_pc


      #点数の高いものを選ぶ-------------
      value_List[:]=List[:,2]             #block_choice_pc=random.randint(1,3)#######
      index=np.argmax(value_List)
      i_pc,j_pc=int(List[index][0]),2
      rotate_N =int(List[index][1])
      value    =int(List[index][2])
      block_choice_pc=int(List[index][12])


      value_delete=int(List[index][3])    
      sukima   =int(List[index][4])
      hikusa=int(List[index][5])    
      tetoris_bonus=int(List[index][6])

      hold=int(List[index][11])

#      deadspace=int(List[index][7])    
 #     tosyutsu   =int(List[index][8])
  #    koteisa_sum=int(List[index][9])    
   #   four_mizo=int(List[index][10])
      
      #print(value_List)
      #print(List[index,1])
      #print("del_line,sukima,hikusa,tetoris_bonus",List[index][3:7]) 
      #print("deadspace,tosyutu,koteisa,four_mizo",List[index][3:7])  

      
      #正式にドロップさせる-----------------
      BlockLoca_pc=np.zeros([n_h+2,n_w+2])
      i_pc,j_pc=int(n_w/3),2
      ini_block_pc(block_choice_pc,i_pc,j_pc)

      for k in range(0,rotate_N+1):
        BlockLoca_pro_pc[:,:]=block_90deg_rotate_pc(i_pc,j_pc,b_n,BlockLoca_pc)
        show_display_pc(line_pc,point_pc,block_choice_next_pc,block_choice_hold_pc)
        pygame.time.wait(10)

      i_pc_ini,j_pc_ini=i_pc,j_pc
      i_pc,j_pc=int(List[index][0]),2

      d_i_pc=i_pc-i_pc_ini
      d_j_pc=j_pc-j_pc_ini
      BlockLoca_pc=np.zeros([n_h+2,n_w+2])
               
      for m in range (1,n_w+1,1):
        for n in range (1,n_h+1,1):
          if BlockLoca_pro_pc[n][m]>=1:
             BlockLoca_pc[n+d_j_pc][m+d_i_pc]=BlockLoca_pro_pc[n][m]
      
      #print(BlockLoca_pc)


      
      show_display_pc(line_pc,point_pc,block_choice_next_pc,block_choice_hold_pc)       
      #pygame.time.wait(10) 
      BlockLoca_pc[:,:] =block_drop_pc(BlockLoca_pc,BackDisp_pc,i_pc,j_pc)
            
      #ブロック置き---------------
      block_put_pc=False
      for k in range(n_h,1,-1):
           for l in range(1,n_w+1,1):   
            if BlockLoca_pc[k,l]>=1 and BackDisp_pc[k+1,l]>=1:#当たり判定
            #背景にブロック書く
             BackDisp_pc=BackDisp_pc+BlockLoca_pc 
             #初期化
             i_pc,j_pc,i_pc_new,j_pc_new=int(n_w/2)-1,1,int(n_w/2)-1,1   
             BlockLoca_pc=np.zeros([n_h+2,n_w+2])

             if hold==0:#holdしなかった　　　
               block_choice_now_pc=block_choice_next_pc
               block_choice_next_pc=random.randint(1,block_N)
               hold_times_pc=0
             if hold==1:#holdした　　　　
               block_choice_hold_pc=block_choice_now_pc
               block_choice_now_pc=random.randint(1,block_N)
               block_choice_next_pc=random.randint(1,block_N)
               hold_times_pc=1

             ini_block_pc(block_choice_now_pc,i_pc,j_pc)
             block_put_pc=True
             if delete_me==True:counter_pc=True
             break
           if  block_put_pc==True:break 
        #  print(i_pc,j_pc) 
           
     #ブロック消し---------------
      delete_lines_pc=0
      for k in range (1,n_h+1,1):        
       if np.all(BackDisp_pc[k,1:n_w+1]>=1):
        BackDisp_pc[1:k+1,1:n_w+1]=BackDisp_pc[0:k,1:n_w+1]
        delete_lines_pc=delete_lines_pc+1
        delete_pc=True
      line_pc=line_pc+delete_lines_pc
      point_pc=point_pc+(delete_lines_pc**2)*10
      DL_pc=DL_pc+delete_lines_pc##

     #ダメージ-----------------
      if counter_pc==True and delete_me==True or \
         counter_me==True and delete_pc==True:
          DL_me,DL_pc,counter_me,counter_pc,delete_me,delete_pc=damage(DL_me,DL_pc)

          
     #画面写し--------------------
#      print(BackDisp_pc)
      show_display_pc(line_pc,point_pc,block_choice_next_pc,block_choice_hold_pc)
#      print(BlockLoca_pc[:,:]+BackDisp_pc[:,:]) 

      #COMゲームオーバーー---------------
      if np.any((BackDisp_pc[1,1:n_w+1])>0) or \
         np.any(BlockLoca_pc[:,:]+BackDisp_pc[:,:]>=2):
         pc_GameOver=True
         stage=stage+1
         me_GameOver=False
         FirststStage_Clear=False
         SecondStage_Clear=False
         FinalStage_Clear=False
         
         if stage==1:FirstStage_Clear=True
         if stage==2:SecondStage_Clear=True
         if stage==3:FinalStage_Clear=True
         if stage>3:PredeterStage_Clear=True
         line_pc,point_pc=0,0
         DL_me,DL_pc=0,0
         GameLoop=False
         

    ##プレイヤー操作
 
     for event in pygame.event.get():
       if event.type == KEYDOWN :
           
         right_me,left_me,down_me,drop_me,p_rotate_me,m_rotate_me = move_state_me()
         #ブロック移動(BlockLoca_proを計算し、i_new,j_newを求める)----------     
         i_me_new,j_me_new,BlockLoca_pro_me= block_move_me(i_me,j_me,right_me,left_me,down_me,drop_me,n_h,n_w)
         i_me,j_me=i_me_new,j_me_new
         BlockLoca_me[:,:]=BlockLoca_pro_me[:,:]
    #     print(BlockLoca_me)
          
         #ブロックHold---------------
         if event.key == K_LSHIFT:
           if hold_times_me<1:
            second_if=True 
            if block_choice_hold_me<1:  
              block_choice_hold_me=block_choice_now_me
              block_choice_now_me=block_choice_next_me
              second_if=False
              
            if block_choice_hold_me>=1 and second_if==True :
              block_choice_hold_me_pre=block_choice_hold_me  
              block_choice_hold_me    =block_choice_now_me
              block_choice_now_me     =block_choice_hold_me_pre
            i_me=i_me+2*int((n_w/3-i_me)/abs(n_w/3-i_me+0.01))+1
            hold_times_me=hold_times_me+1

           BlockLoca_me=np.zeros([n_h+2,n_w+2])
           ini_block_me(block_choice_now_me)
              
         #ブロック回転---------------
         if p_rotate_me==True:
          if block_choice_now_me==6:
           b_n_me=3
          else:b_n_me=4
          block_90deg_rotate_me(i_me,j_me,b_n_me)
         if m_rotate_me==True:
          if block_choice_now_me==6:
           b_n_me=3
          else:b_n_me_now=4   
          block_m90deg_rotate_me(i_me,j_me,b_n_me)

         #ブロック落下位置表示----------
         for pro in range (1,n_h+2,1):
           BlockLoca_drop_laca_me[0+pro:n_h+2,:]=BlockLoca_me[0:n_h+2-pro,:]
           if np.any((BlockLoca_drop_laca_me+BackDisp_me)>=2):
             BlockLoca_drop_laca_me=np.zeros([n_h+2,n_w+2]) 
             BlockLoca_drop_laca_me[0+(pro-1):n_h+2,:]=BlockLoca_me[0:n_h+2-(pro-1),:]
             break
          
         #ブロック置き---------------
         block_put_me=False
        
         for k in range(1,n_h+1,1):
          for l in range(1,n_w+1,1):   
           if BlockLoca_me[k,l]>=1 and BackDisp_me[k+1,l]>=1:
            if np.mod(time,delay_me)==0 or drop_me==True:
             #背景にブロック書く
             BackDisp_me=BackDisp_me+BlockLoca_me   
             #初期化
             i_me,j_me,i_me_new,j_me_new=int(n_w/2),1,int(n_w/2),1   
    #         BackDisp_me[:,:]=BackDisp[:,:]
             BlockLoca_me=np.zeros([n_h+2,n_w+2])
             
             block_choice_now_me=block_choice_next_me
             block_choice_next_me=random.randint(1,block_N)             
             ini_block_me(block_choice_now_me)
             hold_times_me=0
             BlockLoca_drop_laca_me=np.zeros([n_h+2,n_w+2]) 

             block_put_me=True
             if delete_pc==True:counter_me=True
             break
          if  block_put_me==True:break
     
         #ブロック消し---------------
         delete_lines_me=0    
         for k in range (1,n_h+1,1):        
          if np.all(BackDisp_me[k,1:n_w+1]>=1):
            BackDisp_me[1:k+1,1:n_w+1]=BackDisp_me[0:k,1:n_w+1]
            delete_lines_me=delete_lines_me+1
            delete_me=True
         line_me=line_me+delete_lines_me
         point_me=point_me+(delete_lines_me**2)*10
         DL_me=DL_me+delete_lines_me##
         #-----------------------------

         #ダメージ-----------------
         if counter_pc==True and delete_me==True or \
            counter_me==True and delete_pc==True:
          DL_me,DL_pc,counter_me,counter_pc,delete_me,delete_pc=damage(DL_me,DL_pc)
         
         #画面写し--------------------
         show_display_me(line_me,point_me,block_choice_next_me,block_choice_hold_me)
         me=False
         #ゲームオーバー---------------
         if np.any((BackDisp_me[1,1:n_w+1])>0): 
          me_GameOver=True
          stage=0
          DL_me,DL_pc=0,0
          GameLoop=False
                              
         #画面クローズ-----------------
         if event.type == QUIT or event.key == K_ESCAPE: escape()
