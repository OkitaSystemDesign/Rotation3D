"""
紙飛行機の姿勢制御

初期位置からオイラー角で指定した角度へ回転

参考URL
回転行列、クォータニオン(四元数)、オイラー角の相互変換
 https://qiita.com/aa_debdeb/items/3d02e28fb9ebfa357eaf

"""

import ctypes
from enum import Enum
from typing import TYPE_CHECKING

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d


class EulerOrder(Enum):
    XYZ=0
    XZY=1
    YXZ=2
    YZX=3
    ZXY=4
    ZYX=5


# 紙飛行機モデルの作成
def plane(offset):
    # model成分のデータの作成
    x = [1,-1,-1, 1,  -1,-1, 1]
    y = [0, 1,-1, 0,   0, 0, 0]
    z = [0, 0, 0, 0,-0.5, 0, 0]

    mx = list(map(lambda a: a + offset[0], x))
    my = list(map(lambda b: b + offset[1], y))
    mz = list(map(lambda c: c + offset[2], z))

    return mx, my, mz

# 回転軸の作成（表示用）
def axis(offset):
    # 軸成分のデータの作成
    x = [1, 0, 0]
    y = [0, 1, 0]
    z = [0, 0, 1]

    mx = list(map(lambda a: a + offset[0], x))
    my = list(map(lambda b: b + offset[1], y))
    mz = list(map(lambda c: c + offset[2], z))

    return mx, my, mz

# 点(p)の位置をオイラー角(th)で回転
def EulerAngles(p, th, order):
    if order == EulerOrder.XYZ:
        #XYZ
        x = ((np.cos(th[1])*np.cos(th[2]))*p[0]) + ((-np.cos(th[1])*np.sin(th[2]))*p[1]) + (np.sin(th[1])*p[2])
        y = ((np.sin(th[0])*np.sin(th[1])*np.cos(th[2])+np.cos(th[0])*np.sin(th[2]))*p[0]) + ((-np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[0])*np.cos(th[2]))*p[1]) + ((-np.sin(th[0])*np.cos(th[1]))*p[2])
        z = ((-np.cos(th[0])*np.sin(th[1])*np.cos(th[2])+np.sin(th[0])*np.sin(th[2]))*p[0]) + ((np.cos(th[0])*np.sin(th[1])*np.sin(th[2])+np.sin(th[0])*np.cos(th[2]))*p[1]) + ((np.cos(th[0])*np.cos(th[1]))*p[2])
    elif order == EulerOrder.XZY:
        #XZY
        x = ((np.cos(th[1])*np.cos(th[2]))*p[0]) + (-np.sin(th[2])*p[1]) + ((np.sin(th[1])*np.cos(th[2]))*p[2])
        y = ((np.cos(th[0])*np.cos(th[1])*np.sin(th[2])+np.sin(th[0])*np.sin(th[1]))*p[0]) + ((np.cos(th[0])*np.cos(th[2]))*p[1]) + ((np.cos(th[0])*np.sin(th[1])*np.sin(th[2])-np.sin(th[0])*np.cos(th[1]))*p[2])
        z = ((np.sin(th[0])*np.cos(th[1])*np.sin(th[2])-np.cos(th[0])*np.sin(th[1]))*p[0]) + ((np.sin(th[0])*np.cos(th[2]))*p[1]) + ((np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[0])*np.cos(th[1]))*p[2])
    elif order == EulerOrder.YXZ:
        #YXZ
        x = ((np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[1])*np.cos(th[2]))*p[0]) + ((np.sin(th[0])*np.sin(th[1])*np.cos(th[2])-np.cos(th[1])*np.sin(th[2]))*p[1]) + ((np.cos(th[0])*np.sin(th[1]))*p[2])
        y = ((np.cos(th[0])*np.sin(th[2]))*p[0]) + ((np.cos(th[0])*np.cos(th[2]))*p[1]) + ((-np.sin(th[0]))*p[2])
        z = ((np.sin(th[0])*np.cos(th[1])*np.sin(th[2])-np.sin(th[1])*np.cos(th[2]))*p[0]) + ((np.sin(th[0])*np.cos(th[1])*np.cos(th[2])+np.sin(th[1])*np.sin(th[2]))*p[1]) + ((np.cos(th[0])*np.cos(th[1]))*p[2])
    elif order == EulerOrder.YZX:
        #YZX
        x = ((np.cos(th[1])*np.cos(th[2]))*p[0]) + ((-np.cos(th[0])*np.cos(th[1])*np.sin(th[2])+np.sin(th[0])*np.sin(th[1]))*p[1]) + ((np.sin(th[0])*np.cos(th[1])*np.sin(th[2])+np.cos(th[0])*np.sin(th[1]))*p[2])
        y = ((np.sin(th[2]))*p[0]) + ((np.cos(th[0])*np.cos(th[2]))*p[1]) + ((-np.sin(th[0])*np.cos(th[2]))*p[2])
        z = ((-np.sin(th[1])*np.cos(th[2]))*p[0]) + ((np.cos(th[0])*np.sin(th[1])*np.sin(th[2])+np.sin(th[0])*np.cos(th[1]))*p[1]) + ((-np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[0])*np.cos(th[1]))*p[2])
    elif order == EulerOrder.XYZ.ZXY:
        #ZXY
        x = ((-np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[1])*np.cos(th[2]))*p[0]) + ((-np.cos(th[0])*np.sin(th[2]))*p[1]) + ((np.sin(th[0])*np.cos(th[1])*np.sin(th[2])+np.sin(th[1])*np.cos(th[2]))*p[2])
        y = ((np.sin(th[0])*np.sin(th[1])*np.cos(th[2])+np.cos(th[1])*np.sin(th[2]))*p[0]) + ((np.cos(th[0])*np.cos(th[2]))*p[1]) + ((-np.sin(th[0])*np.cos(th[1])*np.cos(th[2])+np.sin(th[1])*np.sin(th[2]))*p[2])
        z = ((-np.cos(th[0])*np.sin(th[1]))*p[0]) + ((np.sin(th[0]))*p[1]) + ((np.cos(th[0])*np.cos(th[1]))*p[2])
    elif order == EulerOrder.ZYX:
        #ZYX
        x = ((np.cos(th[1])*np.cos(th[2]))*p[0]) + ((np.sin(th[0])*np.sin(th[1])*np.cos(th[2])-np.cos(th[0])*np.sin(th[2]))*p[1]) + ((np.cos(th[0])*np.sin(th[1])*np.cos(th[2])+np.sin(th[0])*np.sin(th[2]))*p[2])
        y = ((np.cos(th[1])*np.sin(th[2]))*p[0]) + ((np.sin(th[0])*np.sin(th[1])*np.sin(th[2])+np.cos(th[0])*np.cos(th[2]))*p[1]) + ((np.cos(th[0])*np.sin(th[1])*np.sin(th[2])-np.sin(th[0])*np.cos(th[2]))*p[2])
        z = ((-np.sin(th[1]))*p[0]) + ((np.sin(th[0])*np.cos(th[1]))*p[1]) + ((np.cos(th[0])*np.cos(th[1]))*p[2])

    return x,y,z


# オイラー角で回転
def PaperAirplaneEuler(angle, order):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    plt.cla()

    th9 = [0.0]*3

    offset = [0,0,0]

    # ベース姿勢のモデル    青色の飛行機
    x,y,z = plane(offset)  #ベース3D表示用
    axx,axy,axz = axis(offset)

    # 最終姿勢              赤色の飛行機の位置を設定する
    th9[0] = angle[0] * np.pi / 180.0
    th9[1] = angle[1] * np.pi / 180.0
    th9[2] = angle[2] * np.pi / 180.0
    
    x9,y9,z9 = [0]*7,[0]*7,[0]*7    #最終姿勢3D表示用
    for i in range(7):
        x9[i],y9[i],z9[i] = EulerAngles([x[i],y[i],z[i]], th9, order)
    
    x2,y2,z2 = [0.0]*7, [0.0]*7, [0.0]*7    #移動中3D表示用
    axx2,axy2,axz2 = [0.0]*3, [0.0]*3, [0.0]*3    #軸表示用
    speed = 0.0

    angle2 = [0.0, 0.0, 0.0]
    th2 = [0.0, 0.0, 0.0]

    # 回転順を配列順に並べる
    if order == EulerOrder.XYZ:   od = [0,1,2]
    elif order == EulerOrder.XZY: od = [0,2,1]
    elif order == EulerOrder.YXZ: od = [1,0,2]
    elif order == EulerOrder.YZX: od = [1,2,0]
    elif order == EulerOrder.ZXY: od = [2,0,1]
    elif order == EulerOrder.ZYX: od = [2,1,0]
    OrderNo = 0
    ra = od[OrderNo]

    while True:
        plt.cla()
        
        # 軸で回転
        if angle[ra] >= angle2[ra]:
            angle2[ra] += speed
            if angle2[ra] >= angle[ra]:
                angle2[ra] = angle[ra]

        th2[0] = angle2[0] * np.pi / 180.0
        th2[1] = angle2[1] * np.pi / 180.0
        th2[2] = angle2[2] * np.pi / 180.0

        for i in range(7):
            x2[i],y2[i],z2[i] = EulerAngles([x[i],y[i],z[i]], th2, order)   #青い紙飛行機

        for i in range(3):
            axx2[i],axy2[i],axz2[i] = EulerAngles([axx[i],axy[i],axz[i]], th2, order)   # 回転軸のベクトル用


        # ----- 以下 グラフ表示用 -----
        # 設定した目標位置 赤い紙飛行機
        poly1 = list(zip(x9[:4],y9[:4],z9[:4]))
        ax.add_collection3d(art3d.Poly3DCollection([poly1], color='red', linewidths=0.3, alpha=0.02))
        poly2 = list(zip(x9[3:7],y9[3:7],z9[3:7]))
        ax.add_collection3d(art3d.Poly3DCollection([poly2], color='brown', linewidths=0.3, alpha=0.02))

        # 回転中のモデル
        poly3 = list(zip(x2[:4],y2[:4],z2[:4]))
        ax.add_collection3d(art3d.Poly3DCollection([poly3], color='blue', alpha=0.5))
        poly4 = list(zip(x2[3:7],y2[3:7],z2[3:7]))
        ax.add_collection3d(art3d.Poly3DCollection([poly4], color='midnightblue', alpha=0.5))
        #ax.scatter(x2[:7], y2[:7], z2[:7], color='blue')       #点を表示

        
        # 回転軸のベクトルをプロット
        ax.quiver(offset[0], offset[1], offset[2], axx2[ra], axy2[ra], axz2[ra], color = "orange", length = 2, arrow_length_ratio = 0.2)
        if ra == 0:   vectorText = 'X'
        elif ra == 1: vectorText = 'Y'
        elif ra == 2: vectorText = 'Z'
        ax.text(axx2[ra]*2, axy2[ra]*2, axz2[ra]*2, vectorText, fontsize=9, color='orange')

        # グラフのエリア設定
        ax.set_xlabel("x");     ax.set_ylabel("y");     ax.set_zlabel("z")
        ax.set_xlim(-2,2);      ax.set_ylim(-2,2);      ax.set_zlim(-2,2)
        ax.set_box_aspect((1,1,1))
        #ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        ax.text(-1,-1,-2,'[F1]:Start/Pause, [ESC]:Stop', fontsize=9)
        ax.text(-1,-1,-2.3, 'Target Euler Angle: '+format(angle[0],'.1f')+', '+format(angle[1],'.1f')+', '+format(angle[2],'.1f'), fontsize=9)


        if angle2[ra] == angle[ra]:
            if OrderNo < 2:
                OrderNo = OrderNo + 1
                ra = od[OrderNo]
                plt.pause(1)
            else:
                break
        else:
            plt.pause(0.1)

        if getkey(F1):
            if speed == 0.0:
                speed = 2.0
            else:
                speed = 0.0
        
        if getkey(ESC):
            break
    
    plt.show()


# キー操作用
ESC = 0x1b  #ESCキー
F1 = 0x70   #F1キー
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))

angle = [20.0, 30.0, 40.0]
order = EulerOrder.XYZ
PaperAirplaneEuler(angle, order)
