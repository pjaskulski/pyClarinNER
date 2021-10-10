from deeppavlov import configs, build_model

def read_texts(file_name) -> list:
    """ Wczytywanie tekstów do analizy z plików tekstowych
        Przykładowe teksty oddzielone przez wiersz '---'
    """
    texts = []
    text = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line != "" and line != "---":
                text.append(line)
            elif line == "---":
                texts.append(" ".join(text))
                text = []
        
        if len(text) > 0:
            texts.append(" ".join(text))
    
    return texts


def analiza(ner_model, text):
    result = ner_model([text])

    sentence = result[0][0]
    ner = result[1][0]
    lista = zip(sentence, ner)

    osoba = miejsce = ""
    osoby = [] 
    miejsca = []

    for item in lista:
        word, find_ner = item
        if find_ner == 'B-PERSON':
            if osoba != "": 
                osoby.append(osoba)
            if miejsce != "":
                miejsca.append(miejsce)
                miejsce = ""
            osoba = word  + '(' + find_ner + ')'
        elif find_ner == "I-PERSON":
            osoba += ' ' + word  + '(' + find_ner + ')'
        elif find_ner == 'B-GPE':
            if miejsce != "": miejsca.append(miejsce)
            if osoba != "": 
                osoby.append(osoba)
                osoba = "" 
            miejsce = word + ' ('+find_ner+')'
        elif find_ner == 'I-GPE':
            miejsce += ' ' + word + '(' + find_ner + ')'
        else: 
            if osoba != "":
                osoby.append(osoba)
                osoba = ""
            if miejsce != "":
                miejsca.append(miejsce)
                miejsce = ""

    if osoba != "": osoby.append(osoba)
    if miejsce != "": miejsca.append(miejsce) 

    return osoby, miejsca

def process_file(ner_model, filename):
    texts = read_texts(filename)
    fname_base = filename.replace('.txt', '')
    with open(f'result_{fname_base}_deeppavlov_slavicBERT.txt', 'w', encoding='utf-8') as f:
        for text in texts:
            osoby, miejsca = analiza(ner_model, text)
            f.write(f'TEXT: {text} \n\n')
            f.write('Osoby:\n')
            for item in osoby:
                f.write(f'\t{item}\n')
            f.write('\n')

            f.write('Miejsca:\n')
            for item in miejsca:
                f.write(f'\t{item}\n')
            f.write('\n')

        f.write('\n\n')

if __name__ == '__main__':
    ner_model = build_model(configs.ner.ner_ontonotes_bert_mult_torch, download=False)
    process_file(ner_model, filename='bibliografia.txt')
    process_file(ner_model, filename='mix.txt')
    process_file(ner_model, filename='urzednicy.txt')
             