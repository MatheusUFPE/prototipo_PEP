from functions import *

class Anamnesis():
    """Define parâmetros para se entender a situação do paciente."""

    def __init__(self, date: str, height: float, weight: float, complaint: list, symptom: list, temperature: float,
                 bloodPressure: str, habit: list, family: str):
        
        # complaint = queixa; historic = histórico de doenças; habit = alcoolismo, tabagismo, etc; family = histórico familiar.
        self.__date = verify_date(date)
        self.__height = height
        self.__weight = weight
        self.__complaint = complaint
        self.__symptom = symptom
        self.__temperature = temperature
        self.__bloodPressure = bloodPressure
        self.__habit = habit
        self.__family = family

    def get_date(self):  # Retorna o dia
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_height(self):  # Retorna o valor da altura
        return self.__height

    def set_height(self, height):  # Altera o valor da altura atual
        self.__height = height

    def get_weight(self):  # Retorna o valor do peso
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight  # Altera o peso atual do paciente

    def get_complaint(self):  # Retorna a queixa
        return self.__complaint

    def add_complaint(self, complaint):  # Adiciona uma nova queixa
        self.__complaint.append(complaint)

    def get_symptom(self):  # Retorna o sintoma
        return self.__symptom

    def add_symptom(self, symptom):  # Adiciona um novo sintoma
        self.__symptom.append(symptom)

    def get_temperature(self):  # Retorna a temperatura
        return self.__temperature

    def set_temperature(self, temperature):  # Altera o valor da temperatura
        self.__temperature = temperature

    def get_bloodPressure(self):  # Retorna a pressão sanguínea
        return self.__bloodPressure

    def set_bloodPressure(self, bloodPressure):  # Altera o valor da pressão sanguínea
        self.__bloodPressure = bloodPressure

    def get_habit(self):  # Retorna o histórico de hábitos prejudiciais à saúde
        return self.__habit

    def set_habit(self, habit):  # Adiciona um novo hábito ao histórico
        self.__habit.append(habit)

    def get_family(self):  # Retorna o histórico familiar
        return self.__family

    def get_exams(self):  # Retorna os exames relaizados
        return self.__habit
