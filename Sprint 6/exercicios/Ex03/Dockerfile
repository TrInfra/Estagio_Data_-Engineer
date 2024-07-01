FROM amazonlinux:2.0.20200602.0
RUN yum update -y
RUN amazon-linux-extras install -y python3.8
RUN yum install -y python3-pip zip
RUN yum -y clean all
RUN python3.8 -m pip install --upgrade pip