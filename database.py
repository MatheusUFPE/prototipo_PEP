import sqlite3

def connection():
    try:
        # Conexão ao banco de dados
        connection = sqlite3.connect("patients.db")
        return connection
    except:
        print('Error connecting to the database')

def create_table():
    try:
        
        # Conexão ao banco de dados e criação de um cursor
        connection = connection()
        cursor = connection.cursor()

        # Script para criar tabela
        sql = '''
                CREATE TABLE IF NOT EXISTS patients(
                    name TEXT,
                    birthdate TEXT,
                    age INTEGER,
                    gender TEXT,
                    cpf TEXT PRIMARY KEY,
                    place_of_birth TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT

                )'''

        cursor.execute(sql)

        # Efetivar a criação da tabela
        connection.commit()

        print('Table successfully created.')

    except:
        print('Error connecting to the database when creating the table')

    finally:
        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()

def read_all():
    """Read all data from the database."""

    try:
        # Script to read the data
        sql = '''SELECT * FROM patients'''

        connection = connection()
        cursor = connection.cursor()
        cursor.execute(sql)

        allPatients = cursor.fetchall()
        return allPatients

    except:
        print('Error connecting to the database when reading the data')

    finally:
        cursor.close()
        connection.close()

def insert(patient : dict):
    """Insert a new patient to the database."""

    existe_na_tabela = read_all(patient) ###OLHAR AMANHA
    if existe_na_tabela != None:
        return 'Patient already registered.'
    
    # Conexão ao banco de dados e criação de um cursor
    connection = connection()
    cursor = connection.cursor()
        
    # Executar um comando SQL para inserir os dados do paciente na tabela
    sql = """INSERT INTO patients (
            name, birthdate, age, gender, cpf, place_of_birth, address, phone, email, 
            insurance_name, insurance_plan, insurance_number) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
    values = []
    for value in patient.values():
        values.append(value)
    cursor.execute(sql, values)
    connection.commit()
    connection.close()
        
    print("Patient data sent to database.")