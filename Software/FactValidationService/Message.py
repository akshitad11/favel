import json
from builtins import object

class Message:
    
    def __init__(self, type:str=None, content=None, subject:str=None, predicate:str=None, object:str=None, score=None, text:str=None):
        """
        Available types are:
            call    with content:
                - type
                - training_start
                - training_complete
            training with contents
        """
        if text != None:
            self.parse(text)
        else:
            self._type = type
            self.content = content
            self.subject = subject
            self.predicate = predicate
            self.object = object
            self.score = score
    
    def serialize(self):
        if type == "call":
            return json.dumps({"type": self.type, "content": self.content})
        if type == "training":
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object, "score": self.score})
        if type == "testing":
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object})
    
    def parse(self, text:str):
        response = json.loads(text)
        self.type = response["type"]

        if self.type == "test_result":
            self.score = response["score"]
        elif self.type == "ack":
            self.content = response["content"]
        elif self.type == "type_response":
            self.content = response["content"]
        elif self.type == "error":
            self.content = response['content']
            
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if type in ["call", "train", "test", "test_result", "ack", "type_response", "error"]:
            self._type = type
        
        

