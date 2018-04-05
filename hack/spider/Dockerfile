FROM python:3.6
RUN mkdir /root/code & mkdir /root/spider163
WORKDIR /root/code
ADD ./ /root/code/
ADD hack/spider/spider163.conf /root/spider163/spider163.conf
RUN pip install -e . -i http://mirrors.aliyun.com/pypi/simple --trusted-host=mirrors.aliyun.com && spider163 --help
ENTRYPOINT spider163 webserver


