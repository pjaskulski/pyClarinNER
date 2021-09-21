import json
import requests
import xml.etree.ElementTree as ET


class ClarinNER:
    url = "http://ws.clarin-pl.eu/nlprest2/base/process"

    def __init__(self, user = "tester@ihpan.edu.pl") -> None:
        self.user = user
        self.result = ""


    def process(self, doc, lpmn = 'any2txt|wcrft2|liner2({"model":"all"})') -> tuple:

        query = {'text': doc, 'lpmn': lpmn, 'user': self.user}

        try:
            r = requests.post(ClarinNER.url, data=json.dumps(query))
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
    
        if r.ok:
            self.result = r.content.decode(encoding="utf-8")
            return True, "" 
        else:
            self.result = ""
            return False, str(r.status_code) 


    def get_xml(self):
        return self.result    


    def get_html(self):
        pass


    def is_person(self, tok):
        isPerson = False

        for ann in tok.findall('ann'):
            chan = ann.get('chan')
            if chan in ["nam_liv_person", "nam_liv"] and int(ann.text) > 0:
                isPerson = True
                break

        return isPerson


    def is_city(self, tok):
        isCity = False

        for ann in tok.findall('ann'):
            chan = ann.get('chan')
            if chan in ["nam_loc_gpe_city"] and int(ann.text) > 0:
                isCity = True
                break

        return isCity
        

    def get_persons(self) -> list:
        if self.result == "":
            return []
        
        root = ET.fromstring(self.result)
        persons = []
        isPerson = False
        person = ""
        for chunk in root.iter('chunk'):
            for sentence in chunk.findall('sentence'):
                for tok in sentence.findall('tok'):
                    orth = tok.find('orth').text
                    if self.is_person(tok):
                        if isPerson:
                            person += " " + orth
                        else:
                            person = orth
                            isPerson = True
                    else:
                        if isPerson:
                            persons.append(person)
                            person = ""
                            isPerson = False
            
                if person != "":
                    persons.append(person)
                    person = ""
                    isPerson = False
        
        return persons


    def get_cities(self) -> list:
        if self.result == "":
            return []
        
        root = ET.fromstring(self.result)
        cities = []
        isCity = False
        city = ""
        for chunk in root.iter('chunk'):
            for sentence in chunk.findall('sentence'):
                for tok in sentence.findall('tok'):
                    orth = tok.find('orth').text
                    if self.is_city(tok):
                        if isCity:
                            city += " " + orth
                        else:
                            city = orth
                            isCity = True
                    else:
                        if isCity:
                            cities.append(city)
                            city = ""
                            isCity = False
            
                if city != "":
                    cities.append(cities)
                    city = ""
                    isCity = False
        
        return cities