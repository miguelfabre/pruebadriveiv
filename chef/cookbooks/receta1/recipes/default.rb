# Actualizamos los repositorios 
execute "apt-get-update" do
  command "apt-get update"
end

# Instalación de debootstrap
execute "install debootstrap" do
  command "apt-get install debootstrap"
end

#Creación de una nueva distro
execute "create new distro" do
  command "debootstrap --arch=i386 saucy /home/jaulas/saucy32/ http://archive.ubuntu.com/ubuntu"
end

# Instalamos python 
execute "install python" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install python -y"
end

# Instalamos una serie de herramientas necesarias
execute "install python3-setuptools" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install python3-setuptools -y"
end

execute "easy_install3 pip" do
	command "easy_install3 pip"
end

execute "install python-dev build-essential" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install python-dev build-essential -y"
end

execute "install WebOb" do
  command "sudo chroot /home/jaulas/saucy32/ easy_install3 WebOb"
end

execute "install Paste" do
  command "sudo chroot /home/jaulas/saucy32/ easy_install3 Paste"
end

execute "install webapp2" do
  command "sudo chroot /home/jaulas/saucy32/ easy_install3 webapp2"
end

#Ahora, vamos a descargar el SDK de Google App, clonar nuestro proyecto .git y vamos a poner en funcionamiento nuestra app en la jaula.

#Instalamos wget para poder descargar archivos
execute "install wget" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install wget -y"
end

#Instalamos curl para posteriormente poder realizar los test de pruebas
execute "install curl" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install curl -y"
end

#Descargamos el sdk de Google App Engine
execute "download google-api" do
  command "sudo chroot /home/jaulas/saucy32/ wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.17.zip --no-check-certificate"
end

# Instalamos la herramienta zip
execute "install zip" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install zip -y"
end

# Descomprimimos el fichero descargado, con lo que ya tendremos disponibles las herramientas del sdk
execute "unzip google-api" do
 command "sudo chroot /home/jaulas/saucy32/ unzip -o google_appengine_1.9.17.zip"
end

# Instalamos la herramienta cURL para hacer uso de ésta a la hora de ejecutar los tests
execute "install curl" do
 command "sudo chroot /home/jaulas/saucy32/ apt-get install curl -y"
end

# Una vez hecho esto ya tenemos instalado el entorno de desarrollo necesario para construir y ejecutar aplicaciones que luego funcionarán bajo Google App Engine
#Instalamos git
execute "install git" do
  command "sudo chroot /home/jaulas/saucy32/ apt-get install -y git -y"
end

# Clonamos la carpeta en donde se encuentran los ficheros fuentes de la aplicacion
execute "download sources" do
  command "sudo chroot /home/jaulas/saucy32/ git clone https://github.com/miguelfabre/pruebadriveiv.git"
end

#Ejecutamos el .py de nuestra app

#execute "execute app"
#	command "sudo chroot /home/jaulas/saucy32/ python google_appengine/dev_appserver.py --host=0.0.0.0 pruebadriveiv/"
#end



