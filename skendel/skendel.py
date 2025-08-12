import time

def analise(exp, text):
    biblio = ""
    with open("s/biblioteca.txt", "r", encoding='utf-8') as file:
        conteudo = file.read().split("\n")
        for i in range(0, len(conteudo)):
            conteudo[i] = set(conteudo[i])

        biblio = conteudo

    exp = " "+exp+" "
    rules = []
    i = 0
    while i < len(exp):
        if exp[i] == "<" and exp[i-1] != "#":
            rule = ""
            tkns = "#<>"
            if exp[i+1] == "#":
                rule += "#"
                i+=2
            else:
                i += 1
            while exp[i] != ">":
                if exp[i] == "#" and exp[i+1] in tkns:
                    rule += exp[i+1]
                    i += 2
                else:
                    rule += exp[i]
                    i += 1
            rules.append(rule)
        i += 1

    result = ""
    currentExp = ""


    sucessFlag = True

    leng = len(text)

    j = -1
    i = 0
    ruleQ = []

    while j <= leng and i <= leng:

        if ruleQ == []:
            if sucessFlag == False:
                j += 1
                i = j
                sucessFlag = True
            else:
                j = i
                result += currentExp
                result += "\n"
            ruleQ = rules[:]
            currentExp = ""
        ruleC = ruleQ[0]

        if ruleC[0] == "#": #text match (qualquer coisa que vier depois de "#")
            if ruleC != "#":
                comprimento = len(ruleC[1:])
                if text[i:i+comprimento] == ruleC[1:]:
                    currentExp+=text[i:i+comprimento]
                    i += comprimento-1
                else:
                    currentExp = ""
                    ruleQ == []
                    sucessFlag = False

        elif ruleC[0] in "duapg": #digit/char match (n? que vier depois da letra)
            idmap = {"p":0,"d":1,"u":2,"a":3,"g":4}
            compCharMap = biblio[idmap[ruleC[0]]]

            comprimento = len(ruleC[1:])
            if comprimento > 0:
                analise = text[i:i+comprimento]
                analisado = ""
                for char in analise:
                    if char in compCharMap:
                        analisado += char
                
                if analisado == analise:
                    currentExp+=text[i:i+comprimento]
                    i += comprimento-1
                else:
                    currentExp = ""
                    ruleQ == []
                    sucessFlag = False

        elif ruleC[0] == "t": #till matches
            matches = ruleC[4:]
            if matches != "":
                comprimento = len(matches)
                k = i
                while k <= leng:
                    if text[k:k+comprimento] == matches:
                        currentExp+=text[i:k+comprimento]
                        i += (k+comprimento-i)-1
                        break
                    k += 1
                if text[k:k+comprimento] != matches:
                    currentExp = ""
                    ruleQ == []
                    sucessFlag = False

        ruleQ.pop(0)
        i += 1

    return(text, result)

ans = ""
text = ""
filename = ""

while (True):
    store = False
    exp = input(" --> ")
    
    if "<" not in exp:
        if exp == "help":
            
            print("="*30)
            print("Para saber comandos    : 1")
            print("para saber analisadores: 2")
            print("="*30)

            choice = input(" --> ")
            if choice == "1":
                print("="*30)
                print("Para sair digite: /")
                print("Para selecionar o arquivo txt a ser analisado digite seu nome sem a extensão: (analise.txt) --> analise")
            elif choice == "2":
                print("="*30)
                with open("s/tutorial.txt", "r", encoding="utf-8") as tut:
                    print(tut.read())
            print("="*30)

        elif exp == "/":
            break
        else:
            with open(f"{exp}.txt" , "r", encoding="utf-8") as f:
                filename = f"{exp}Skended.txt"
                text = f.read()
    else:
        if exp[0] == "w":
            store = True
            exp = exp[1:]

        curr = time.time()
        ans = (analise(exp, text)[1])
        print(f"\n{(time.time()-curr):.2f}s")
        if store:
            with open(filename, "w", encoding="utf-8") as o:
                o.write(str(ans))
        else:
            print(ans)