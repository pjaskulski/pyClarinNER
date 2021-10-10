import spacy


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


def analiza(text):
    doc = nlp(text)
    osoby = []
    miejsca = []
    for entity in doc.ents:
        if entity.label_ == 'persName':
            osoby.append(f'{entity.text} ({entity.label_})')
        elif entity.label_ == 'geogName':
            miejsca.append(f'{entity.text} ({entity.label_})')
        elif entity.label_ == 'placeName':
            miejsca.append(f'{entity.text} ({entity.label_})')
    
    return osoby, miejsca

def process_file(filename):
    texts = read_texts(filename)
    fname_base = filename.replace('.txt', '')
    with open(f'report_{fname_base}_spaCy_pl_core_news_lg.txt', 'w', encoding='utf-8') as f:
        for text in texts:
            osoby, miejsca = analiza(text)
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
    nlp = spacy.load("pl_core_news_lg")
    process_file(filename='bibliografia.txt')
    process_file(filename='mix.txt')
    process_file(filename='urzednicy.txt')
             