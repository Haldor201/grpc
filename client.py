import grpc
import gRPC_pb2
import gRPC_pb2_grpc
import bd
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = gRPC_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(gRPC_pb2.HelloRequest(name='U20245299'))
    print("Estudiante: " + response.message)

if __name__ == '__main__':
    run()