FROM python:3.10-slim

#copy application code
COPY . /app/

#setup working directory

WORKDIR /app
#install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libportaudio2 \
    portaudio19-dev \
    gcc \
    libc-dev \
    make \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg


#expose port
EXPOSE 7860

#start code inside container..using cmd it become our terminal
CMD ["sh", "-c", "python front_app.py"]
