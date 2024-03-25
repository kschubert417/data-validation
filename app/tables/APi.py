import grpc
import sys
import os
import logging
#from chirpstack_api import gateway_pb2, gateway_pb2_grpc
# Configure logging (optional)
logging.basicConfig(filename='gateway_creation.log', level=logging.INFO)

import chirpstack_api.api.gateway_pb2 as gateway_pb2
import chirpstack_api.api.gateway_pb2_grpc as gateway_pb2_grpc

#Define ChirpStack server address and API token
server = "localhost:8080"
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6ImU5MjBkMTA3LWFlZjQtNDc2Ny05NjFiLTQzZWZhZmQxZDRlYiIsInR5cCI6ImtleSJ9.5GYheEdW3A9zW38Ttb7bP3Q5jM8HHToXXPaxpp4bmJY"
gateway_info = {
    "gateway_id": "0016C001F111523E",
    "name": "gateway1",
    "tags": {
        "tag1": "value1",
        "tag2": "value2"
    }
}


# Create a gateway message object
gateway = gateway_pb2.Gateway(**gateway_info)

# Connect to ChirpStack server
channel = grpc.insecure_channel(server)

# Create a stub for the GatewayService
stub = gateway_pb2_grpc.GatewayServiceStub(channel)

# Create the gateway
try:
    # Print debug information before sending the request
    print("Sending CreateGatewayRequest:")
    print(gateway)

    # Send the CreateGatewayRequest
    response = stub.Create(gateway)

    print("Gateway created successfully!")
except Exception as e:
    print(f"Error creating gateway: {e}")
# Close the channel
channel.close()