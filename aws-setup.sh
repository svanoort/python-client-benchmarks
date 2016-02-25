# Config
# c4.large, 8 GB volume, open security group, Amazon linux

sudo yum update -y
# GCC and libcurl are needed to pip install pycurl
sudo yum install -y python python pycurl python-pip git docker
cd /tmp
git clone https://github.com/svanoort/python-client-benchmarks/
cd python-client-benchmarks
git checkout command-line-run
sudo pip install -r requirements.txt  # Will fail for pycurl

# Start bench env
sudo service docker start
sudo sh build-docker.sh
sudo ./run-docker.sh &