"""The Python implementation of the GRPC helloworld.Greeter client."""
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

        rectangle = helloworld_pb2.Rectangle(
            lo=helloworld_pb2.Point(latitude=400000000, longitude=-750000000),
            hi=helloworld_pb2.Point(latitude=420000000, longitude=-730000000))
        print("Looking for features between 40, -75 and 42, -73")
        response = stub.ListFeatures(rectangle)
        for feature in response:
            print("Feature called %s at %s" % (feature.name, feature.location))


if __name__ == '__main__':
    logging.basicConfig()
    run()
