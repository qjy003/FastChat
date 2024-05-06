# 需要使用的jdos基础镜像
FROM forecast-ai/cbimg15607:vmaster.20230511.231740.507
# 设置语言
ENV LANG zh_CN.UTF-8
RUN curl http://ngx2agent-agent.harbor.svc.n.jd.local/application_worker/other/image-install.sh|sh
# 更新镜像中的默认的pip版本，解决因为pip版本过低导致安装python依赖包报错的问题
RUN pip3 install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN pip3 install --upgrade setuptools -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN yum -y install python3-devel
# 默认工作目录，使用Dockerfile方式构建的应用镜像，应用文件会默认复制到/home/apps下
ADD . /home/export/App/
# 安装python项目包依赖
RUN yum -y install hostname tree&& \
    yum clean all && \
    pip3 install -r /home/export/App/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com && \
    chmod +x /home/export/App/* && \
    echo 1 > /home/admin/app_info
EXPOSE 80
EXPOSE 22
EXPOSE 9501
EXPOSE 9502
EXPOSE 9503
# 安装虎符
RUN yum install -y wget openssh* && yum clean all
RUN mkdir -p /opt
ADD ./hf_docker_install.sh /opt
ENV JD_ONLINE_MAIN_PATH="/home/export/App"
ENV JD_ONLINE_BAD_CASE_DIR="/export/Data"
ENV JD_ONLINE_PORT=80
ENV JD_ONLINE_LOGGING_DIR="/export/Data"
ENV JD_ONLINE_KNOWLEDGE_BASE_DIR="/home/export/App/data/docs"
# 运行服务
ENTRYPOINT /usr/sbin/crond && /usr/sbin/sshd && python3 /home/export/App/main.py && sleep 9999999d
