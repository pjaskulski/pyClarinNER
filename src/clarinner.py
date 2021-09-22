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
            self.result = self.result.strip()
            return True, "" 
        else:
            self.result = ""
            return False, str(r.status_code) 


    def result_type(self):
        if self.result[:2] == "[{":
            return 'json'
        elif self.result[:5] == "<?xml":
            return 'xml'
        else:
            return 'none'


    def get_xml(self):
        if self.result.strip()[:5] == "<?xml":
            return self.result
        else:
            return ""    


    def get_json(self):
        if self.result.strip()[:2] == "[{":
            return self.result
        else:
            return ""

    def get_dict(self):
        if self.result.strip()[:2] == "[{":
            return json.loads(self.result.strip())
        else:
            return ""    


    def get_html(self):
        pass


    def is_person(self, tok):
        isPerson = False
        label = ""
        labels = ["nam_liv_person", 
                  "nam_liv"]
        for ann in tok.findall('ann'):
            chan = ann.get('chan')
            if chan in labels and int(ann.text) > 0:
                isPerson = True
                if label == "":
                    label += chan
                else:
                    label += ", " + chan

        return isPerson, f"{label}"


    def is_city(self, tok) -> tuple:
        isCity = False
        label = ""
        #name = tok.find('orth').text
        labels = ["nam_loc_gpe_city", 
                  "nam_loc_hydronym_river",
                  "nam_loc_gpe_country",
                  "nam_loc_historical_region", 
                  "nam_loc"]
        for ann in tok.findall('ann'):
            chan = ann.get('chan')
            if chan in labels and int(ann.text) > 0:
                isCity = True
                if label == "":
                    label += chan
                else:
                    label += ", " + chan
                
        return isCity, f"{label}"
        

    def get_persons(self) -> list:
        result_type = self.result_type()
        if result_type == 'xml':
            return self.get_persons_xml()
        elif result_type == 'json':
            return self.get_persons_json()
        else:
            return []


    def get_persons_xml(self) -> list:
        root = ET.fromstring(self.result)
        persons = []
        isPerson = False
        person = ""
        for chunk in root.iter('chunk'):
            for sentence in chunk.findall('sentence'):
                for tok in sentence.findall('tok'):
                    orth = tok.find('orth').text
                    ok, label = self.is_person(tok)
                    if ok:
                        if isPerson:
                            person += f" {orth} ({label})"
                        else:
                            person = f"{orth} ({label}) "
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
    

    def get_persons_json(self) -> list:
        persons = []
        labels = []
        output = json.loads(self.result)
        for item in output:
            entities = item['entities']
            for ent in entities:
                if ent['label'] == "nam_liv_person":
                    persons.append(f"{ent['text']} - {ent['label']}")
        
        return persons


    def get_cities(self) -> list:
        result_type = self.result_type()
        if result_type == 'xml':
            return self.get_cities_xml()
        elif result_type == 'json':
            return self.get_cities_json()
        else:
            return []


    def get_cities_xml(self) -> list:
        root = ET.fromstring(self.result)
        cities = []
        isCity = False
        city = ""
        label = ""
        for chunk in root.iter('chunk'):
            for sentence in chunk.findall('sentence'):
                for tok in sentence.findall('tok'):
                    orth = tok.find('orth').text
                    ok, label = self.is_city(tok)
                    if ok:
                        if isCity:
                            city += f" {orth} ({label})"
                        else:
                            city = f"{orth} ({label})"
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
    

    def get_cities_json(self) -> list:
        cities = []
        labels = ["nam_loc_gpe_city", 
                  "nam_loc_gpe_district",
                  "nam_loc_gpe_country",
                  "nam_loc_gpe_subdivision",
                  "nam_loc_country_region",
                  "nam_loc_hydronym_river",
                  "nam_loc_hydronym_lake",
                  "nam_loc_hydronym_ocean",
                  "nam_loc_hydronym_sea",
                  "nam_loc_hydronym",
                  "nam_loc_land_continent",
                  "nam_loc_land_island",
                  "nam_loc_land_region",
                  "nam_loc_land", 
                  "nam_loc_historical_region",
                  "nam_loc_land_mountain",
                  "nam_loc"]
        output = json.loads(self.result)
        for item in output:
            entities = item['entities']
            for ent in entities:
                if ent['label'] in labels:
                    cities.append(f"{ent['text']} - {ent['label']}")
        
        return cities