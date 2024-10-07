# -*- coding: cp1251 -*-
import random

n = 15
k = 15
c = [24, 29, 6, 11, 20, 3, 15, 3, 15, 21, 4, 16, 24, 29, 24]
w = [29, 30, 12, 10, 22, 4, 16, 22, 8, 16, 6, 16, 20, 16, 10]
s = [0 for i in range(n)]
r = []
Q = []
count = 1
max_count = int(input('Введите желаемое количество шагов '))

Wmax = 94
summa = 0
q = 0
m_best = 0
m_weight = 0

ans_1 = input(
    'Выберите способ формирования начальной популяции \n1 - Случайно с контролем ограничений  \n2 - Эвристика \n3 - Полный перебор от максимального к минимальному\n')

if ans_1 == '1':
    for j in range(k):
        for i in range(n):
            x = random.randint(0, 1)
            if x == 1:
                if summa + x * w[i] < Wmax:
                    summa += x * w[i]
                    q += c[i]
                    s[i] = 1
        r.append(s)
        Q.append(q)
        s = [0 for i in range(n)]
        summa = 0
        q = 0


elif ans_1 == '2':
    p1 = []
    p1.append((0, c[0]))
    o1 = 0
    o2 = c[0]
    p_full = c[0]

    for i in range(1, n):
        p_full += c[i]
        o1 += c[i - 1]
        o2 += c[i]
        p1.append((o1, o2))

    for i in range(k):
        p = p1.copy()
        C = random.randint(0, p_full)
        j = -1
        while j == -1:
            for l in range(len(p)):
                if C >= p[l][0] and C <= p[l][1]:
                    j = l
                    break

        p[j] = (0, 0)
        while summa + w[j] <= Wmax:
            summa += w[j]
            q += c[j]
            s[j] = 1
            j = -1
            while j == -1:
                C = random.randint(0, p_full)
                for l in range(len(p)):
                    if C >= p[l][0] and C <= p[l][1]:
                        j = l
                        break
            p[j] = (0, 0)
        summa = 0
        r.append(s)
        Q.append(q)
        s = [0 for i in range(n)]
        q = 0

print('Начальная популяция:')
for i in range(k):
    print(*r[i], " - ", Q[i], ", ", w[i])

ans_2 = input('\nВыберите кроссовер \n1 - Двухточечный \n2 - Однородный\n3 - Одноточечный')
ans_3 = input('Выберите мутацию \n1 - Сальтация \n2 - Генная\n3 - Хромосомная')
ans_4 = input('Выберите стратегию формирования \n1 - Поколенческая \n2 - Устойчивое состояние\n')

while len(r) != 0:

    generation = []
    mutation = []
    sum_Q = 0
    parents = []
    for i in range(k):
        sum_Q += Q[i]

    m_1 = 0
    i_1 = 0
    for i in range(k // 2 + 1):
        for m in range(len(Q)):
            p1 = Q[m] / sum_Q
            if p1 > m_1:
                m_1 = p1
                i_1 = i
        parents.append(r[i_1])
        Q[i_1] = 0
        m_1 = 0

    # КРОССОВЕР #
    child = [0 for i in range(n)]
    children = []
    if ans_2 == '1':
        break1 = random.randint(0, n // 2)
        break2 = random.randint(n // 2 + 1, n - 1)
        for j in range(k):
            parent_1 = random.choice(parents)
            for i in range(break1):
                child[i] = parent_1[i]
            parent2 = random.choice(parents)
            while parent2 == parent_1:
                parent2 = random.choice(parents)
            for i in range(break1, break2):
                child[i] = parent2[i]

            e = random.randint(0, 1)
            if e == 1:
                parent3 = parent_1
            else:
                parent3 = parent2
            for i in range(break2, n):
                child[i] = parent3[i]

            children.append(child)
            mutation.append(child)
            child = [0 for i in range(n)]

    elif ans_2 == '2':
        for j in range(k):
            parent_1 = random.choice(parents)
            parent2 = random.choice(parents)
            while parent2 == parent_1:
                parent2 = random.choice(parents)
            for i in range(n):
                y = random.randint(0, 1)
                if y == 1:
                    child[i] = parent_1[i]
                else:
                    child[i] = parent2[i]

            children.append(child)
            mutation.append(child)
            child = [0 for i in range(n)]

    elif ans_2 == '3':
        for j in range(k):
            parent1 = random.choice(parents)
            for i in range(n // 2):
                child[i] = parent1[i]
            parent2 = random.choice(parents)
            while parent2 == parent1:
                parent2 = random.choice(parents)
            for i in range(n // 2, n):
                child[i] = parent2[i]
            children.append(child)
            mutation.append(child)
            child = [0 for i in range(n)]

    # МУТАЦИЯ #
    if ans_3 == '1':
        for i in range(k):
            for j in range(3):
                y = random.randint(0, n - 1)
                if mutation[i][y] == 0:
                    mutation[i][y] = 1
                else:
                    mutation[i][y] = 0
    elif ans_3 == '2':
        for i in range(k):
            y = random.randint(0, n - 1)
            if mutation[i][y] == 0:
                mutation[i][y] = 1
            else:
                mutation[i][y] = 0

    elif ans_3 == '3':
        for i in range(k):
            for j in range(n):
                if mutation[i][j] == 0:
                    mutation[i][j] = 1
                else:
                    mutation[i][j] = 0

    # ФОРМИРОВАНИЕ #
    generation1 = []
    for i in range(len(mutation)):
        generation1.append(mutation[i])
        generation1.append(children[i])

    if ans_4 == '1':
        generation = generation1.copy()
    elif ans_4 == '2':
        G = round(random.random() * 2 * k)
        for i in range(G):
            j = random.randint(0, 2 * k - 1)
            generation.append(generation1[j])
        for i in range(k - G):
            j = random.randint(0, k // 2)
            generation.append(parents[j])

    # CЕЛЕКЦИЯ #
    fitness = []
    w1 = []
    weight = []
    price = []
    selection = []
    for l in range(len(generation)):
        one = generation[l]
        f = 0
        d = 0
        for v in range(len(one)):
            f += one[v] * c[v]
            d += one[v] * w[v]
        fitness.append(f)
        w1.append(d)

    roulette = []
    roulette.append((0, fitness[0]))
    o1 = 0
    o2 = fitness[0]
    full = fitness[0]

    for i in range(1, len(fitness)):
        full += fitness[i]
        o1 += fitness[i - 1]
        o2 += fitness[i]
        roulette.append((o1, o2))

    for l in range(k + 2):
        C = random.randint(0, full)
        j = -1
        while j == -1:
            C = random.randint(0, full)
            for i in range(len(roulette)):
                if C >= roulette[i][0] and C <= roulette[i][1]:
                    j = i
                    break
        roulette[j] = (0, 0)
        selection.append(generation[j])
        price.append(fitness[j])
        weight.append(w1[j])

    modification = []
    for i in range(len(selection)):
        one = selection[i]
        if weight[i] > Wmax:
            for j in range(len(one)):
                while weight[i] > Wmax:
                    l = random.randint(0, n - 1)
                    if one[l] == 1:
                        selection[i][l] = 0
                        weight[i] -= w[l]
                break
        modification.append(selection[i])

    k1 = 0
    r = modification
    k = len(modification)
    Q.clear()
    for i in range(len(modification)):
        q1 = 0
        one = modification[i]
        for j in range(len(one)):
            q1 += one[j] * c[j]
        Q.append(q1)
    if len(Q) != 0:
        print('\n\n Номер ', count)
        count += 1
        print('\nПопуляция')
        for i in range(len(modification)):
            print(modification[i], " - ", Q[i], ", ", weight[i])

        q_max = max(Q)
        b = Q.index(q_max)
        if Q[b] > m_best:
            best = modification[b]
            m_best = Q[b]
            m_weigth = weight[b]

        print('\nНаилучшая особь', modification[b], " - ", Q[b], ", ", weight[b])

    for i in range(k):
        for j in range(i, k):
            if price[i] == price[j] and i != j:
                k1 += 1

    if count > max_count:
        break

print('\n\nНаилучшая особь:', best, ' - ', m_best, ', ', m_weight)


