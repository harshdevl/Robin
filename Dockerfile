#from python 3 
FROM amd64/python:3

#first copying whl file to download it first 
COPY requirements.txt /Robin/
COPY . /Robin/
#setting workdir
WORKDIR /Robin/

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio
RUN pip install -r requirements.txt 

#running cmds
CMD [ "python", "main.py" ]


