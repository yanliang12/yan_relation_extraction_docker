##########Dockerfile###########
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y tar

RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

WORKDIR /

RUN wget http://nlp.stanford.edu/software/stanford-corenlp-4.1.0-models-english-kbp.jar
RUN wget http://nlp.stanford.edu/software/stanford-corenlp-4.1.0.zip

RUN unzip stanford-corenlp-4.1.0.zip

RUN mv /stanford-corenlp-4.1.0-models-english-kbp.jar /stanford-corenlp-4.1.0/

WORKDIR /stanford-corenlp-4.1.0/

RUN pip3 install py4j==0.10.9

RUN wget https://repo1.maven.org/maven2/net/sf/py4j/py4j/0.10.7/py4j-0.10.7.jar

RUN echo "gsgdsewr"

RUN git clone https://github.com/yanliang12/yan_relation_extraction_docker.git
RUN mv yan_relation_extraction_docker/* ./

RUN bash jessica_build_java_class.sh

CMD bash
##########Dockerfile###########