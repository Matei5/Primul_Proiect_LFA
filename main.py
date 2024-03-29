# Lambda NFA
def acceptat(cuvant):
    global stariFinale, stareInitiala

    returned = deltaT([stareInitiala], cuvant)
    return returned


def deltaT(stari, cuvant):
    returned = []

    if len(cuvant) == 1:
        for stare in stari:
            acc = delta(stare,cuvant[0])
            if acc is not None:
                returned += acc
        return returned

    for stare in stari:
        acc = delta(stare,cuvant[0])
        if acc is not None:
            returned += acc

    return deltaT(returned, cuvant[1:])

def delta(stare,cuvant):
    global muchii

    if (stare,cuvant) in muchii:
        return muchii[(stare,cuvant)]

    return None

def lamb():
    global lambdas
    b = 0

    for element in lambdas:
        # print(element)
        if (element[2],'.') in muchii.keys():
            for value in muchii[(element[2],'.')]:
                if [element[0],'.',value] not in lambdas:
                    lambdas += [[element[0],'.',value]]

    if b == 1:
        lamb()

# ===================================================
simple = True;
fisier = True;
# ===================================================


f = open("LNFA.txt")
nrAcceptate = 0

nrS = int(f.readline())
NotUsedStari = [int(x) for x in f.readline().split()]

nrA = int(f.readline())
alfabet = [x for x in f.readline().split()]

stareInitiala = int(f.readline())

nrSF = int(f.readline())
stariFinale = [int(x) for x in f.readline().split()]

nrM = int(f.readline())
muchii = {}
lambdas = []
for i in range(nrM):
    inputs = f.readline().split()
    inputs = [int(inputs[0]), inputs[1], int(inputs[2])]

    if (inputs[0],inputs[1]) in muchii:
        muchii[(inputs[0],inputs[1])].append(inputs[2])
    else:
        muchii[(inputs[0],inputs[1])] = [inputs[2]]

    if inputs[1] == ".":
        lambdas += [inputs]

# print(lambdas)
lamb()

for lamb in lambdas:
    for a in muchii[(lamb[0],lamb[1])]:
        for letter in alfabet:
            if (a,letter) in muchii:
                if (lamb[0],letter) in muchii:
                    muchii[(lamb[0],letter)] += muchii[(a, letter)]
                else:
                    muchii[(lamb[0],letter)] = muchii[(a, letter)]

for x in muchii.keys():
    muchii[x] = list(set(muchii[x]))

if simple is True:
    if fisier is True:
        g = open("out.txt", "w")
        nrC = int(f.readline())
        for line in f:
            line = line.rstrip()
            stari = acceptat(line)
            for stare in stari:
                if stare in stariFinale:
                    g.write("DA\n");
                    line = -1
                    nrAcceptate += 1
                    break
            if line != -1:
                g.write("NU\n");

    if fisier is False:
        nrC = int(f.readline())
        for line in f:
            line = line.rstrip()
            stari = acceptat(line)
            for stare in stari:
                if stare in stariFinale:
                    print("DA")
                    line = -1
                    nrAcceptate += 1
                    break
            if line != -1:
                print("NU")

if simple is False:
    nrC = int(f.readline())
    for line in f:
        line = line.rstrip()
        stari = acceptat(line)
        print(f"Starile finale ale cuvantului {line} sunt {stari} si este", end = " ")
        for stare in stari:
            if stare in stariFinale:
                print("Acceptat")
                line = -1
                nrAcceptate += 1
                break
        if line != -1:
            print("Respins")

    print(nrAcceptate)


f.close()