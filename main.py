from infrastructure.ui.main_app import main as ui_main

def main():
    # Delegamos al punto de entrada de la capa de infraestructura (UI)
    return ui_main()


if __name__ == '__main__':
    main()