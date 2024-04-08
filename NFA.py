def accepta_cuvant(muchii, cuvant, stareInitiala, stariFinale):
    stari_actuale = [stareInitiala]
    for litera in cuvant:
        stari_noi = []
        for stare in stari_actuale:
            if stare in muchii and litera in muchii[stare]:
                stari_noi.extend(muchii[stare][litera])
        stari_actuale = stari_noi

    for stare in stari_actuale:
        if stare in stariFinale:
            return True
    return False

''' =================================================================================== '''

printer = 0 # variabila pt debbuging

f = open("NFA.txt")
g = open("out.txt","w")

n = f.readline()
n = f.readline()
n = f.readline()
n = f.readline()
stareInitiala = int(f.readline())
n = f.readline()
stariFinale = [int(x) for x in f.readline().split()]

n = int(f.readline())
muchii = {}
for _ in range(n):
    stareInceput, litera, stareSfarsit = f.readline().split()
    stareInceput, stareSfarsit = int(stareInceput), int(stareSfarsit)

    if stareInceput not in muchii:
        muchii[stareInceput] = {}
    if litera not in muchii[stareInceput]:
        muchii[stareInceput][litera] = []

    muchii[stareInceput][litera].append(stareSfarsit)

if printer == 1:
    print(*muchii.items(), sep="\n")

m = int(f.readline())
for _ in range(m):
    cuvant = f.readline().strip()
    
    if(printer == 1):
        g.write(cuvant)
        g.write(" ")
        
    if accepta_cuvant(muchii, cuvant, stareInitiala, stariFinale):
        g.write("DA\n")
    else:
        g.write("NU\n")
