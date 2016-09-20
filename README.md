# automagica

Permite crear en forma fácil libros listos para la imprenta o para distribuir digitalmente.

Funciona en Linux, OS X y Windows.

# Requerimientos

* pdflatex
* python 2
* pandoc
* pdfrw

# En Windows

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
