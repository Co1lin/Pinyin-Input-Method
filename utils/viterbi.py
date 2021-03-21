import math

def dist2(x, y, model: dict, alpha=0.8):
    '''
    probability that y follows x
    :return: P(y|x) = alpha * count(xy) / count(x) + (1 - alpha) * P(x)
    '''
    # use
    count_x = model['1'].get(x, 0)
    if count_x == 0:
        return math.inf
    else:
        res = -math.log(alpha * model['2'].get(x + y, 0) / count_x + \
                (1 - alpha) * count_x / model['1_total'])
        print(x, y, res)
        return res

def transfer_cost(pre, char, model: dict, alpha=0.8, beta=0.8):

    res = 0
    # yx a
    # Cost(a|x) = alpha * count(xa) / count(x) + (1 - alpha) * P(a)
    count_a = model['1'].get(char, 0)
    p_a = count_a / model['1_total']
    count_x = model['1'].get(pre[-1], 0.1)
    count_xa = model['2'].get(pre[-1] + char, 0)
    try:
        res = -math.log(alpha * count_xa / count_x + (1 - alpha) * p_a)
    except ValueError:
        return math.inf

    if len(pre) >= 2:
        # Cost(a|yx) = beta * count(yxa) / count(yx) + (1 - beta) * P(a)
        count_yx = model['2'].get(pre[-2:], 0.1)
        count_yxa = model['3'].get(pre[-2:] + char, 0)
        try:
            res += -math.log(beta * count_yxa / count_yx + (1 - beta) * p_a)
        except ValueError:
            pass

    return res

def viterbi(line, pinyin_dict: dict, model: dict, alpha=0.8):
    '''
    viterbi algorithm
    :return: a Chinese string
    '''
    line = ('start ' + line + ' end').split()

    # build a graph for viterbi algorithm
    graph = []
    for spelling in line:
        graph.append(pinyin_dict[spelling])

    #
    cost = [ [0] ]
    trace = [ ['>'] ]
    for i in range(1, len(graph)):
        # layer i
        layer_trace = []
        layer_cost = []
        for j in range( len(graph[i]) ):
            # j_th character in current layer i
            # compute cost for j_th character
            best_k, best_cost = -1, math.inf
            for k in range( len(cost[-1]) ):
                # transfer from k_th character in last layer
                k_cost = cost[-1][k] + transfer_cost(trace[-1][k], graph[i][j], model, alpha)
                if k_cost < best_cost:
                    # update best value
                    best_k, best_cost = k, k_cost
            # record the best value
            layer_cost.append(best_cost)
            layer_trace.append(trace[-1][best_k] + graph[i][j])
        trace.append(layer_trace)
        cost.append(layer_cost)

    return trace[-1][0][1:][:-1]

