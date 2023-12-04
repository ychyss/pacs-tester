#!/bin/bash
# 通过多台发送请求到PACS

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <operation> [args]"
  echo "Available operations: generate, send, delete"
  exit 1
fi

OPERATION=$1
shift

LOCAL_APP_DIR="/home/hys/WS_python/data-platform/test/pacs-tester/"
REMOTE_APP_DIR="/home/user/apps/pacs-tester"

# Default input and output directories
INPUT_DIR="./source_data/Head"
OUTPUT_DIR="./test_data"

GATEWAY_AE="DCM_GATEWAY"
GATEWAY_HOST="192.168.1.200"
GATEWAY_PORT="32005"
DCM4CHE_PATH="./dcm4che-5.26.0"
MAX_WORKERS=2
SERIES_COUNT=5

declare -a REMOTE_HOSTS=()

for arg in "$@"
do
  case $arg in
    --input-dir=*)
    INPUT_DIR_ARG="$arg"
    shift
    ;;
    --output-dir=*)
    OUTPUT_DIR_ARG="$arg"
    shift
    ;;
    --remote-host=*)
    REMOTE_HOSTS+=("${arg#*=}")
    shift
    ;;
    *)
    shift
    ;;
  esac
done

# Set the input-dir and output-dir arguments to their default values if not provided
if [ -z "$INPUT_DIR_ARG" ]; then
  INPUT_DIR_ARG="--input-dir=$DEFAULT_INPUT_DIR"
fi

if [ -z "$OUTPUT_DIR_ARG" ]; then
  OUTPUT_DIR_ARG="--output-dir=$DEFAULT_OUTPUT_DIR"
fi

# Pass the provided arguments along with input-dir and output-dir to the local and remote applications
for remote_host in "${REMOTE_HOSTS[@]}"; do
  ssh $remote_host "cd $REMOTE_APP_DIR && python main.py --$OPERATION --input-dir $INPUT_DIR --output-dir $OUTPUT_DIR --gateway-ae $GATEWAY_AE --gateway-host $GATEWAY_HOST --gateway-port $GATEWAY_PORT --dcm4che-path $DCM4CHE_PATH --max-workers $MAX_WORKERS" &
done

#cd $LOCAL_APP_DIR
#python main.py --$OPERATION --input-dir $INPUT_DIR --output-dir $OUTPUT_DIR --gateway-ae $GATEWAY_AE --gateway-host $GATEWAY_HOST --gateway-port $GATEWAY_PORT --dcm4che-path $DCM4CHE_PATH --max-workers $MAX_WORKERS

wait
