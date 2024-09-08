import grpc
from concurrent import futures
import gRPC_pb2
import gRPC_pb2_grpc
from bd import findByCode
import json
import os  # Importa os para leer variables de entorno

class GreeterServicer(gRPC_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        try:
            print("Solicitud Recibida")
            resultado = findByCode(request.name)
            
            if resultado:
                resultado['_id'] = str(resultado['_id'])
                message = json.dumps(resultado)
            else:
                message = "No se encontró el código"
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return gRPC_pb2.HelloReply(message="Error interno del servidor")
        return gRPC_pb2.HelloReply(message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gRPC_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    
    # Obtén el puerto de la variable de entorno o usa 50051 como predeterminado
    port = os.environ.get('PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
