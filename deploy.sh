eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /var/www/gundam-backend #helloworld
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop flask-back
docker rm flask-back
docker rmi woka/containerd:be-latest
docker run -d --name flask-back -p 5000:5000 woka/containerd:be-latest

