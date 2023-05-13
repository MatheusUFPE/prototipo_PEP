from datetime import datetime
import re
import requests
import pandas as pd
import os
import chardet


def convert_toDatetime(date : str):
  """Convert a date in the string format to a datetime format."""

  date = re.sub('[^0-9]', '', date)  #Retirar todos os caracteres não numéricos
  date = datetime.strptime(date, '%d%m%Y')   #Conversão da data em tipo datetime a fim de facilitar a manipulação
  return date

def verify_date(date : str):
  """Verify if the date is between 1900 and 2023."""

  try:
    date = convert_toDatetime(date)
    day = date.day
    month = date.month
    year = date.year
    assert (year >= 1900 or year <= 2023) #Verificação para que o ano esteja entre 1900 e 2023

  except AssertionError:
    print('Digite o ano de nascimento entre 1900 e 2023: ')

  return f'{day}/{month}/{year}'

def verify_cep(cep : str):
  """Verify if a CEP code exists. If it does, return a dictionary with the address information 
  related to the CEP code. If not, return a dictionary {'erro': True}"""

  cep = re.sub('[^0-9]', '', cep)
  dict_request = {}
  if len(cep) == 8:
      link = f'https://viacep.com.br/ws/{cep}/json/'
      request = requests.get(link)
      dict_request = request.json()
      if 'erro' in dict_request.keys():
         print("CEP not found.")
      else:
        dict_request['erro'] = False
        dict_request['invalido'] = False
  else:
      dict_request['invalido'] = True
      print("CEP is not valid")
  return dict_request
               
def verify_cpf(cpf : str) -> dict:
  """Verify if a CPF is valid."""

  cpf = re.sub('[^0-9]', '', cpf)
  digits_ver = cpf[-2:]
  digits = cpf[:-2]
  s1 = 0
  s2 = 0
    
  # Verify the first digit
  for cont, d in enumerate(digits):
      s1 += (int(d)*(10-cont))
  if (s1 % 11) in [0,1]:
      digits += '0'
  else:
      digits += '{}'.format(11-(s1 % 11))
    
  # Verify the second digit
  for cont, d in enumerate(digits):
      s2 += (int(d)*(11-cont))
  if (s2 % 11) in [0,1]:
      digits += '0'
  else:
      digits += '{}'.format(11-(s2 % 11))
    
  #Compare both digits generated to the original cpf last digits
  if int(digits[-2:]) == int(digits_ver):
      print(f'{cpf} - CPF is valid!')
      error = False
  else:
      print(f'{cpf} - CPF is not valid!')
      error = True

  dict_cpf = {'cpf': cpf,'error': error}

  return dict_cpf

def get_dict_address(address : dict) -> dict:
   """Get only the fields of interest to an address: "CEP, logradouro, complemento, bairro, localidade, uf". """

   dict_address = {key: address[key] for key in ['cep','logradouro','complemento','bairro','localidade','uf']}
   return dict_address

def calculate_age(birthdate : str):
    """Calculate the current age given a birthdate."""
    
    birthdate = convert_toDatetime(birthdate)
    year = birthdate.year
    today = datetime.now()
    age = today.year - year - ((today.month, today.day) < (birthdate.month, birthdate.day)) 
    return age

def imc(weight : float, height : float): 
  """Calculate the imc through weight and height and return a string containing the value of imc 
     and the degree (underweight, ideal weight, overweight and obese)."""
     
  imc = round(weight/(height**2),1)

  if imc <= 18.5:
    return f'{imc} - Abaixo do peso'
  elif imc >= 18.6 and imc <= 24.9:
    return f'{imc} - peso ideal'
  elif imc >= 25 and imc <= 29.9:
    return f'{imc} - Sobrepeso'
  elif imc >= 30 and imc <= 34.9:
    return f'{imc} - Obesidade Grau I'
  elif imc >= 35 and imc <= 39.9:
    return f'{imc} - Obesidade Grau II (Severa)'
  elif imc >= 40:
    return f'{imc} - Obesidade Grau III (Mórbida)'
  
def convert_toDict(instance : object ) -> dict:
   "Return the attributes of an object Id as a dict."

   instance_dict = vars(instance)
   new_dict = {}
   for key,value in instance_dict.items():
     new_key = key.replace(f"_Id__","").replace(f"_Patient__","").replace(f"_Anamnesis__","")
     new_dict[new_key] = value
   return new_dict

def csv_writer(d : dict, filename : str):  #Atualização de planilha
    
    #path = f'/home/nayara/Documentos/Técnicas_projeto_final/{name}'
    path = f'C:/Users/User/Documents/Tecnicas computacionais/PEP/{filename}'
    if os.path.exists(path) == False:
        dataframe = pd.DataFrame({},columns=list(d.keys()))
        dataframe.to_csv(filename)

    with open(path, 'rb') as f:
      result = chardet.detect(f.read())

    dataframe = pd.read_csv(path, encoding=result['encoding'])

    # Adicionar as linhas ao dataframe
    new_lines= pd.DataFrame(data=d, index=[0],columns=list(dataframe.columns))
    dataframe = pd.concat([dataframe, new_lines], axis=0, ignore_index=True)

    # Salvar o dataframe de volta no arquivo CSV
    dataframe.to_csv(path, index=False)