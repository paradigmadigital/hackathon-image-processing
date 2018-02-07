# IoT OpenCV

## Instalación

Para empezar a trabajar con la librería OpenCV para Python, recomendamos seguir estos pasos. Daremos por hecho
que todos tienen Python instalado en el equipo.

### Linux Opción 1

    sudo apt-get -y install build-essential cmake pkg-config git
    sudo apt-get -y install libffi-dev libffi6
    sudo apt-get -y install libjpeg-dev libpng-dev
    sudo apt-get -y install libsm6 libxrender1 libfontconfig1
    sudo apt-get -y install python-dev python-tk python-setuptools python-virtualenv
    sudo easy_install pip

Crearemos un entorno virtual para instalar las librerías en la carpeta de este repositorio

    virtualenv venv

Activamos el entorno virtual e instalamos las dependencias para empezar a trabajar

    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

Los `requirements.txt` intentarán instalar la versión `opencv-python==3.4.0.12`. Si no funciona, mira los pasos para descargar el código y compilarlo en la sección de raspberry de este manual.

Listado de errores comunes tras la instalación:

* En Ubuntu con KDE instalar desde pip la librería opencv-python no funciona
* No instalar desde aptitude libopencv-dev python-opencv porque instala la versión 2.4 y algunos ejemplos no funcionarán o se comportarán del mismo modo
* [moveToThread](https://stackoverflow.com/questions/46449850/how-to-fix-the-error-qobjectmovetothread-in-opencv-in-python)

#### Linux/Windows Opción 2.

*ATENCIÓN! con una máquina virtual no se mostrarán las imagenes ya que no hay un entorno gráfico para renderizarlo*

Tendremos que tener instalados [VirtualBox](https://www.virtualbox.org/) y
[Vagrant](https://www.vagrantup.com/downloads.html)

Desde una consola poner desde la carpeta de este repositorio

    vagrant up
    vagrant ssh

    cd /vagrant/
    virtualenv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

### Raspberry Pi devices

  - (system update) `sudo apt-get update`
  - (system update) `sudo apt-get upgrade`

  - `sudo apt-get install build-essential cmake pkg-config`
  - `sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev`
  - `sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`
  - `sudo apt-get install libxvidcore-dev libx264-dev`
  - `sudo apt-get install libgtk2.0-dev`
  - `sudo apt-get install libatlas-base-dev gfortran`
  - `sudo apt-get install python2.7-dev python3-dev`

  - `cd ~`
  - `wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip`
  - `unzip opencv.zip`
  - `wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip`
  - `unzip opencv_contrib.zip`

  - (pip installation) `wget https://bootstrap.pypa.io/get-pip.py`
  - (pip installation) `sudo python get-pip.py`

  - `pip install numpy`

  - `cd ~/opencv-3.4.0/`
  - `mkdir build`
  - `cd build`
  - `cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
    -D BUILD_EXAMPLES=ON ..`
  - `make -j4` or `make`
  - `sudo make install`
  - `sudo ldconfig`

  - `ls -l /usr/local/lib/python3.4/dist-packages/`
  - `cd /usr/local/lib/python3.4/site-packages/`
  - `sudo mv cv2.cpython-34m.so cv2.so`
  - `ln -s /usr/local/lib/python3.4/site-packages/cv2.so cv2.so`

To test this installation:

  - `$ python3`
  - `>>> import cv2`
  - `>>> cv2.__version__`
  - `'3.4.0'`
  - `>>>`



## Ejecutar comandos

Como consola para ejecutar el código, podemos elegir trabajar desde ipython tecleando en la consola

    ipython

o con un notebook desde

    jupyter notebook --ip=0.0.0.0

En el navegador http://localhost:8888/notebooks/Ejemplos_basicos.ipynb
