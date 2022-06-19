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

        try:
            response = stub.SayHelloStrict(helloworld_pb2.HelloRequest(
                name='Leonhard Euler'))
        except grpc.RpcError as e:
            # ouch!
            # lets print the gRPC error message
            # which is "Length of `Name` cannot be more than 10 characters"
            print(e.details())
            # lets access the error code, which is `INVALID_ARGUMENT`
            # `type` of `status_code` is `grpc.StatusCode`
            status_code = e.code()
            # should print `INVALID_ARGUMENT`
            print(status_code.name)
            # should print `(3, 'invalid argument')`
            print(status_code.value)
            # want to do some specific action based on the error?
            if grpc.StatusCode.INVALID_ARGUMENT == status_code:
                # do your stuff here
                pass
        else:
            print(response.Result)

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
