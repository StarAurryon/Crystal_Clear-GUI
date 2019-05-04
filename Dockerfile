FROM ubuntu:18.04
RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y --no-install-recommends gunicorn3 python3-pip git && apt-get clean && \
        mkdir -p /opt/crystal_clear-gui && cd /opt/crystal_clear-gui && git clone https://github.com/StarAurryon/Crystal_Clear-GUI.git . && \
        rm -r .git && mkdir -p data/in data/out && useradd -r crystal_clear && chown -R crystal_clear:crystal_clear /opt/crystal_clear-gui && \
        pip3 install flask filetype && apt-get purge -y git python3-pip && apt-get purge -y --autoremove

WORKDIR /opt/crystal_clear-gui
USER crystal_clear
EXPOSE 5000
CMD ["gunicorn3", "--access-logfile", "'-'", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
