"""Arranque de la instancia pública con los datos de demostración optativos."""

import os
import subprocess
import sys


def manage(*args):
    subprocess.run([sys.executable, 'manage.py', *args], check=True)


def main():
    manage('migrate', '--noinput')
    manage('configurar_grupos')
    manage('collectstatic', '--noinput')
    if os.environ.get('CARGAR_CATALOGO_DEMO') == '1':
        manage('cargar_catalogo_demo')

    puerto = os.environ.get('PORT', '8000')
    os.execvp('gunicorn', [
        'gunicorn', 'config.wsgi:application', '--bind', f'0.0.0.0:{puerto}',
        '--workers', '1', '--threads', '4', '--access-logfile', '-',
    ])


if __name__ == '__main__':
    main()
