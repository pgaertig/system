FROM debian:stable-slim
ENV LC_ALL=en_US.utf-8 LANG=en_US.utf-8 LANGUAGE=en_US:en
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo \
      locales bash-completion mc dropbear rsync openssh-client acl curl \
      qrencode nano vim git python3 python3-pip mc docker.io && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

EXPOSE 122
CMD /usr/sbin/dropbear -p 122 -a -s -E -F
