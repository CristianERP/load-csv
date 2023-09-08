import pandas as pd


CYTIES = {"1": "Bucaramanga", "2": "Giron", "3": "Florida", "4": "Piedecuesta"}
CYTIES_KEYS = list(CYTIES.keys())
SEXO = ["F", "M", "f", "m"]
HEADERS = ["codigo", "sexo", "nombre", "edad", "ciudad"]

datos = False


def menu():
    while True:
        print("*" * 32)
        print("Menu Principal")
        print("Cristian Rojas")
        print("*" * 32)
        print("a. Cargar Datos")
        print("b. Informe Especial")
        print("c. Operaciones")
        print("d. Salir")
        print("*" * 32)

        opcion = input("Seleccione una opción: ")

        if opcion == "a":
            cargar_datos()
        elif opcion == "b":
            informe_especial()
        elif opcion == "c":
            submenu()
        elif opcion == "d":
            guardar_datos()
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def cargar_datos():
    global datos
    nombre_archivo = input("Ingrese el nombre del archivo CSV: ")
    try:
        datos = pd.read_csv(
            nombre_archivo,
            header=None,
            names=HEADERS,
        )
        print(datos)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")

    input("\nPresione Enter para continuar...")


def informe_especial():
    if datos is False:
        print("No existe archivo cargado.")
        input("\nPresione Enter para continuar...")
        return

    datos_mostrados = datos.copy()
    datos_mostrados["sexo"] = datos_mostrados["sexo"].apply(
        lambda x: "Femenino" if x in ["F", "f"] else "Masculino"
    )
    datos_mostrados["ciudad"] = datos_mostrados["ciudad"].astype(str)
    datos_mostrados["ciudad"] = datos_mostrados["ciudad"].map(CYTIES)

    print("\nDatos:")
    print(datos_mostrados)

    agg_ciudad = datos_mostrados.groupby("ciudad").size()
    total_registros = len(datos_mostrados)
    porcentajes = (agg_ciudad / total_registros) * 100

    print("\nTotales por Ciudad:")
    for ciudad, total, porcentaje in zip(agg_ciudad.index, agg_ciudad, porcentajes):
        print(f"{ciudad}: {total} participantes ({porcentaje:.2f}%)")

    grupos = datos_mostrados.copy()
    grupos["edad"] = grupos["edad"].astype(int)

    def definir_grupo(edad):
        if edad <= 5:
            return "Grupo 1"
        elif 5 < edad <= 10:
            return "Grupo 2"
        else:
            return "Grupo 3"

    grupos["grupo_edad"] = grupos["edad"].apply(definir_grupo)

    print("\nGrupo según Edad:")
    grupos_edad = grupos.groupby("grupo_edad").size()
    print(grupos_edad)

    input("\nPresione Enter para continuar...")


def guardar_datos():
    if datos is False:
        print("No hay datos cargados.")
        return

    resp = input("¿Desea guardar los cambios? (SI [S] o NO [N]): ").upper()
    if resp != "S":
        return

    nombre_archivo = input("Ingrese el nombre del archivo CSV para guardar: ")
    datos.to_csv(nombre_archivo, index=False)
    print(f"Datos guardados en '{nombre_archivo}'")


def submenu():
    if datos is False:
        print("No existe archivo cargado.")
        input("\nPresione Enter para continuar...")
        return

    while True:
        print("*" * 32)
        print("Submenú")
        print("*" * 32)
        print("a. Agregar")
        print("b. Editar")
        print("c. Borrar")
        print("d. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "a":
            agregar()
        elif opcion == "b":
            editar()
        elif opcion == "c":
            borrar()
        elif opcion == "d":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def agregar():
    global datos

    codigo = input("Ingrese el código: ")
    sexo = input("Ingrese el sexo (F/M): ")
    while sexo not in SEXO:
        print("Error: El sexo debe ser 'F' o 'M'.")
        sexo = input("Ingrese el sexo (F/M): ")
    nombre = input("Ingrese el nombre: ")
    edad = input("Ingrese la edad: ")
    ciudad = input(
        "Ingrese la ciudad (1: Bucaramanga, 2: Giron, 3: Florida, 4: Piedecuesta): "
    )
    while ciudad not in CYTIES_KEYS:
        print("Error: La ciudad debe ser un número del 1 al 4.")
        ciudad = input(
            "Ingrese la ciudad (1: Bucaramanga, 2: Giron, 3: Florida, 4: Piedecuesta): "
        )

    nuevo_registro = {
        "codigo": codigo,
        "sexo": sexo.upper(),
        "nombre": nombre.upper(),
        "edad": edad,
        "ciudad": int(ciudad),
    }

    datos = pd.concat([datos, pd.DataFrame([nuevo_registro])], ignore_index=True)
    print("Registro agregado con éxito.")
    return


def editar():
    global datos
    datos["codigo"] = datos["codigo"].astype(int)
    codigo = input("Ingrese el código a editar: ")
    codigo = int(codigo)
    if datos["codigo"].isin([codigo]).any() == False:
        print(f"No existe el código {codigo}.")
        return

    columna = input(
        "Ingrese la columna a editar (codigo, sexo, nombre, edad, ciudad): "
    )
    while columna not in HEADERS:
        columna = input(
            "Ingrese la columna a editar (codigo, sexo, nombre, edad, ciudad): "
        )
    if columna == "sexo":
        nuevo_valor = input(f"Ingrese el nuevo valor para {columna} (F/M): ")
        while nuevo_valor not in SEXO:
            print("Error: El sexo debe ser 'F' o 'M'.")
            nuevo_valor = input(f"Ingrese el nuevo valor para {columna} (F/M): ")

        nuevo_valor = nuevo_valor.upper()
    elif columna == "ciudad":
        nuevo_valor = input(
            f"Ingrese el nuevo valor para {columna} (1: Bucaramanga, 2: Giron, 3: Florida, 4: Piedecuesta): "
        )
        while nuevo_valor not in CYTIES_KEYS:
            print("Error: La ciudad debe ser un número del 1 al 4.")
            nuevo_valor = input(
                f"Ingrese el nuevo valor para {columna} (1: Bucaramanga, 2: Giron, 3: Florida, 4: Piedecuesta): "
            )
        nuevo_valor = int(nuevo_valor)
    else:
        nuevo_valor = input(f"Ingrese el nuevo valor para {columna}: ")

    if columna == "nombre":
        nuevo_valor = nuevo_valor.upper()

    if columna == "edad":
        nuevo_valor = int(nuevo_valor)

    datos.loc[datos["codigo"] == codigo, columna] = nuevo_valor

    print("Registro editado con éxito.")
    return


def borrar():
    global datos
    codigo = input("Ingrese el código del registro a borrar: ")
    codigo = int(codigo)

    if datos["codigo"].isin([codigo]).any():
        datos = datos[datos["codigo"] != codigo]
        print(f"Registro con código {codigo} eliminado.")
    else:
        print(f"No se encontró ningún registro con código {codigo}.")

    return


if __name__ == "__main__":
    menu()
