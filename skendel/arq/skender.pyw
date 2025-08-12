import tkinter as tk
import ast

janela = tk.Tk()
janela.resizable(False, False)
janela.geometry('1250x900')
janela.title("slk")

def analise(exp, text):
    biblio = ""
    with open("biblioteca.txt", "r", encoding='utf-8') as file:
        biblio = ast.literal_eval(file.read())

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

    j = -1
    i = 0
    ruleQ = []
    while j <= len(text) and i <= len(text):
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
                while k <= len(text):
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


###############################################


def enviar():
    user_text = text.get("1.0", tk.END).strip()
    user_exp = input.get("1.0", tk.END).strip()
    result = analise(user_exp, user_text)
    output.config(state=tk.NORMAL)
    output.delete("1.0", tk.END)
    output.insert(tk.END, str(result[1][1:]))
    janela.update()

def atualizar(*args):
    text = input.get("1.0", tk.END).strip()
    text = text.replace("\n", "")
    input.delete("1.0", tk.END)
    input.insert(tk.END, text)
    input.mark_set("insert", "1.0")
    input.tag_remove("sel", "1.0", "end")

    enviar()

def brilhe():
    output.tag_add("h")

#################################################################
textoinput2 = tk.Label(janela, text="Resultado:")
textoinput2.grid(row=0, column=2, padx=10, pady=10)

output = tk.Text(janela, height=50, width=75, state=tk.DISABLED)
output.grid(row=1, column=2, padx=10, pady=10)

input = tk.Text(janela, height=1, width=75)
input.grid(row=0, column=1, padx=10, pady=10)
input.bind("<Return>", atualizar)

text = tk.Text(janela, height=50, width=75)
text.grid(row=1, column=1, padx=10, pady=10)
text.bind("<KeyRelease>", atualizar)

text.insert(tk.END, 'Durante a reunião realizada na última #sexta-feira, foi decidido que o responsável técnico pelo #projeto será João Henrique da Silva, CPF 123.456.789-09, que já atuou em iniciativas semelhantes no passado. A equipe aprovou por unanimidade a sua indicação, destacando sua experiência e comprometimento com prazos. Além disso, definiu-se que todos os relatórios deverão ser entregues até às 18h00 de cada sexta-feira — sem exceções! Os formatos aceitos incluem: .pdf, .docx, e .xlsx; arquivos fora desses padrões serão rejeitados. Para dúvidas, os contatos disponíveis são: joao.henrique@empresa.com, suporte@projeto.org ou (11) 91234-5678. Ressaltou-se ainda que a identificação dos arquivos deverá seguir o padrão: nome_arquivo@data.extensão (exemplo: relatorio_final@15-05-2025.pdf). A diretoria alertou: “Atrasos recorrentes poderão gerar advertências formais — inclusive suspensão temporária das atividades!”')

janela.mainloop()