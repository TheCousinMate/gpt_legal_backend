import os

<<<<<<< HEAD

def pack_selective_project_for_review(
    project_root, include_paths, output_filename="project_bundle_selective.txt"
):
=======
def pack_selective_project_for_review(project_root, include_paths, output_filename="project_bundle_selective.txt"):
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96
    """
    Packs specified files and directories into a single output file,
    excluding common large/sensitive directories and files.

    project_root: The root directory of your project.
    include_paths: A list of file or directory paths (relative to project_root) to include.
    output_filename: The name of the output text file.
    """
    excluded_dirs = ["node_modules", ".git", "__pycache__"]
<<<<<<< HEAD
    excluded_files = [
        output_filename,
        ".env",
        ".gitignore",
        "pack_project.py",
        "project_bundle.txt",
    ]
=======
    excluded_files = [output_filename, ".env", ".gitignore", "pack_project.py", "project_bundle.txt"]
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96

    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write(f"--- INICIO DEL BUNDLE DEL PROYECTO (SELECTIVO) ---\n\n")
        outfile.write(f"Raíz del proyecto: {os.path.basename(project_root)}\n\n")

        for path_to_include in include_paths:
            full_path = os.path.join(project_root, path_to_include)

            if not os.path.exists(full_path):
<<<<<<< HEAD
                outfile.write(
                    f"\n--- ADVERTENCIA: Ruta no encontrada: {path_to_include} ---\n"
                )
=======
                outfile.write(f"\n--- ADVERTENCIA: Ruta no encontrada: {path_to_include} ---\n")
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96
                continue

            # If it's a single file
            if os.path.isfile(full_path):
                file_name = os.path.basename(full_path)
                if file_name in excluded_files:
<<<<<<< HEAD
                    continue  # Skip excluded files
=======
                    continue # Skip excluded files
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96

                try:
                    with open(full_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                    outfile.write(f"\n--- Archivo: {path_to_include} ---\n")
                    outfile.write(content)
<<<<<<< HEAD
                    outfile.write("\n")  # Add newline for separation
                except UnicodeDecodeError:
                    outfile.write(
                        f"\n--- Archivo (IGNORADO - posible binario): {path_to_include} ---\n"
                    )
                except Exception as e:
                    outfile.write(
                        f"\n--- ERROR al leer archivo {path_to_include}: {e} ---\n"
                    )
=======
                    outfile.write("\n") # Add newline for separation
                except UnicodeDecodeError:
                    outfile.write(f"\n--- Archivo (IGNORADO - posible binario): {path_to_include} ---\n")
                except Exception as e:
                    outfile.write(f"\n--- ERROR al leer archivo {path_to_include}: {e} ---\n")
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96

            # If it's a directory, walk through it
            elif os.path.isdir(full_path):
                for root, dirs, files in os.walk(full_path):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if d not in excluded_dirs]

                    relative_root = os.path.relpath(root, project_root)

                    # Add a directory header if it's not the top-level included path or if it has files
<<<<<<< HEAD
                    if files or (
                        relative_root != path_to_include and relative_root != "."
                    ):
=======
                    if files or (relative_root != path_to_include and relative_root != "."):
>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96
                        outfile.write(f"\n--- Directorio: {relative_root} ---\n")

                    for file_name in files:
                        if file_name in excluded_files:
<<<<<<< HEAD
                            continue  # Skip excluded files

                        file_path = os.path.join(root, file_name)
                        # Attempt to read common text files, skip known binary types
                        if not (
                            file_name.lower().endswith(
                                (
                                    ".png",
                                    ".jpg",
                                    ".jpeg",
                                    ".gif",
                                    ".zip",
                                    ".tar.gz",
                                    ".log",
                                    ".ico",
                                    ".svg",
                                )
                            )
                            or os.path.islink(file_path)
                        ):
                            try:
                                with open(file_path, "r", encoding="utf-8") as infile:
                                    content = infile.read()
                                outfile.write(
                                    f"\n--- Archivo: {os.path.join(relative_root, file_name)} ---\n"
                                )
                                outfile.write(content)
                                outfile.write("\n")
                            except UnicodeDecodeError:
                                outfile.write(
                                    f"\n--- Archivo (IGNORADO - posible binario): {os.path.join(relative_root, file_name)} ---\n"
                                )
                            except Exception as e:
                                outfile.write(
                                    f"\n--- ERROR al leer archivo {os.path.join(relative_root, file_name)}: {e} ---\n"
                                )
        outfile.write(f"\n--- FIN DEL BUNDLE DEL PROYECTO (SELECTIVO) ---\n")
    print(f"Proyecto empaquetado selectivamente en '{output_filename}'")


=======
                            continue # Skip excluded files

                        file_path = os.path.join(root, file_name)
                        # Attempt to read common text files, skip known binary types
                        if not (file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar.gz', '.log', '.ico', '.svg')) or os.path.islink(file_path)):
                            try:
                                with open(file_path, "r", encoding="utf-8") as infile:
                                    content = infile.read()
                                outfile.write(f"\n--- Archivo: {os.path.join(relative_root, file_name)} ---\n")
                                outfile.write(content)
                                outfile.write("\n")
                            except UnicodeDecodeError:
                                outfile.write(f"\n--- Archivo (IGNORADO - posible binario): {os.path.join(relative_root, file_name)} ---\n")
                            except Exception as e:
                                outfile.write(f"\n--- ERROR al leer archivo {os.path.join(relative_root, file_name)}: {e} ---\n")
        outfile.write(f"\n--- FIN DEL BUNDLE DEL PROYECTO (SELECTIVO) ---\n")
    print(f"Proyecto empaquetado selectivamente en '{output_filename}'")

>>>>>>> 03c2c84b047c243bcbdeac10025a8f13ee62ef96
if __name__ == "__main__":
    # <<<<<<<<<<<<<<<<<<<<<<<< MODIFICA ESTA LISTA >>>>>>>>>>>>>>>>>>>>>>>>>>
    # Añade aquí los nombres de los archivos y carpetas que quieres que yo revise.
    # Ejemplos:
    # - "server.js" (tu archivo principal del servidor)
    # - "package.json" (para ver las dependencias)
    # - "models" (si tus modelos están en una carpeta llamada 'models')
    # - "routes" (si tienes una carpeta 'routes' para tus rutas)
    # - "controllers" (si tienes una carpeta 'controllers')
    # - "utils" (si tienes una carpeta 'utils')
    # - etc.
    #
    # Si tu modelo está en un archivo específico, por ejemplo, "models/UserModel.js", inclúyelo.
    # Si tienes más de un modelo, añade todos los archivos de modelo relevantes.
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    essential_paths_for_review = [
        "server.js",
        "package.json",
        # EJEMPLO: Si tienes una carpeta 'models', descomenta la siguiente línea:
        # "models",
        # EJEMPLO: Si tienes un archivo de modelo específico como 'User.js' en la raíz o en 'models/User.js':
        # "models/User.js",
        # EJEMPLO: Si tus rutas están en una carpeta 'routes':
        # "routes",
        # ... añade más rutas y archivos según sea necesario para tu revisión ...
    ]

    pack_selective_project_for_review(os.getcwd(), essential_paths_for_review)
