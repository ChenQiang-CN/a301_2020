FROM busybox

RUN mkdir -p /srv/a301_notebooks
COPY ./notebooks/ /srv/a301_notebooks

CMD tail -f /dev/null


