import csv
import random

# ___________________________Función para leer el archivo de chat de WhatsApp Android___________________________

def leer_chat(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        chat_lines = file.readlines()
    return chat_lines


# ___________________________Función para contar las palabras dichas por cada contacto y guardar los resultados en un archivo CSV___________________________

def contar_palabras_por_contacto(chat, palabras):
    frecuencias = {}
    palabras_a_contar = palabras.split(',')

    for linea in chat:
        partes = linea.split(': ')
        contacto = partes[0].split('- ')

        if len(partes) == 2:
            nombre_contacto, mensaje = contacto[1], partes[1]

            if nombre_contacto not in frecuencias:
                frecuencias[nombre_contacto] = {}
            
            for palabra in palabras_a_contar:
                frecuencia = mensaje.lower().count(palabra.lower())
                frecuencias[nombre_contacto][palabra] = frecuencias[nombre_contacto].get(palabra, 0) + frecuencia

    archivo_destino = input("Ingrese el archivo destino para guardar el reporte: ")

    with open(archivo_destino, 'w', newline='') as csvfile:
        fieldnames = ['contacto', 'palabra', 'frecuencia']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for contacto, palabras_frecuencia in frecuencias.items():
            for palabra, frecuencia in palabras_frecuencia.items():
                writer.writerow({'contacto': contacto, 'palabra': palabra, 'frecuencia': frecuencia})
    
    print("Reporte generado!")


# ___________________________Función para generar un modelo de Markov basado en el historial de mensajes del contacto___________________________

def generar_modelo_markov(chat, contacto_seleccionado):
    modelo_markov = {}

    for linea in chat:
        partes = linea.split(': ')
        contacto = partes[0].split('- ')

        if len(partes) == 2:
            nombre_contacto, mensaje = contacto[-1], partes[1].strip()
            if nombre_contacto == contacto_seleccionado:
                palabras = mensaje.split()
                for i in range(len(palabras) - 1):
                    palabra_actual = palabras[i].lower()
                    palabra_siguiente = palabras[i + 1].lower()
                    if palabra_actual not in modelo_markov:
                        modelo_markov[palabra_actual] = []
                    modelo_markov[palabra_actual].append(palabra_siguiente)

    for lista_palabras in modelo_markov.values():
        lista_palabras.append(None)

    return modelo_markov


# ___________________________Función para generar un mensaje pseudo-aleatorio a partir de un contacto___________________________

def generar_mensaje_pseudo_aleatorio(chat, contacto):
    modelo_markov = generar_modelo_markov(chat, contacto)

    palabra_actual = random.choice(list(modelo_markov.keys()))
    mensaje = [palabra_actual.capitalize()]

    while True:
        siguiente_palabras = modelo_markov.get(palabra_actual)
        if siguiente_palabras is None:
            break
        palabra_siguiente = random.choice(siguiente_palabras)
        if palabra_siguiente is None:
            break 
        mensaje.append(palabra_siguiente)
        palabra_actual = palabra_siguiente

    return f'"{contacto}: {" ".join(mensaje)}"'


# ___________________________Función principal___________________________

def main():

    archivo_de_chat =input("Por favor, ingrese la ruta del archivo de chat de WhatsApp Android: ")
    archivo_de_chat = archivo_de_chat.strip('"')
    try:
        lineas_de_chat = leer_chat(archivo_de_chat)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo: {archivo_de_chat}")
        return
    except IOError as e:
        print(f"Error al abrir el archivo: {e}")
        return

    while True:
        print("\nMenú de opciones:")
        print("1. Contar palabras por contacto y guardar en un archivo CSV")
        print("2. Generar un mensaje pseudo-aleatorio")
        print("3. Salir")
        opcion_elegida = input("Seleccione una opción (1/2/3): ")

        if opcion_elegida == '1':
            try:
                palabras = input("Ingrese palabras a contar (separadas por comas sin utilizar espacios antes o despues de las comas): ")
                contar_palabras_por_contacto(lineas_de_chat, palabras)
            except Exception as e:
                print(f"Error al contar las palabras: {e}")

        elif opcion_elegida == '2':
            try:
                print("Contactos disponibles:")
                contactos = []
                for linea in lineas_de_chat:
                    partes = linea.split(': ')
                    contacto = partes[0].split('- ')
                    if len(partes) == 2:
                        nombre_contacto = contacto[1]
                        if nombre_contacto not in contactos:
                            contactos.append(nombre_contacto)
                for i, contacto in enumerate(contactos):
                    print(f"{i}. {contacto}")
                print(f"{len(contactos)}. Salir")
                opcion_contacto = input("Ingrese el número del contacto para generar el mensaje: ")
                if opcion_contacto.isdigit():
                    opcion_contacto = int(opcion_contacto)
                    if 0 <= opcion_contacto < len(contactos):
                        contacto_seleccionado = contactos[opcion_contacto]
                        mensaje_generado = generar_mensaje_pseudo_aleatorio(lineas_de_chat, contacto_seleccionado)
                        print(mensaje_generado)
                    elif opcion_contacto == len(contactos):
                        print("Saliendo del programa.")
                        break
                else:
                    print("Opción no válida. Ingrese un número válido.")
            except Exception as e:
                print(f"Error al generar un mensaje pseudo-aleatorio: {e}")

        elif opcion_elegida == '3':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")