##################################################
#                                                #
#  dolphin version beta-3                        #
#                                                #
#  Container designed with:                      #
#  RedHat Enterprise Linux 8 base image          #
#                                                #
#  The dolphin project develops images with RHEL #
#+ RHEL to ensure high quality and security.     #
#                                                #
##################################################

FROM registry.access.redhat.com/ubi8/ubi:latest

WORKDIR /dolphin

# Confire Python 3.X environment
RUN yum install -y python3; \
	yum clean all;

# Install PIP requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Begin copy of project files
COPY . .

# Program ENTRYPOINT
ENTRYPOINT ["python3", "dolphin.py"]