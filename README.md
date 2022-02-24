# 3D Rotation
Matrix EulerAngle Quaternion 

紙飛行機のモデルを空間で回転します


## PaperAirplaneEuler.py
オイラー角を使って紙飛行機を回転してみます  
[F1]キーで回転が始まります

### EulerAngles(p, th, order)
点(p)の位置をオイラー角(th)で指定回転順(order)で回転します

### PaperAirplaneEuler(angle, order)
紙飛行機のモデルを7点で作ってオイラー角で回転する様子をmatplotlibで表示します


## PaperAirplaneQuaternion.py
クオータニオン（四元数）を使って紙飛行機を回転してみます  
[F1]キーで回転が始まります

### Euler2Quaternion(th, order)
オイラー角(th)をクオータニオンに変換します

### PaperAirplaneQuaternion(angle, order)
紙飛行機のモデルを7点で作ってクオータニオンで任意の姿勢に回転する様子をmatplotlibで表示します

#Qiita記事  
https://qiita.com/OkitaSystemDesign/items/23e94d4e0db22cc6ebd4  
https://qiita.com/OkitaSystemDesign/items/fb5d5e4918d31ccd5e34
