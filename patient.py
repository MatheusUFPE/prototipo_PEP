from id import Id

class Patient(Id):
  """Definem parâmteros relacionados a um paciente."""

  def __init__(self, id_obj : Id, insuranceName : str, insurancePlan : str, insuranceNumber : str) -> None:
    
    super().__init__(id_obj.get_name(), id_obj.get_birthdate(), id_obj.get_gender(), id_obj.get_cpf(), id_obj.get_place_of_birth(), 
                     id_obj.get_address()['cep'], id_obj.get_address()['complemento'].split(',')[0], 
                     id_obj.get_address()['complemento'].split(',')[1],id_obj.get_phone(), id_obj.get_email())
    self.__allergy = None
    self.__insuranceName = insuranceName
    self.__insurancePlan = insurancePlan
    self.__insuranceNumber = insuranceNumber

  def __str__(self):
    return str(super().__str__()) + '\n\nPatient information: \nAllergies: {} \nInsuranceName: {} \nInsurancePlan: {} \nInsuranceNumber: {}'.format(
              self.__allergy, self.__insuranceName, self.__insurancePlan, self.__insuranceNumber)
  
  def get_allergy(self) -> str:
    return self.__allergy
  
  def add_allergy(self, allergy) -> None:
    self.__allergy.append(allergy.upper())
  
  def remove_allergy(self, allergy) -> None:
    self.__allergy.discard(allergy.upper())
  
  def get_insuranceName(self) -> str:
    return self.__insuranceName

  def get_insurancePlan(self) -> str:
    return self.__insurancePlan

  def get_insuranceNumber(self) -> str:
    return self.__insuranceNumber