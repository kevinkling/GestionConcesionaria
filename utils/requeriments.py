import subprocess
import sys

class InstalarRequerimientos :
    
    def __init__(self) :
        # Lista de paquetes a verificar e instalar
        self.packages = ['tkcalendar']
        self.install_packages()
        
    def check_install(self, package):
        """ Verifica si un paquete está instalado. """
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'show', package])
        except subprocess.CalledProcessError:
            return False
        return True

    def install_packages(self):
        """Instala los paquetes que no están instalados."""
        for package in self.packages:
            if not self.check_install(package):
                print(f'Instalando {package}...')
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


