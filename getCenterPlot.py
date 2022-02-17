# -*- coding: utf-8 -*-

# 3点を通る球と平面を表示する
# 連立方程式はnumpyを使わず自力でガウスの消去法

#from typing import no_type_check_decorator
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from module import qtrotate as rotate

# 3元連立方程式を解く
# ガウスの消去法
def gauss(a):
    for i in range(3):
        m = 0
        pivot = i
        for j in range(i, 3, 1):
            if abs(a[j][i]) > m:
                m = abs(a[j][i])
                pivot = j
        
        if pivot != i:
            for j in range(4):
                a[pivot][j], a[i][j] = a[i][j], a[pivot][j]

    for k in range(3):
        p = a[k][k]
        a[k][k] = 1
        for j in range(k+1, 4, 1):
            a[k][j] /= p
        for i in range(k+1, 3, 1):
            q = a[i][k]
            for j in range(k+1, 4, 1):
                a[i][j] -= q * a[k][j]
            a[i][k] = 0

    for i in range(2, -1, -1):
        for j in range(2, i, -1):
            a[i][3] -= a[i][j] * a[j][3]

    return a[0][3],a[1][3],a[2][3]



def getCenter(A, B, C):
    M = [[0 for i in range(4)] for j in range(3)]

    # p(x, y, z)は中心座標
    # |AP| = |BP|
    # (x - A.x)^2 + (y - A.y)^2 + (z - A.z)^2
    #   = (x - B.x)^2 + (y - B.y)^2 + (z - B.z)^2
    M[0][0] = 2*(B[0] - A[0])
    M[0][1] = 2*(B[1] - A[1])
    M[0][2] = 2*(B[2] - A[2])
    M[0][3] = B[0]*B[0] + B[1]*B[1] + B[2]*B[2] - A[0]*A[0] - A[1]*A[1] - A[2]*A[2]
    
    #|AP| = |CP|
    # (x - A.x)^2 + (y - A.y)^2 + (z - A.z)^2
    #   = (x - C.x)^2 + (y - C.y)^2 + (z - C.z)^2
    M[1][0] = 2*(C[0] - A[0])
    M[1][1] = 2*(C[1] - A[1])
    M[1][2] = 2*(C[2] - A[2])
    M[1][3] = C[0]**2 + C[1]**2 + C[2]**2 - A[0]**2 - A[1]**2 - A[2]**2

    AB = [B[0] - A[0], B[1] - A[1], B[2] - A[2]] 
    AC = [C[0] - A[0], C[1] - A[1], C[2] - A[2]] 
    ABxAC = [AB[1] * AC[2] - AB[2] * AC[1], \
             AB[2] * AC[0] - AB[0] * AC[2], \
             AB[0] * AC[1] - AB[1] * AC[0]]

    # P は 平面ABC上、法線ベクトルABｘAC とベクトルAP は直行、内積が0
    # ABxAC[0](x - A.x) + ABxAC[1](y - A.y) + ABxAC[2](z - A.z) = 0
    M[2][0] = ABxAC[0]
    M[2][1] = ABxAC[1]
    M[2][2] = ABxAC[2]
    M[2][3] = ABxAC[0] * A[0] + ABxAC[1] * A[1] + ABxAC[2] * A[2]

    P = gauss(M)

    return P


# 法線ベクトルを指定して平面をプロットする関数
# vector：法線ベクトル
# point：平面上の点
# size: 平面の大きさ
# 戻り値: x,y,z
def plane(vector, point, offset, size):

    # 格子点の作成
    x = np.arange(offset[0]-size, offset[0]+size, 1)
    y = np.arange(offset[1]-size, offset[1]+size, 1)
    xx, yy = np.meshgrid(x, y)

    # 平面の方程式
    # ベクトル(p,q,r)
    # z = (p*x + q*y + s) / r 
    zz = point[2] - (vector[0]*(xx-point[0]) + vector[1]*(yy-point[1])) / vector[2]

    return xx, yy, zz

# 3点を通る平面をプロットする関数
# p0,p1,p2: 3点
# size平面の大きさ
def point_plane(p0, p1, p2, offset, size):

    u = p1 - p0
    v = p2 - p0
    w = np.cross(u, v)
    vector = 0.5 * np.abs(size) * w / np.sqrt(np.sum(w**2))
    
    x, y, z = plane(vector, p0, offset, size)

    return x, y, z, vector


def getCenterPlot(A, B, C):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    # 中心の座標を求める
    P = getCenter(A, B, C)

    ax.scatter(A[0], A[1], A[2], color='blue')
    ax.scatter(B[0], B[1], B[2], color='blue')
    ax.scatter(C[0], C[1], C[2], color='blue')
    ax.scatter(P[0], P[1], P[2], color='red')
    ax.text(A[0], A[1], A[2], 'A', fontsize=9)
    ax.text(B[0], B[1], B[2], 'B', fontsize=9)
    ax.text(C[0], C[1], C[2], 'C', fontsize=9)
    ax.text(P[0], P[1], P[2], 'P0='+format(P[0],'.1f')+', '+format(P[1],'.1f')+', '+format(P[2],'.1f'), fontsize=9)

    # 2点間の距離
    r = np.sqrt((P[0]-A[0])**2 + (P[1]-A[1])**2 + (P[2]-A[2])**2)
    print(r)

    # 球を描く
    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = r * np.outer(np.cos(u), np.sin(v)) + P[0]
    y = r * np.outer(np.sin(u), np.sin(v)) + P[1]
    z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + P[2]
    ax.plot_surface(x, y, z, color="lightgreen",rcount=100, ccount=100, antialiased=False, alpha=0.3)
    

    # 3点を通る平面をプロット
    x,y,z,vector = point_plane(np.array(A), np.array(B), np.array(C), P, r+1)
    ax.plot_surface(x, y, z, color="blue", alpha=0.3)

    # 3点の重心
    cg = (np.array(A) + np.array(B) + np.array(C)) / 3
    ax.scatter(cg[0], cg[1], cg[2], color='orange')
    ax.text(cg[0], cg[1], cg[2], ' center of gravity=' + format(cg[0],'.1f')+', '+format(cg[1],'.1f')+', '+format(cg[2],'.1f'), fontsize=9, color="orange")

    # 法線ベクトルをプロット
    ax.quiver(P[0], P[1], P[2], vector[0], vector[1], vector[2], color = "red", length = 1, arrow_length_ratio = 0.2)
    ax.text(P[0]+vector[0], P[1]+vector[1], P[2]+vector[2], format(v[0],'.1f')+', '+format(v[1],'.1f')+', '+format(v[2],'.1f'), fontsize=9, color="red")

    # クオータニオン回転
    qtr = rotate.qtrotate()
    th = np.linspace(0, 2 * np.pi, 201) # 回転角
    x1,y1,z1 = [],[],[]
    v1 = vector / np.linalg.norm(vector)

    for i in range(len(th)):
        pos = qtr.rotate(v1, np.array(A) - np.array(P), th[i])
        x1.append(pos[0] + P[0])
        y1.append(pos[1] + P[1])
        z1.append(pos[2] + P[2])
        #print("(%10.3f,%10.3f,%10.3f)" % (pos[0], pos[1], pos[2]))
        
    ax.plot(x1, y1, z1, linestyle = 'solid', color='green')


    # グラフの設定
    gsize = r +1.0
    ax.set_xlabel("x");    ax.set_ylabel("y");    ax.set_zlabel("z")
    absview = max(np.abs(P)) + r + 1.0
    ax.set_xlim(-absview, absview);    ax.set_ylim(-absview,absview);     ax.set_zlim(-absview,absview)
    
    ax.set_box_aspect((1,1,1))
    plt.show()


# 3点の座標
A = list((-2.0, 1.0, 0.0)) 
B = list((0.0, 1.0, 0.7)) 
C = list((1.0, 0.0, 0.0))
#A = list((1.0, 1.0, 1.0))
#B = list((2.0, 2.0, 2.0))
#C = list((2.0, 1.0, 1.0))
#A = list((3.0, 6.0, 2.0)) 
#B = list((1.0, 2.0, 8.0)) 
#C = list((7.0, 3.0, 3.0)) 
#A = list((0.0, 5.0, 0.0))
#B = list((0.0, 0.7, 0.7))
#C = list((1.0, -10.0, 0.0))
#A = list((-0.0, 6.0, 2.0))
#B = list((-10.0, 2.0, 24.0))
#C = list((-26.0, 1.0, 32.0))
#A = list((-10.0, 6.0, 0.0))
#B = list((-20.0, 2.0, 0.0))
#C = list((-36.0, 1.0, 0.0))
#A = list((5.0, 1.0, 1.0))
#B = list((5.0, 2.0, 5.0))
#C = list((7.0, 3.0, 1.0))

getCenterPlot(A, B, C)

