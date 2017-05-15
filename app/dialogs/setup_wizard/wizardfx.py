def get_missing_imports():
    missing_imports = []
    imports = open("import_list.txt").readlines()

    for name in imports:
        try:
            exec ("import " + name)
        except ImportError:
            missing_imports.append(name)

    return missing_imports