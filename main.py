# Lambda NFA

def deltaT(stari, cuvant):
    # lista starilor in care putem ajunge la pasul curent
    returned = []

    # daca cuvantul a ajuns la ultima lui litera
    if len(cuvant) == 1:
        # iau toate starile listei cu care am ajuns aici
        for stare in stari:
            # si le trec prin checker-ul de tranzitie -- functia delta
            acc = delta(stare,cuvant[0])
            # daca exista o tranzitie, atunci o adauga la lista starilor in care ajunge cuvantul
            # la final, daca nu exista, primeste None si nu e adaugat
            if acc is not None:
                returned += acc
        return returned

    #daca cuvantul are mai mult de o litera
    for stare in stari:
        # facem ca mai devreme, dar nu returnam final lista
        acc = delta(stare,cuvant[0])
        if acc is not None:
            returned += acc

    # ci doar continuam in adancime cu restul cuvantului
    return deltaT(returned, cuvant[1:])

def delta(stare,cuvant):
    global muchii

    # daca cuvantul este in multimea de tranzitii (pe care am numit-o muchii
    # cand am facut codul acum 2 saptamani), este returnata multimea starilor in care
    # poate ajunge
    if (stare,cuvant) in muchii:
        return muchii[(stare,cuvant)]

    # daca nu e in muchii, atunci e returnat None si e ignorat in deltaT
    return None

def lamb():
    global lambdas
    b = 0

    # pentru fiecare lambda din lambda
    for element in lambdas:
        # daca avem inca o lambda in continuare, element[2] fiind starea in care ajungem
        # in urma unei tranzitii, atunci adaugam noile tranzitii, de la element[0] la
        # starile in care ajungem cu continuarea de lambda, in lambda tranzitii in lambdas
        if (element[2],'.') in muchii.keys():
            for value in muchii[(element[2],'.')]:
                if [element[0],'.',value] not in lambdas:
                    lambdas += [[element[0],'.',value]]
                    b = 1

    if b == 1:
        lamb()

# ===================================================

# ===================================================


f = open("LNFA.txt")
g = open("out.txt", "w")
nrAcceptate = 0

# citim nr de stari si starile
nrS = int(f.readline())
NotUsedStari = [int(x) for x in f.readline().split()]

# citim nr de litere in alfabet si alfabetul
nrA = int(f.readline())
alfabet = [x for x in f.readline().split()]

# cititm starea initiala
stareInitiala = int(f.readline())

# cititm nr de stari finale si starile finale
nrSF = int(f.readline())
stariFinale = [int(x) for x in f.readline().split()]

# citim nr de tranzitii si tranzitiile
nrM = int(f.readline())
muchii = {}
lambdas = []
for i in range(nrM):
    # procesam linia de de input cu muchia // tranzitiile
    inputs = f.readline().split()
    inputs = [int(inputs[0]), inputs[1], int(inputs[2])]

    # daca exista deja tranzitia din starea inputs[0] cu litera din alfabet inputs[1]
    # in dictionarul de tranzitii, atunci adaugam o stare noua in multimea apelata de
    # muchii[(inputs[0],inputs[1])]
    if (inputs[0],inputs[1]) in muchii:
        muchii[(inputs[0],inputs[1])].append(inputs[2])
    # daca nu exista aceasta tranzitie, creez legatura
    else:
        muchii[(inputs[0],inputs[1])] = [inputs[2]]

    # daca este o lambda tranzitie, atunci o adaug in lista auxiliara lambdas pentru
    # procesarea lambdaurilor ulterior
    if inputs[1] == ".":
        lambdas += [inputs]

# print(lambdas)

# apelez functia lamb, care adauga in lambda toate perechile de 2 sau mai multe
# lambda tranzitii care pot fi adaugate
lamb()

# adaug noile tranzitii cu conexiunile starii respective in dictionar
for lamb in lambdas:
    for a in muchii[(lamb[0],lamb[1])]:
        for letter in alfabet:
            if (a,letter) in muchii:
                if (lamb[0],letter) in muchii:
                    muchii[(lamb[0],letter)] += muchii[(a, letter)]
                else:
                    muchii[(lamb[0],letter)] = muchii[(a, letter)]

# sterg duplicatele
for x in muchii.keys():
    muchii[x] = list(set(muchii[x]))

# iau nr de cuvinte si apoi cuvintele din fisier la rand
nrC = int(f.readline())
for line in f:
    # scot \n de la sfarsitul randului
    line = line.rstrip()
    # apelez functia acceptat care imi da multimea starilor in care sfarseste cuvantul
    stari = deltaT([stareInitiala], line)
    # iau starile la rand si daca este o stare finala adaug "DA" in fisierul text pentru acceptat
    # altfel adaug "NU" in fisierul text
    for stare in stari:
        if stare in stariFinale:
            g.write("DA\n");
            line = -1
            nrAcceptate += 1
            break
    if line != -1:
        g.write("NU\n");



f.close()