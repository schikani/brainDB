
sudo apt-get install build-essential libreadline-dev libffi-dev git
pkg-config gcc-arm-none-eabi libnewlib-arm-none-eabi

git clone https://github.com/micropython/micropython.git ./db_scripts/upython

cd ./db_scripts/upython/mpy-cross && make
cd ../ports/unix
make submodules && make
cp micropython ../../../