#!/usr/bin/env bash
set -e

proto_dir=$KUBE_MSG/proto
app_dir=$KUBE_MSG/messenger/messenger
messenger_python_out_dir=$app_dir/proto/messenger
alerts_python_out_dir=$app_dir/proto/alerts
venv=$KUBE_MSG/messenger/venv

$venv/bin/python \
    -m grpc_tools.protoc \
    -I $proto_dir \
    --python_out=$alerts_python_out_dir \
    --grpc_python_out=$alerts_python_out_dir \
    $proto_dir/alerts.proto

$venv/bin/python \
    -m grpc_tools.protoc \
    -I ${proto_dir} \
    --python_out=${messenger_python_out_dir} \
    --grpc_python_out=${messenger_python_out_dir} \
    $proto_dir/messenger.proto
