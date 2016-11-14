# automagica

Automágica permite maquetear en forma automática libros listos para imprimir en una imprenta o para distrubuir digitalmente.

Funciona en Linux, OS X y Windows.

[![Estado actual de Automágica](https://img.youtube.com/vi/BtyG786BUmo/0.jpg)](https://www.youtube.com/watch?v=BtyG786BUmo)

# Instalación

## Requerimientos

* pdflatex
* python 2
* pandoc
* pdfrw

## En Linux

* apt-get install pandoc, texlive-full
* pip install pdfwr

## En Windows

* http://mirror.ctan.org/systems/texlive/tlnet/install-tl-windows.exe (para tener pdflatex.exe)
* https://github.com/jgm/pandoc/releases/download/1.17.2/pandoc-1.17.2-windows.msi
* https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi
* Agregar Python al PATH del sistema:
  - Apretar las teclas Win y Pause.
  - Click en Advanced System Settings.
  - Click en Environment Variables.
  - Agregar ;C:\python27 a la variable PATH.
  - Reiniciar cmd.
* Para instalar pdfrw abrir cmd para entrar a la línea de comandos y ejecutar:
  - C:\Python27\Scripts\pip.exe install pdfrw
* Bajar el .zip de automágica desde esta misma página.

# Uso

`python automagica.py ejemplo` genera la versión en pdf del libro en la caprpeta ejemplo.


`python automagica.py --pdf --bookle --epub ejemplo` genera la versión en pdf, pdf booklet y epub del libro en la caprpeta ejemplo.
