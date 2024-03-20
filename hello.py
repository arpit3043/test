from queue import Queue
import uuid
class Validator:
    @staticmethod
    def is_valid_action(action):
        valid_actions = ['accept', 'reject']
        return action in valid_actions

class Parser:
    @staticmethod
    def parse_data(data):
        if 'sdp_offer' not in data or 'caller_number' not in data or 'calling_id' not in data:
            raise ValueError("Invalid data format")
        return data

class Checker:
    @staticmethod
    def is_stable_connection(response):
        return response.status_code == 200

class WSConnectionManager:
    def __init__(self, url):
        self.url = url

    def connect(self):
        # WebSocket connection logic
        pass

    def send(self, message):
        pass  # sending message via WebSocket

    def receive(self):
        pass  # Implement receiving message via WebSocket

    def handle_connection(self, con):
        pass  # Implement handling connection logic

class WebRTCGateway:
    def __init__(self, url_gateway):
        self.ws = WSConnectionManager(url_gateway)
        self.session_id = None

    def get_session(self):
        if not self.session_id:
            transaction_id = uuid.uuid4().hex
            message = {"janus": "create", "transaction": transaction_id}
            self.ws.send(message)
            # Create session logic here
            self.session_id = "12345"  # Placeholder, actual session ID from response
        return self.session_id

    def create_offer(self, sdp_offer):
        session_id = self.get_session()
        message = {"janus": "offer", "sdp_offer": sdp_offer, "session_id": session_id}
        self.ws.send(message)
        # Logic to handle response and get SDP answer
        sdp_answer = "Dummy SDP answer"  # Placeholder
        return sdp_answer

class JanusGateway(WebRTCGateway):
    def create_offer(self, sdp_offer):
        # Overriding create_offer method to handle Janus-specific logic
        session_id = self.get_session()
        message = {"janus": "offer", "sdp_offer": sdp_offer, "session_id": session_id}
        self.ws.send(message)
        # Additional Janus-specific logic for handling response and getting SDP answer
        sdp_answer = "Janus-specific SDP answer"  # Placeholder
        return sdp_answer
    
class Consumer:
    def __init__(self, queue, gateway):
        self.queue = queue
        self.gateway = gateway

    def consume_and_process(self):
        while True:
            data = self.queue.get()
            if data == 'STOP':
                break
            print(f"Consumed data: {data}")
            sdp_offer = data.get('sdp_offer')
            sdp_answer = self.gateway.create_offer(sdp_offer)
            print(f"Received SDP answer: {sdp_answer}")

class Producer:
    def __init__(self):
        pass  # Initialization logic for producer

    def produce(self):
        pass  # Logic to produce data

class WaApiClient:
    def __init__(self, sdp_answer=None, call_id=None):
        self.sdp_answer = sdp_answer
        self.call_id = call_id

    def prepare_payload(self, action):
        # Prepares the payload for WhatsApp API request.
        valid_actions = ['accept', 'reject']
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Expected one of {valid_actions}")
        payload = {'action': action}
        if action == 'accept':
            payload.update({'sdp_answer': self.sdp_answer, 'call_id': self.call_id})
        elif action == 'reject':
            payload.update({'call_id': self.call_id})
        return payload

    def call_api(self, action):
        # Sends a request to the Web API with the prepared payload.
        payload = self.prepare_payload(action)
        response = requests.post('https://api.com/process_call', data=payload)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")
        return response.json()
