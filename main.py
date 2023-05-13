from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
from id import Id
from patient import Patient
from anamnesis import Anamnesis
from functions import *
from csvFile import CSVfile
import chardet

class GUI(QMainWindow):
    """Class responsable for the graphic user interface. It is also the main code."""

    def __init__(self):
        super(GUI, self).__init__()
        self.newPatient_window = uic.loadUi('patientID.ui')
        self.patientsList_window = uic.loadUi('patientsList.ui')
        self.individualInfo_window = uic.loadUi('Individual_info.ui')
        self.anamnesis_window = uic.loadUi('newAnamnesis.ui')
        self.viewAnamnesis_window = uic.loadUi('viewAnamnesis.ui')
        self.csv_obj = CSVfile('PatientList.csv')
        self.csv_anamnesis = CSVfile('AnamnesisList.csv')
        self.csv_obj.create_csvFile()
        self.people_list = self.load_data(self.csv_obj.filename)

        self.patientsList_window.show()
        self.patientsList_window.tableWidget.setColumnWidth(0,100)
        self.patientsList_window.tableWidget.setColumnWidth(1,80)
        self.patientsList_window.tableWidget.setColumnWidth(2,160)
        self.patientsList_window.tableWidget.setColumnWidth(3,100)
        self.patientsList_window.pushButton_Select.clicked.connect(self.select_patient)
        self.patientsList_window.actionSair.triggered.connect(exit)
        self.patientsList_window.actionNovo_cadastro.triggered.connect(self.open_newPatient_window)
        self.patientsList_window.searchField.textChanged.connect(self.search_patient)
        
        self.individualInfo_window.pushButton_editPatient.clicked.connect(self.edit_patient)
        self.individualInfo_window.pushButton_addAnamnesis.clicked.connect(self.add_new_anamnesis)
        self.individualInfo_window.pushButton_CancelA.clicked.connect(self.close_individualInfo_window)
        self.individualInfo_window.pushButton_viewAnamnesis.clicked.connect(self.view_anamnesisData)
        
        self.newPatient_window.cpfField.textChanged.connect(self.check_cpf)
        self.newPatient_window.pushButton_OK.clicked.connect(self.complete_address)
        self.newPatient_window.pushButton_Cancel.clicked.connect(self.close_newPatient_window)
        self.newPatient_window.pushButton_Save.clicked.connect(self.save_newPatient)
        
        self.anamnesis_window.pushButton_CancelA.clicked.connect(self.close_anamnesis_window)
        self.anamnesis_window.pushButton_SaveA.clicked.connect(self.save_newAnamnesis)

        self.viewAnamnesis_window.pushButton_CancelA.clicked.connect(self.close_viewAnamnesis_window)

    def search_patient(self) -> None:
        """Look for a patient in the database and return a list with the matching patients."""

        search = self.patientsList_window.searchField.text().upper()
        results = self.get_results(search)
        self.show_results(results)

    def get_results(self, search : str) -> list:
        """Get a list of patients whose names match the search."""

        names = [row['Nome'] for row in self.people_list]
        results = []
        for i, name in enumerate(names):
            if search in name.upper():
                results.append(self.people_list[i])
        return results
    
    def show_results(self, results : list) -> None:
        """Update the table in the GUI to show the matching patients to the search."""

        row = 0
        self.patientsList_window.tableWidget.setRowCount(len(results))
        for person in results:
            self.patientsList_window.tableWidget.setItem(row, 0, QTableWidgetItem(person['Nome']))   
            self.patientsList_window.tableWidget.setItem(row, 1, QTableWidgetItem(person['CPF']))
            self.patientsList_window.tableWidget.setItem(row, 2, QTableWidgetItem(person['E-mail']))
            self.patientsList_window.tableWidget.setItem(row, 3, QTableWidgetItem(person['Celular']))
            row += 1
    
    def open_newPatient_window(self) -> None:
        """Open New Patient Window."""

        self.newPatient_window.show()
    
    def close_newPatient_window(self) -> None:
        """Clear all fields from the New Patient Window and close the window."""

        self.clear_newPatient_fields()
        self.newPatient_window.close()

    def add_new_patient(self) -> None:
        """Get the values inserted by the user for new patient register."""
    
        try:
            self.name = self.newPatient_window.nameField.text()
            self.birthdate = self.newPatient_window.birthdateField.text()
            self.age = calculate_age(self.birthdate)
            self.select_gender()
            self.cpf = self.newPatient_window.cpfField.text()
            if len(self.cpf) < 11:
                QMessageBox.about(self.newPatient_window, 'Erro', 'CPF com dígitos insuficientes.')
                self.newPatient_window.cpfField.setText('')
            self.place_of_birth = self.newPatient_window.placeOfBirthField.text()
            self.select_insurance_name()
            self.insurance_plan = self.newPatient_window.insurancePlanField.text()
            self.insurance_number = self.newPatient_window.insuranceNumberField.text()
            self.address_number = self.newPatient_window.addressNumberField.text()
            self.address_complement = self.newPatient_window.addressComplementField.text()
            self.phone = self.newPatient_window.phoneField.text()
            self.email = self.newPatient_window.emailField.text()
    
        except Exception as error:
            raise error

    def check_fields(self) -> bool:
        """Check if all fields from the New Patient Window are filled."""

        fields = [self.name, self.birthdate, self.age, self.gender, self.cpf, self.place_of_birth, self.insurance_name, self.insurance_plan,
                  self.insurance_number, self.cep, self.address_number, self.address_complement, self.phone, self.email]
        if any(field == '' for field in fields):
            QMessageBox.about(self.newPatient_window, 'Erro', 'Preencher todos os campos.')
            return False
        else:
            return True 
        
    def save_newPatient(self) -> None:
        """Save new patient data to the database if all fields are filled."""
        
        self.add_new_patient()
        if self.check_fields() == True:
            try:
                self.patient = Patient(Id(self.name, self.birthdate, self.gender, self.cpf, self.place_of_birth, self.cep, 
                                          self.address_number, self.address_complement, self.phone, self.email), 
                                          self.insurance_name, self.insurance_plan, self.insurance_number)
            
                self.patient_dict = convert_toDict(self.patient)
                if self.csv_obj.fill_csvFile(self.patient_dict) == False:
                    QMessageBox.about(self.newPatient_window,'Permissão negada','Feche a planilha antes de adicionar um paciente.')

            except Exception as error:
                raise error
            
            QMessageBox.about(self.patientsList_window, 'Cadastro OK', 'Cadastro concluído com sucesso.')
            self.show_results(self.load_data(self.csv_obj.filename))
            self.close_newPatient_window()
        
    def clear_newPatient_fields(self) -> None:
        """Clear all fields from the New Patient Window."""

        self.newPatient_window.nameField.setText('')
        self.newPatient_window.birthdateField.setDate(convert_toDatetime('01/01/2000'))
        self.newPatient_window.genderField.clearSelection()
        self.newPatient_window.placeOfBirthField.setText('')
        self.newPatient_window.cpfField.setText('')
        self.newPatient_window.insuranceNameField.clearSelection()
        self.newPatient_window.insurancePlanField.setText('')
        self.newPatient_window.insuranceNumberField.setText('')
        self.newPatient_window.cepField.setText('')
        self.newPatient_window.addressField.setText('')
        self.newPatient_window.addressNumberField.setText('')
        self.newPatient_window.addressComplementField.setText('')
        self.newPatient_window.neighborhoodField.setText('')
        self.newPatient_window.cityField.setText('')
        self.newPatient_window.stateField.setText('')
        self.newPatient_window.phoneField.setText('')
        self.newPatient_window.emailField.setText('')

    def select_gender(self) -> None:
        """Select the gender in a QListWidget."""

        selected_item = self.newPatient_window.genderField.currentItem()
        if selected_item is not None:
            self.gender = selected_item.text()
            
    def select_insurance_name(self) -> None:
        """Select the health insurance name in a QListWidget."""

        selected_item = self.newPatient_window.insuranceNameField.currentItem()
        if selected_item is not None:
            self.insurance_name = selected_item.text()

    def complete_address(self) -> None:
        """Verify the cep code using an API and complete the address information."""

        dict_cep = {}
        self.cep = self.newPatient_window.cepField.text()
        if self.newPatient_window.pushButton_OK.clicked and self.cep != '':
            dict_cep = verify_cep(self.cep)

            # If CEP not found, clear all fields related to the address and pops up a message.
            if dict_cep['erro'] == True:
                QMessageBox.about(self.newPatient_window, 'Erro', 'CEP não encontrado.')
                self.newPatient_window.cepField.setText('')
                self.newPatient_window.addressField.setText('')
                self.newPatient_window.addressNumberField.setText('')
                self.newPatient_window.addressComplementField.setText('')
                self.newPatient_window.neighborhoodField.setText('')
                self.newPatient_window.cityField.setText('')
                self.newPatient_window.stateField.setText('')
            elif dict_cep['invalido'] == True:
                QMessageBox.about(self.newPatient_window, 'Erro', 'CEP inválido.')
                self.newPatient_window.cepField.setText('')
                self.newPatient_window.addressField.setText('')
                self.newPatient_window.addressNumberField.setText('')
                self.newPatient_window.addressComplementField.setText('')
                self.newPatient_window.neighborhoodField.setText('')
                self.newPatient_window.cityField.setText('')
                self.newPatient_window.stateField.setText('')
            else:
                dict_cep = get_dict_address(dict_cep)
                try:
                    self.newPatient_window.cityField.setText(dict_cep['localidade'])
                    self.newPatient_window.stateField.setText(dict_cep['uf'])
                    if dict_cep['logradouro'] == '':
                        dict_cep['logradouro'] = self.newPatient_window.addressField.text()
                    else:
                        self.newPatient_window.addressField.setText(dict_cep['logradouro'])
                    if dict_cep['bairro'] == '':
                        dict_cep['bairro'] = self.newPatient_window.neighborhoodField.text()
                    else:
                        self.newPatient_window.neighborhoodField.setText(dict_cep['bairro'])

                except:
                    QMessageBox.about(self.newPatient_window, 'Erro', 'Erro ao preencher o endereço.')
        else: 
            QMessageBox.about(self.newPatient_window, 'Erro', 'Digite um CEP.')

    def check_cpf(self) -> None:
        """Verify if the CPF is valid. If not, it pops up an error message."""
        
        cpf = self.newPatient_window.cpfField.text()
        cpf = re.sub('[^0-9]', '', cpf)
        if len(cpf) == 11:
            cpf = verify_cpf(cpf)['cpf']
            error = verify_cpf(cpf)['error']
            if error == True:
                QMessageBox.about(self.newPatient_window, 'Erro', 'CPF inválido.')
                self.newPatient_window.cpfField.setText('')
            else:
                self.cpf = cpf
            
        elif len(cpf) > 11:
            QMessageBox.about(self.newPatient_window, 'Erro', 'CPF inválido.')
            self.newPatient_window.cpfField.setText('')

    def load_data(self, csv_name):
        """Load the selected data for the patients list and display in the interface."""
        
        #path = f'/home/nayara/Documentos/Técnicas_projeto_final/{csv_name}'
        path = f'C:/Users/User/Documents/Tecnicas computacionais/PEP/{csv_name}'
        new_list = []
        if os.path.exists(path) == False:
            df = pd.DataFrame({})
            df.to_csv(csv_name)

        with open(path, 'rb') as f:
           result = chardet.detect(f.read())
      
        df = pd.read_csv(path, encoding=result['encoding'])

        if df.shape[0] == 0:
            self.patientsList_window.searchField.setText('')
        else:

            for row in range(0,df[df.columns[0]].count()):
                aux_dict = dict()
                for column in list(df.columns):
                    aux_dict[column] = str(df[column][row])
                new_list.append(aux_dict)
        
            row = 0
            self.patientsList_window.tableWidget.setRowCount(len(new_list))
            for person in new_list:
                self.patientsList_window.tableWidget.setItem(row, 0, QTableWidgetItem(person['Nome']))   
                self.patientsList_window.tableWidget.setItem(row, 1, QTableWidgetItem(str(person['CPF'])))
                self.patientsList_window.tableWidget.setItem(row, 2, QTableWidgetItem(str(person['E-mail'])))
                self.patientsList_window.tableWidget.setItem(row, 3, QTableWidgetItem(str(person['Celular'])))
                row += 1
            return new_list

    def select_patient(self) -> None:
        """Select a patient from the list to show their information."""

        self.item = self.patientsList_window.tableWidget.currentRow()
        self.person = self.people_list[self.item]
        self.individualInfo_window.show()
        self.individualInfo_window.label_name.setText(self.person['Nome'])
        self.individualInfo_window.label_cpf.setText(str(self.person['CPF']))
        text = ''
        for k,v in self.person.items():
            text += f'{k}: {v}\n'
        self.individualInfo_window.patient_info.setText(text)

    def close_individualInfo_window(self) -> None:
        """Close Individual Info window."""

        self.individualInfo_window.close()
    
    def edit_patient(self):
         """Get the new values inserted by the user for patient register modification."""
         
         self.open_newPatient_window()
         self.newPatient_window.nameField.setText(self.person['Nome'])
         self.newPatient_window.birthdateField.setDate(convert_toDatetime(self.person['Data de nascimento']))
        
         gender_dict = {'Feminino': 0, 'Masculino': 1, 'Não declarar': 2}
         gender = self.person['Sexo']
         item = self.newPatient_window.genderField.item(gender_dict[gender])
         self.newPatient_window.genderField.setCurrentItem(item)
         
         self.newPatient_window.placeOfBirthField.setText(self.person['Naturalidade'])
         self.newPatient_window.cpfField.setText(str(self.person['CPF']))
         self.newPatient_window.cepField.setText(self.person['Endereço'].split('CEP: ')[1])
         self.complete_address()
         self.newPatient_window.addressNumberField.setText(self.person['Endereço'].split(', ')[1])
         self.newPatient_window.addressComplementField.setText(self.person['Endereço'].split(', ')[2].split('- ')[0])
         self.newPatient_window.phoneField.setText(self.person['Celular'])
         self.newPatient_window.emailField.setText(self.person['E-mail'])
         
         
         insurance_dict = {'Amil': 0, 'CASSI': 1, 'Hapvida': 2, 'SulAmérica': 3, 'Unimed': 4, 'Sem convênio': 5}
         insurance = self.person['Convênio']
         item_ins = self.newPatient_window.insuranceNameField.item(insurance_dict[insurance])
         self.newPatient_window.insuranceNameField.setCurrentItem(item_ins)
         
         self.newPatient_window.insurancePlanField.setText(self.person['Plano'])
         self.newPatient_window.insuranceNumberField.setText(str(self.person['Número']))
         self.newPatient_window.pushButton_Save.clicked.connect(self.modify_patient)

    def modify_patient(self):
        """Modify a patient register and update the interface."""

        self.add_new_patient()
        if self.check_fields() == True:
            try:
                self.csv_obj.edit_csvFile(self.person, self.item)

            except Exception as error:
                raise error
            
            self.close_newPatient_window()
            QMessageBox.about(self.individualInfo_window, 'Atualização de Cadastro', 'Atualização de cadastro concluída com sucesso.')
            
    
    def close_anamnesis_window(self) -> None:
        """Clear all fields from the New Patient Window and close the window."""

        self.clear_anamnesis_fields()
        self.anamnesis_window.close()

    def add_new_anamnesis(self) -> None:
        """Get the values inserted by the user for new anamnesis register."""

        self.anamnesis_window.show()
        try:
            self.date = self.anamnesis_window.dateField.text()
            self.weight = self.anamnesis_window.weightField.text()
            self.heightP = self.anamnesis_window.heightField.text()
            self.temp = self.anamnesis_window.tempField.text()
            self.blood = self.anamnesis_window.bloodField.text()
            self.complaint = self.anamnesis_window.complaintField.text()
            self.symptoms = self.anamnesis_window.symptomsField.text()
            self.family = self.anamnesis_window.familyField.text()
            self.habit = self.anamnesis_window.habitField.text()

        except Exception as error:
            raise error

    def check_fields_anamnesis(self) -> bool:
        """Check if all fields from the New anamnesis Window are filled."""

        fields = [self.date, self.weight, self.heightP, self.temp, self.blood, self.complaint, self.symptoms,
                  self.family, self.habit]
        if any(field == '' for field in fields):
            QMessageBox.about(self.anamnesis_window, 'Erro', 'Preencher todos os campos.')
            return False
        else:
            return True

    def save_newAnamnesis(self) -> None:
        """Save new anamnesis data to the database if all fields are filled."""

        self.add_new_anamnesis()
        if self.check_fields_anamnesis() == True:
            try:
                anamnesis = Anamnesis(self.date, self.heightP, self.weight, self.complaint,
                                      self.symptoms, self.temp, self.blood, self.habit, self.family)
                self.anamnesis_dict = convert_toDict(anamnesis)
                self.csv_anamnesis.fill_csvFile(self.anamnesis_dict)

            except Exception as error:
                raise error

            self.close_anamnesis_window()
            QMessageBox.about(self.patientsList_window, 'Cadastro OK', 'Cadastro de anamnese concluído com sucesso.')

    def clear_anamnesis_fields(self) -> None:
        """Clear all fields from the New anamnesis Window."""

        self.anamnesis_window.dateField.setDate(convert_toDatetime('01/01/2000'))
        self.anamnesis_window.weightField.setText('')
        self.anamnesis_window.heightField.setText('')
        self.anamnesis_window.tempField.setText('')
        self.anamnesis_window.bloodField.setText('')
        self.anamnesis_window.complaintField.setText('')
        self.anamnesis_window.symptomsField.setText('')
        self.anamnesis_window.familyField.setText('')
        self.anamnesis_window.habitField.setText('')

    def view_anamnesisData(self) -> None:
        """Display the information of an Anamnesis sheet from a selected date."""

        self.viewAnamnesis_window.show()
        self.viewAnamnesis_window.nameField.setText(self.person['Nome'])
        self.viewAnamnesis_window.dateField.setDate(convert_toDatetime(self.anamnesis_dict['date']))
        self.viewAnamnesis_window.weightField.setText(self.anamnesis_dict['weight'])
        self.viewAnamnesis_window.heightField.setText(self.anamnesis_dict['height'])
        self.viewAnamnesis_window.tempField.setText(self.anamnesis_dict['temp'])
        self.viewAnamnesis_window.bloodField.setText(self.anamnesis_dict['blood'])
        self.viewAnamnesis_window.complaintField.setText(self.anamnesis_dict['complaint'])
        self.viewAnamnesis_window.symptomsField.setText(self.anamnesis_dict['symptoms'])
        self.viewAnamnesis_window.familyField.setText(self.anamnesis_dict['family'])
        self.viewAnamnesis_window.habitField.setText(self.anamnesis_dict['habit'])
    
    def close_viewAnamnesis_window(self) -> None:
        """Close View Anamnesis Sheet window."""

        self.viewAnamnesis_window.close()

def main():
    app = QApplication(sys.argv)
    window = GUI()
    app.exec_()

if __name__ == '__main__':
    main()