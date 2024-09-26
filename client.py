import requests

def solicitudPost(codigo :str):
    url = "https://grpc-gcxm.onrender.com/sayhello"
    try:
        payload = {
            "name": codigo
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("Respuesta del servidor: ", response.json())
        else:
            print("Error en la petición:", response.status_code, response.text)
    except:
        print("Ocurrio un error al hacer la petición")

def menu():
    print("""\n1. Consultar datos
2. salir
    """)
    return int(input())

def funciones(numero):
    if(numero==1):
        codigo=input("Ingrese el codigo del estudiante: ")
        solicitudPost(codigo)
        return True
    elif(numero==2):
        return False
    else:
        print("Escriba un numero valido: ")


if __name__ == '__main__':
    estado=True
    while(estado):
        numero=menu()
        estado=funciones(numero)