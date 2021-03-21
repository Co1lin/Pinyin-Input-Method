import math

def transfer_cost(pre, char, model: dict, beta):
    res = 0
    # yx a
    # Cost(a|x) = alpha * count(xa) / count(x) + (1 - alpha) * P(a)
    count_a = model[1].get(char, 0.1)
    p_a = count_a / model['1_total']
    count_x = model[1].get(pre[-1], 1)
    count_xa = model[2].get(pre[-1] + char, 0)
    res = -math.log(beta[0] * count_xa / count_x + (1 - beta[0]) * p_a)
    if len(pre) >= 2:
        # Cost(a|yx) = beta * count(yxa) / count(yx) + (1 - beta) * P(a)
        count_yx = model[2].get(pre[-2:], 1)
        count_yxa = model[3].get(pre[-2:] + char, 0)
        res += -math.log(beta[1] * count_yxa / count_yx + (1 - beta[1]) * p_a)
    return res

def viterbi(line, pinyin_dict: dict, model: dict, beta=[0.8, 0.8]):
    '''
    viterbi algorithm
    :return: a Chinese string
    '''
    line = ('start ' + line + ' end').split()

    # build a graph for viterbi algorithm
    graph = []
    for spelling in line:
        graph.append(pinyin_dict[spelling])

    # viterbi
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
                k_cost = cost[-1][k] + transfer_cost(trace[-1][k], graph[i][j], model, beta)
                if k_cost < best_cost:
                    # update best value
                    best_k, best_cost = k, k_cost
            # record the best value
            layer_cost.append(best_cost)
            layer_trace.append(trace[-1][best_k] + graph[i][j])
        trace.append(layer_trace)
        cost.append(layer_cost)

    return trace[-1][0][1:][:-1]

