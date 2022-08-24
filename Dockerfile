FROM python:3

ADD spotifybotify.py /

RUN pip install requests

CMD [ "python","-u", "./spotifybotify.py" ]