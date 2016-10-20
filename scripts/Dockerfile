FROM caffe:cpu
ADD src /opt/flask_nsfw
WORKDIR /opt/flask_nsfw
RUN pip install -r flask_nsfw/requirements.txt
RUN ln -s /opt/flask_nsfw/open_nsfw /usr/local/lib/python2.7/dist-packages
VOLUME ["/opt/flask_nsfw"]
CMD ["python", "-m", "flask_nsfw.app"]
