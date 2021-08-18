FROM python:3.7

# stdout和stderr不缓存
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 安装Python依赖包
COPY ./requirements ./requirements
RUN pip install -r requirements/local.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
