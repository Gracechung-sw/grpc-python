import unittest
from unittest.mock import patch, Mock

from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

from greeter_server import Greeter


class GreeterTest(unittest.TestCase):
    def setUp(self):
        # Server
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        helloworld_pb2_grpc.add_GreeterServicer_to_server(
            Greeter(), self._server)
        self._server.add_insecure_port('[::]:50051')
        self._server.start()

        # Client
        self._channel = grpc.insecure_channel('localhost:50051')
        self._stub = helloworld_pb2_grpc.GreeterStub(self._channel)

        self._context = Mock()
        self._greeter = Greeter()

    def tearDown(self):
        self._server.stop(None)

    def test_greet_with_server(self):
        response = self._stub.SayHello(
            helloworld_pb2.HelloRequest(name='Test'))
        assert(response.message == "Hello, Test!")

    def test_greet_with_mock(self):
        response = self._greeter.SayHello(
            request=helloworld_pb2.HelloRequest(name='Test'), context=self._context)
        assert (response.message == "Hello, Test!")


if __name__ == '__main__':
    unittest.main()
