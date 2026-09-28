# Kitchen Conversions — built in two stages.
#
# The generated site is deliberately NOT committed to git (see .gitignore: public/ is a
# build artefact). Stage 1 runs the generator from source, so the image is reproducible from
# the repository alone and the numbers on the site can never drift from content/.

FROM python:3.12-alpine AS site
WORKDIR /site
COPY generator/ generator/
COPY content/ content/
COPY assets/ assets/
RUN python3 generator/build.py && test -f public/index.html && test -d public/assets

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=site /site/public/ /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz || exit 1
