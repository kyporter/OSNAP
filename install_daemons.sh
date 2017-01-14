cd $HOME

curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2 

tar -xjf httpd-2.4.25.tar.bz2

cd /home/osnapdev/httpd-2.4.25

./configure --prefix=$HOME/installed

make

make install 

cd $HOME/installed

git clone https://github.com/postgres/postgres.git
