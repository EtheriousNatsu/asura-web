# 从django镜像开始构建
FROM test_asura_service:latest

# 版本号控制
ENV WAIT_VERSION 2.7.2

# 设置工作目录
WORKDIR /app

# 下载脚本
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait

# 赋予执行权限
RUN chmod +x /wait
