# grpc-python

## setup

```bash
$ virtualenv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Generate

```bash
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/pingpong.proto
```
