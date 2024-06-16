import requests
from bs4 import BeautifulSoup
import random
import string
from rut_chile import rut_chile
import time

def generate_rut():
    def calculate_verifier_digit(rut):
        reverse_digits = map(int, reversed(str(rut)))
        factors = [2, 3, 4, 5, 6, 7] * 2  # Multiplicadores
        s = sum(d * f for d, f in zip(reverse_digits, factors))
        mod11 = 11 - (s % 11)
        if mod11 == 11:
            return '0'
        elif mod11 == 10:
            return 'K'
        else:
            return str(mod11)
    
    number = random.randint(4000000, 24999999)
    verifier = calculate_verifier_digit(number)
    if number < 10000000:
        return f"{number}-{verifier}"
    else:
        formatted_number = f"{str(number)[:2]}.{str(number)[2:5]}.{str(number)[5:]}"
        return f"{formatted_number}-{verifier}"

def generate_password(length=10):
    if length < 10:
        raise ValueError("La longitud mínima de la contraseña debe ser 10")

    uppercase_letters = string.ascii_uppercase.replace('Ñ', '')
    lowercase_letters = string.ascii_lowercase.replace('ñ', '')
    digits = string.digits
    special_characters = "~!@#$^*-_=[]{}|;,.?"

    words = [
        "Maria", "Juan", "Pedro", "Ana", "Luis", "Carmen", "Jose", "Lucia", "Carlos", "Laura",
        "Miguel", "Marta", "Francisco", "Sofia", "David", "Paula", "Javier", "Elena", "Antonio", 
        "Marcos", "Isabel", "Daniel", "Sara", "Fernando", "Clara", "Roberto", "Raquel", "Alberto", 
        "Pablo", "Cristina", "Sergio", "Sandra", "Rafael", "Beatriz", "Eduardo", "Monica", "Jorge", 
        "Nuria", "Ricardo", "Patricia", "Adrian", "Rosa", "Enrique", "Gloria", "Victor", "Irene"
    ]

    # Determinar si la contraseña incluirá una palabra de la lista
    include_word = random.choice([True, False])
    
    password = []

    if include_word:
        word = random.choice(words)
        password.append(word)
        remaining_length = length - len(word)
    else:
        remaining_length = length

    # Garantizar que la contraseña cumpla con los requisitos mínimos
    password.extend([
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_characters)
    ])

    # Rellenar el resto de la contraseña con caracteres aleatorios
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters
    password += [random.choice(all_characters) for _ in range(remaining_length - len(password))]

    if not include_word:
        random.shuffle(password)

    return ''.join(password)
    

def generate_random_number():
    return str(random.randint(10, 99))
def main():
    # URL inicial
    initial_url = 'https://r.medsoluciones.cl/r/Rk4lskS'

    # Encabezados
    headers = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/126.0 Firefox/126.0'}

    # Crear una sesión para mantener las cookies
    session = requests.Session()

    # Realizar la solicitud GET inicial
    response = session.get(initial_url, headers=headers, allow_redirects=True)
    print(response.url)
    # Realizar la segunda solicitud GET
    response2 = session.get(response.url, headers=headers, allow_redirects=True)

    # URL de la solicitud POST para iniciar sesión
    post_url = 'https://personas.medsoluciones.cl/personas/inicioSesion.asp'

    # Generar un RUT y una clave aleatoria
    rut = rut_chile.format_rut_with_dots(generate_rut())
    clave = generate_password()
    print(rut, clave)

    # Datos del formulario para la solicitud POST de inicio de sesión
    data = {
        'rut': rut,
        'clave': clave
    }

    post_response = session.post(post_url, data=data, headers=headers)

    # Crear el objeto BeautifulSoup con el contenido de la respuesta POST
    soup = BeautifulSoup(post_response.content, 'html.parser')

    # Buscar todos los elementos input en el formulario
    inputs_first = soup.find_all('input')

    # Crear un diccionario para los datos del formulario final
    final_data = {}

    for input_tag in inputs_first:
        name = input_tag.get('name')
        if name:
            final_data[name] = generate_random_number()  # Generar valores de dos dígitos aleatorios

    first_superclave_post = 'https://personas.medsoluciones.cl/transa/segmentos/Menu/bloqueoTemporal.asp/revision'
    first_superclave_response = session.post(first_superclave_post, data=final_data, headers=headers)

    soup2 = BeautifulSoup(first_superclave_response.content, 'html.parser')
    inputs_second = soup2.find_all('input')
    final_data2 = {}

    for input_tag in inputs_second:
        name = input_tag.get('name')
        if name:
            final_data2[name] = generate_random_number()

    second_superclave_post = 'https://personas.medsoluciones.cl/transa/segmentos/Menu/bloqueoTemporal.asp/error/revision'

    final_post_response = session.post(second_superclave_post, data=final_data2, headers=headers)

    final_soup = BeautifulSoup(final_post_response.content, 'html.parser')
    alert_div = final_soup.find('div', {'class': 'col-sm-8 text-center alert alert-success my-5'})
    if alert_div:
        success_message = alert_div.get_text(strip=True)
        print(success_message)
    else:
        print("Mensaje de éxito no encontrado.")

while True:
    main()
    time.sleep(5)