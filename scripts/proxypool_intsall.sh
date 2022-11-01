git clone https://github.com/Python3WebSpider/ProxyPool.git;
cd ProxyPool;
wget https://download.redis.io/releases/redis-7.0.5.tar.gz;
tar -zxvf redis-7.0.5.tar.gz;
cd redis-7.0.5;
make MALLOC=libc;
mkdir lib && cp -rf redis-5.0.14/src ./lib;
cd src && make install;
redis-server;