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
````

## Deployment

The site is published through Google App Engine. The workflow in `.github/workflows/deploy.yml` builds the Jekyll site, copies the generated `_site` directory, and deploys a lightweight Flask wrapper that serves the static assets. Workload Identity Federation is used for authentication.

Manual deployment steps:

1. `JEKYLL_ENV=production bundle exec jekyll build`
2. `gcloud app deploy app.yaml`

Ensure your `gcloud` CLI is authenticated and targeting the `blog-arima-eu` project. Keep `_site`, `main.py`, `requirements.txt`, and the committed `.gcloudignore` together when running the deployment so App Engine can serve the generated files. The runtime currently uses Python 3.10 (see `app.yaml`).

### Required GCP roles

The GitHub Actions service account needs at least:

- `roles/appengine.deployer`
- `roles/iam.serviceAccountTokenCreator`
- `roles/storage.objectAdmin` on the `staging.blog-arima-eu.appspot.com` bucket (or broader storage permissions)
- `roles/iam.serviceAccountUser` on `blog-arima-eu@appspot.gserviceaccount.com`
