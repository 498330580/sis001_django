# 基础版本python3.10
FROM python:alpine3.10
# 创建工作目录
RUN mkdir -p /app

# 指定语言，防止中文日志乱码
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# 指定代理环境变量
ENV PROXY_TYPE http
ENV PROXY_URL 127.0.0.1:10809
ENV COOKIES cookies

# 指定pip源，并更新pip
COPY pip.conf /root/.pip/pip.conf
RUN pip install --upgrade pip

# 有以下内容才能安装Pillow
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# 安装nginx
# RUN apk add nginx

# 安装依赖
COPY requirements.txt /app
RUN pip install -I -r /app/requirements.txt

# 添加项目文件到app目录
COPY . /app

# 添加定时任务
COPY python-cron /etc/cron.d/python-cron
RUN chmod 0644 /etc/cron.d/python-cron
RUN crontab /etc/cron.d/python-cron
# RUN touch /app/logs/get_xiaosuo.log

# 容器对外暴露8000断开
EXPOSE 8000
# 用于指定持久化目录（指定此目录可以被挂载出去）
VOLUME ['/app/data', "/app/logs"]

# 指定工作目录
WORKDIR /app

# 运行定时任务
# CMD ["crond", "start"]
# CMD ['crond', '-l 2', '-f']
# CMD crond && tail -f /app/logs/get_xiaosuo.log
# 运行django
# CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD crond && uwsgi --ini uwsgi.ini