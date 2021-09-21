# testy usługi NER z CLARIN-PL

from clarinner import ClarinNER


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


def get_person_city_liner2(text):
    """ Przetwarzanie podanego tekstu przez usługę NER (Liner2) z CLARIN-PL
        w celu wyszukania miejscowości i osób
    """
    if text == "":
        return
    else:
        print(f"TEXT: {text}")

    # instancja klasy ClarinNER 
    cl = ClarinNER()

    resp, status = cl.process(text)
    if resp:
        # wyszukiwanie osób w tekście
        osoby = cl.get_persons()
        print("Osoby:")
        if len(osoby) > 0:
            for item in osoby:
                print(f"\t{item}")

        # wyszukiwanie miejscowości w tekście
        miejsca = cl.get_cities()
        print("Miejsca:")
        if len(miejsca) > 0:
            for item in miejsca:
                print(f"\t{item}")
        
        print()

    else:
        print(f"Error, status code = {status}")


def get_person_city_poldeep(text):
    """ Przetwarzanie podanego tekstu przez usługę NER (PolDeepNer2) z CLARIN-PL
        w celu wyszukania miejscowości i osób
    """
    if text == "":
        return
    else:
        print(f"TEXT: {text}")

    # instancja klasy ClarinNER 
    cl = ClarinNER()

    resp, status = cl.process(text, lpmn='any2txt|poldeepner2')
    if resp:

        # wyszukiwanie osób w tekście
        osoby = cl.get_persons()
        print("Osoby:")
        if len(osoby) > 0:
            for item in osoby:
                print(f"\t{item}")

        # wyszukiwanie miejscowości w tekście
        miejsca = cl.get_cities()
        print("Miejsca:")
        if len(miejsca) > 0:
            for item in miejsca:
                print(f"\t{item}")

    else:
        print(f"Error, status code = {status}")


if __name__ == "__main__":
    
    # fragmenty z urzędników małopolskich        
    teksty = read_texts("texts/urzednicy.txt")
    for item in teksty:
        get_person_city_liner2(item)
    for item in teksty:
        get_person_city_poldeep(item)


    # fragmenty z bibliografii
    teksty = read_texts("texts/bibliografia.txt")
    for item in teksty:
        get_person_city_liner2(item)
    for item in teksty:
        get_person_city_poldeep(item)


    # teksty z różnych źródeł
    teksty = read_texts("texts/mix.txt")
    for item in teksty:
        get_person_city_liner2(item)
    for item in teksty:
        get_person_city_poldeep(item)


