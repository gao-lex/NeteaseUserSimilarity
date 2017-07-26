import json
import random
from math import sqrt
from PIL import Image,ImageDraw

def tanimoto(d1,d2):
    # 返回值交集与并集的比率
    # 1.0表示不存在交集，0.0代表两人完全一样
    shr = 0
    songsList1 = d1['songsAllRank'].keys()
    songsList2 = d2['songsAllRank'].keys()
    if(len(songsList1)>=len(songsList2)):
        for i in songsList2:
            if i in songsList1:
                shr+=1
    else:
        for i in songsList1:
            if i in songsList2:
                shr+=1
    return 1.0 - shr/(len(songsList1)+len(songsList2)-shr)

def dataCleaning(data):
    # for i in data.keys():
    #     if len(data[i]['songsAllRank'])==0:
    #         del data[i]
    # return data
    # 字典过滤,将采集数据中搜有时间听歌100首以上的前100首过滤出来
    return {k:v for(k,v) in data.items() if len(v['songsAllRank']) !=0}

def clusterScaleDown(data,distance = tanimoto,rate=0.01):
    n = len(data)

    loopList = data.keys()
    # 每一对数据间的真实(计算出来的应该有的)距离
    realDist = [  [distance(data[j],data[i]) for j in loopList]  for i in loopList ]

    # 随机初始化节点在二维空间中的起始位置(0-1之间)
    loc = [[random.random(),random.random()] for i in range(n)]
    # 每一对数据间目前的距离
    fakeDist = [[0.0 for j in range(n)] for i in range(n)]
    # [
    #   [n个0]
    #   n行
    # ]

    lastError = None
    # 在最多1000次循环里面找最优解
    for m in range(0,1000):
        # 寻找投影后的距离
        for i in range(n):
            for j in range(n):
                fakeDist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2) for x in range(len(loc[i]))]))
        # 移动节点
        grad = [[0.0,0.0] for i in range(n)]# n行的[0,0]

        totalError = 0

        for k in range(n):
            for j in range(n):
                if j==k :continue
                # 误差值等与目标距离与当前距离之间差值的百分比
                errorTerm = (fakeDist[j][k] - realDist[j][k])/realDist[j][k]
                # 每一个节点都须要根据误差的多少，按比例移离或移向其他节点
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakeDist[j][k]) * errorTerm
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakeDist[j][k]) * errorTerm
                # 记录总的误差值
                totalError +=abs(errorTerm)
        print(totalError)

        # 如果节点移动之后的情况变得更糟，则程序结束
        if lastError and lastError<totalError:break
        lastError = totalError

        # 根据rate参数与grad值相乘的结果，移动每一个节点
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]

    return loc

def draw2d(data):
    img = Image.new('RGB', (2000,2000), 255, 255, 255)
    draw = ImageDraw.Draw(img)
    loopList = data.keys()
    print(loopList)

f = open('./info.json','r')
data = dataCleaning(json.load(f))
keys1 = data.keys()
keys2 = data.keys()
print(keys1==keys2)
clusterScaleDown(data)
draw2d(data)
f.close()