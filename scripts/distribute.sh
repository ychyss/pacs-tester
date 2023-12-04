#!/bin/bash
# 将文件分发到其他机器,进行多节点测试
# 默认使用root发送, 因此每次操作中途都需要输入密码

# Remote hosts (replace with your remote hostnames or IPs)
HOSTS=("bmecluster01" "bmecluster02")

# Local file to send (replace with your local file path)
LOCAL_FILE="../dist/dist.7z"

# Remote directory where the file will be sent (replace with your remote directory path)
REMOTE_DIR="/home/user/apps/pacs-tester"

# Remote port number (replace with your desired port)
PORT="22"

# Get the file name from the local file path
FILE_NAME=$(basename "${LOCAL_FILE}")

# Iterate over each remote host and send the file
for HOST in "${HOSTS[@]}"; do
  echo "Sending file to root@${HOST}"

  # Check if the remote directory exists, and create it if it doesn't
  ssh "root@${HOST}" "mkdir -p ${REMOTE_DIR}"

  # Send the file to the remote host
  scp "${LOCAL_FILE}" "root@${HOST}:${REMOTE_DIR}"

  # Unzip the file on the remote host
  ssh -p "${PORT}" "root@${HOST}" "cd ${REMOTE_DIR} && 7za x ${REMOTE_DIR}/${FILE_NAME} && rm ${REMOTE_DIR}/${FILE_NAME}"
done

echo "File sent to all remote hosts."
