# grpc-python

## gPRC and protocol buffers

gRPC can use protocol buffers as both its Interface Definition Language (**IDL**)

- https://developers.google.com/protocol-buffers/docs/proto3
- On the server side, the server implements this interface and runs a gRPC server to handle client calls.
- On the client side, the client has a stub (referred to as just a client in some languages) that provides the same methods as the server.

By default, gRPC uses [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview)
, Google’s mature open source mechanism for serializing structured data (although it can be used with other data formats such as JSON).

1. define the structure for the data you want to serialize in a ._proto file_

   Protocol buffer data is structured as *messages*, where each message is a small logical record of information containing a series of name-value pairs called *fields*. Here’s a simple example:

```protobuf
message Person {
  string name = 1;
  int32 id = 2;
  bool has_ponycopter = 3;
}
```

2. use the protocol buffer compiler `protoc`
    to generate data access classes in your preferred language(s) from your proto definition.
   if your chosen language is Python, running the compiler on the example above will generate a class called `Person`.

## setup

```bash
$ virtualenv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Define proto

gRPC is based around the idea of defining a service, specifying the methods that can be called remotely with their parameters and return types.

그러니까 service에 gPRC server와 client가 request, response를 할 수 있는 method를 정의하는 것이다.

```protobuf
service HelloService {
	rpc SayHello (HelloRequest)returns (HelloResponse);
}

message yesHelloRequest {
	string greeting = 1;
}

message HelloResponse {
	string reply = 1;
}
```

- client가 single request를 보내고, server가 그 요청을 받아서 single response를 보내는 식의 service method는 `rpc SayHello(HelloRequest) returns (HelloResponse);` 이런 식으로 작성된다.
- 반면 A response-streaming RPC where the client sends a request to the server and gets a stream to read a sequence of messages back. The client reads from the returned stream until there are no more messages. As you can see in the example, you specify a response-streaming method by placing the stream keyword before the response type. stream일 때는 `rpc LotsOfReplies(HelloRequest) returns (stream HelloResponse);` 이런 식으로 작성한다.

## Generate server and client code using the protocol buffer compiler.

```bash
$ python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/helloworld.proto
```

This regenerates

- `helloworld_pb2.py`: contains our generated **request and response** classes
- `helloworld_pb2_grpc.py` : contains our generated **client and server** classes.
  - classes for the messages defined in helloworld.proto
  - classes for the service defined in helloworld.proto
    - `class GreeterStub(object):`, which can be used by clients to invoke RouteGuide RPCs
    - `class GreeterServicer(object):`, which defines the interface for implementations of the RouteGuide service
  - a function for the service defined in helloworld.proto
    - `def add_GreeterServicer_to_server(servicer, server):`, which adds a RouteGuideServicer to a grpc.Server

## Use the Python gRPC API to write a simple client and server for your service.

The Python implementation of the GRPC helloworld.Greeter server.

- https://developers.google.com/protocol-buffers/docs/reference/python-generated

## Run

Run the server:

```bash
$ python greeter_server.py
```

From another terminal, run the client:

```bash
$ python greeter_client.py
```

Result

```
Greeter client received: Hello, you!
Greeter client received: Hello again, you!
Looking for features between 40, -75 and 42, -73
Feature called Patriots Path, Mendham, NJ 07945, USA at latitude: 407838351
longitude: -746143763

Feature called 101 New Jersey 10, Whippany, NJ 07981, USA at latitude: 408122808
longitude: -743999179

Feature called U.S. 6, Shohola, PA 18458, USA at latitude: 413628156
longitude: -749015468

Feature called 5 Conners Road, Kingston, NY 12401, USA at latitude: 419999544
longitude: -740371136

Feature called Mid Hudson Psychiatric Center, New Hampton, NY 10958, USA at latitude: 414008389
longitude: -743951297

Feature called 287 Flugertown Road, Livingston Manor, NY 12758, USA at latitude: 419611318
longitude: -746524769

Feature called 4001 Tremley Point Road, Linden, NJ 07036, USA at latitude: 406109563
longitude: -742186778

.....

...

```
