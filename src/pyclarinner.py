# testy usługi NER z CLARIN-PL

from clarinner import ClarinNER
import os

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


def get_person_city_liner2(filename, output_dir) -> None:
    """ Przetwarzanie podanego pliku przez usługę NER (Liner2) z CLARIN-PL
        w celu wyszukania elementów 'geograficznych' (miejscowości, pasma górskie, 
        rzeki, kraje, krainy) i osób.

        filename - ścieżka do pliku z tekstami (każda próbka rozdzielona 
        wierszem: ---)

        output_dir - ścieżka do katalogu, gdzie ma być zapisany raport
    """

    if filename == "": 
        print("Nie podano nazwy pliku z tekstami.")
        return

    # wczytanie próbek tekstów
    teksty = read_texts(filename)
    if len(teksty) == 0:
        print(f"Pusty plik: {filename}")
        return
    
    if output_dir.strip() == "":
        print("Nie wskazano folderu wyjściowego.")
        return

    basename = os.path.basename(filename)
    if basename[-4:] == ".txt":
        basename = basename[:-4]
    if output_dir[-1] == "\\" or output_dir[-1] == "/":
        output_dir = output_dir[:-1]

    print(f"Liner2, przetwarzanie pliku: {filename}\n")

    # instancja klasy ClarinNER 
    cl = ClarinNER()

    with open(f"{output_dir}/report_{basename}_Liner2.txt", "w", encoding='utf-8') as f:
        for text in teksty:
            resp, status = cl.process(text)
            if resp:
                # przetwarzany tekst
                f.write(f"TEXT: {text}\n\n")
                
                # wyszukiwanie osób w tekście
                osoby = cl.get_persons()
                f.write("Osoby:\n")
                if len(osoby) > 0:
                    for item in osoby:
                        f.write(f"\t{item}\n")

                # wyszukiwanie miejscowości w tekście
                miejsca = cl.get_cities()
                f.write("Miejsca:\n")
                if len(miejsca) > 0:
                    for item in miejsca:
                        f.write(f"\t{item}\n")
        
                f.write("\n\n")

            else:
                print(f"Error, status code = {status}")
                break


def get_person_city_poldeep(filename, output_dir) -> None:
    """ Przetwarzanie podanego pliku przez usługę NER (PolDeepNer2) z CLARIN-PL
        w celu wyszukania elementów 'geograficznych' (miejscowości, pasma górskie, 
        rzeki, kraje, krainy) i osób

        filename - ścieżka do pliku z tekstami (każda próbka rozdzielona 
        wierszem: ---)

        output_dir - ścieżka do katalogu, gdzie ma być zapisany raport
    """

    if filename == "": 
        print("Nie podano nazwy pliku z tekstami.")
        return

    # wczytanie próbek tekstów
    teksty = read_texts(filename)
    if len(teksty) == 0:
        print(f"Pusty plik: {filename}")
        return
    
    if output_dir.strip() == "":
        print("Nie wskazano folderu wyjściowego.")
        return

    basename = os.path.basename(filename)
    if basename[-4:] == ".txt":
        basename = basename[:-4]
    if output_dir[-1] == "\\" or output_dir[-1] == "/":
        output_dir = output_dir[:-1]

    print(f"PolDeepNer2, przetwarzanie pliku: {filename}\n")

    # instancja klasy ClarinNER 
    cl = ClarinNER()

    with open(f"{output_dir}/report_{basename}_PolDeepNer2.txt", "w", encoding='utf-8') as f:
        for text in teksty:
            resp, status = cl.process(text, lpmn='any2txt|poldeepner2')
            if resp:
                #if "Czechow" in cl.result: print(cl.get_dict())
                # przetwarzany tekst
                f.write(f"TEXT: {text}\n\n")
                
                # wyszukiwanie osób w tekście
                osoby = cl.get_persons()
                f.write("Osoby:\n")
                if len(osoby) > 0:
                    for item in osoby:
                        f.write(f"\t{item}\n")

                # wyszukiwanie miejscowości w tekście
                miejsca = cl.get_cities()
                f.write("Miejsca:\n")
                if len(miejsca) > 0:
                    for item in miejsca:
                        f.write(f"\t{item}\n")
            
                f.write("\n\n")

            else:
                print(f"Error, status code = {status}")
                break


if __name__ == "__main__":
    
    pliki = []
    output_dir = "output"
    
    pliki.append("texts/urzednicy.txt")    # fragmenty z urzędników małopolskich        
    pliki.append("texts/bibliografia.txt") # fragmenty z bibliografii
    pliki.append("texts/mix.txt")          # teksty z różnych źródeł
    
    for plik in pliki:
        get_person_city_liner2(plik, output_dir)
        get_person_city_poldeep(plik, output_dir)
