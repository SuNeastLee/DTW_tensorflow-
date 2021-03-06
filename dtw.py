import tensorflow as tf
import fastdtw as dw
import numpy as np
import sys

content_music = tf.placeholder(tf.float32, [1, 2, 10, 1])
style = tf.placeholder(tf.float32, [1, 2, 10, 1])


def DTW(style_m, content, window=None, d=lambda x, y: tf.abs(tf.subtract(x, y))):
    style = tf.reshape(style_m, [10, 2])
    content = tf.reshape(content, [10, 2])

    style_input = tf.Variable(tf.zeros([10, 2],tf.float32))
    content_input = tf.Variable(tf.zeros([10, 2], tf.float32))



    print(style_input[0])



    style_input = tf.assign_add(style_input,style)
    print(style_input[0])
    content_input = tf.assign_add(content_input,content)
    # style_input = tf.TensorArray(dtype=tf.float32, handle=style_input,tensor_array_name=None,flow=1)

    style = tf.reduce_mean(style_input,1)
    content = tf.reduce_mean(content_input,1)

    content_array = tf.TensorArray(dtype=tf.float32,size=10,flow=1)

    style_array = tf.TensorArray(dtype=tf.float32,size=10,flow=1)


    con = tf.unstack(content)
    sty = tf.unstack(style)

    M, N = len(con), len(sty)
    # M, N = len(content), len(style)
    cost = tf.Variable(tf.ones([M,N], tf.float32))
    cost = tf.reshape(cost,[M,N])
    tem = 10*10
    cost = tf.TensorArray(dtype=tf.float32, size=tem)

    # cost = tf.make_ndarray(cost)

    content_array = content_array.scatter([0,10],content)
    style_array = style_array.scatter([0,10],style)

    # temp1 = content_array.unstack(content).read(0)
    # temp1 = content_array.read(0)
    # temp2 = style_array.read(0)
    # temp3 = d(temp1,temp2)

    # temp4 = cost[0,0]


    # cost.write(0,12)
    tem0 = cost.read(0)
    # temp6 = cost[0][0]

    # cost = cost[0,0].assign(d(con[0], sty[0]))

    # cost = tf.scatter_add(cost,[0], [d(content[0], style[0])])
    temcon = content_array.read(0)
    temsty = style_array.read(0)
    dis = d(temcon,temsty)
    cost.write(0,dis).mark_used()

    for i in range(1, M):
        # cost = tf.scatter_update(cost, [i][0], cost[i - 1, 0] + d(con[i], sty[0]))
        cost.write(i, cost.read(i-1)+d(content_array.read(0), style_array.read(i))).mark_used()
        # tem=cost.read(i)
        # print(i)

    for j in range(1, tem, M):
        # cost = tf.scatter_update(cost, [0][j], cost[0, j-1] + d(con[0], sty[j]))
        cost.write(j, cost.read(j-M)+d(content_array.read(0), style_array.read(j))).mark_used()
        print(j)



    for i in range(0, tem-M):
        b = i
        if i%M!=9 :
            a = i%M
            temp1 = cost.read(i)
            temp2 = cost.read(i + 1)
            temp3 = cost.read(i + M)
            temp_mid = tf.minimum(temp1, temp2)
            min_value = tf.minimum(temp_mid, temp3)
            new_value = min_value + d(content_array.read(i), style_array.read(i % M))
            index = i+M+1
            cost.write(index,new_value).mark_used()

    minimum_cost =cost.read(tem-1)


    return minimum_cost


a = DTW(style, content_music)
