# Quickstart with docker
Start writing posts quickly with docker

```
git clone https://github.com/wearearima/wearearima.github.io.git
$ cd wearearima.github.io
$ docker run -p 4000:4000 --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll jekyll server
```

To see content in __draft_ folder
```
$ git clone https://github.com/wearearima/wearearima.github.io.git
$ cd wearearima.github.io
$ docker run -p 4000:4000 --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll jekyll server --draft
```
You can then access blog here: http://localhost:4000

## Using cache

In case you want to speed up consecutive builds, you can use Docker volumes to store Jekyll's gems locally. This can be done in like this:

Create a docker volume:
```
docker volume create jekyll-ruby-gems
```
Each time we want to launch our Jekyll container, run it like this:
````
docker run --rm -p 4000:4000 --name jekyll --volume="$PWD:/srv/jekyll" --mount source=jekyll-ruby-gems,target=/usr/local/bundle -it jekyll/jekyll:3.8 jekyll serve
