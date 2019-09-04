# Quickstart with docker
Start writing posts quickly with docker

```
git clone https://github.com/wearearima/wearearima.github.io.git
cd wearearima.github.io
docker run -p 4000:4000 --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll jekyll server
```
You can then access blog here: http://localhost:4000