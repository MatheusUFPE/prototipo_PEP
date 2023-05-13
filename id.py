from functions import *

class Id():
  """Define as variáveis essenciais que definem uma pessoa."""

  def __init__(self, name : str, birthdate : str, gender : str, cpf : str, place_of_birth : str, 
               cep : str, address_number : str, address_complement: str, phone : str, email : str):
    self.__name = name
    self.__birthdate = verify_date(birthdate)
    self.__age = calculate_age(self.__birthdate)
    self.__gender = gender
    self.__cpf = verify_cpf(cpf)['cpf']
    self.__place_of_birth = place_of_birth  
    address = verify_cep(cep)
    self.__address = get_dict_address(address)
    self.__address['complemento'] = (f'{address_number}, {address_complement}')
    self.__phone = phone
    self.__email = email
  
  
  def __str__(self):
    return f'''Name: {self.__name} \nBirthdate: {self.__birthdate} \nAge: {self.__age} \nGender: {self.__gender} \nCPF: {self.__cpf}
    \nPlace of Birth: {self.__place_of_birth} \nAddress: {self.__address['logradouro']}, {self.__address['complemento']} - 
    {self.__address['bairro']} - {self.__address['localidade']}/{self.__address['uf']} \nCEP : {self.__address['cep']} 
    \nPhone: {self.__phone}; \nEmail: {self.__email}'''
  
  def get_name(self):   
    return self.__name

  def get_birthdate(self):   
    return self.__birthdate

  def get_age(self):   
    return self.__age

  def get_gender(self):   
    return self.__gender

  def get_cpf(self):   
    return self.__cpf
  
  def get_place_of_birth(self):  
    return self.__place_of_birth
  
  def get_address(self):   
    return self.__address

  def get_phone(self):  
    return self.__phone

  def get_email(self):
    return self.__email