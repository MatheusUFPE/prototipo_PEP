import csv
import os

class CSVfile:

    def __init__(self, filename):
        self.filename = filename

    def create_csvFile(self) -> None:
        """Create a CSV file if the file does not exist."""

        if not os.path.exists(self.filename):
            headers = ['Nome','Data de nascimento','Idade', 'Sexo','CPF','Naturalidade','Endereço', 
                       'Celular','E-mail','Alergias','Convênio','Plano','Número']
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)

    def fill_csvFile(self, patient_dict : dict) -> bool:
        """Add a new patient to the CSV file."""

        try:   
            with open(self.filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                patient_dict['address'] = "{},{} - {}, {}/{} CEP: {}".format(patient_dict['address']['logradouro'],
                                                                             patient_dict['address']['complemento'],
                                                                             patient_dict['address']['bairro'],
                                                                             patient_dict['address']['localidade'],
                                                                             patient_dict['address']['uf'],
                                                                             patient_dict['address']['cep'])
                writer.writerow(patient_dict.values())
                return True
            
        except PermissionError as error:
            print("Close the CSV file before adding a new patient.")
            return False
    
    def edit_csvFile(self, new_patient_dict : dict, index : int) -> None:

        rows = self.read_all()
        rows[index] = new_patient_dict.values()

        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    
    def read_all(self) -> list:

        rows = []
        with open(self.filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row)
                
        return rows

    def csv_Anamnesis(self, anamnesis, person) -> None:
        """"""
        
        if not os.path.exists(self.filename):
            headers = ['Nome', 'CPF', 'Data', 'Peso, kg', 'Altura, cm', 'Temperatura,°C', 'Pressão sanguínea, mmHg', 
                       'Reclamação','Sintomas', 'Histórico', 'Hábitos']
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            dict_aux = {'Nome': person['Nome'], 'CPF': person['CPF'] }
            for key, value in anamnesis.items():
                dict_aux[key] = value
            writer.writerow(dict_aux.values())
            
            