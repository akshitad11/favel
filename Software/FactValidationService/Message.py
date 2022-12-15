import json

class Message:
    
    def __init__(self, type:str=None, content=None, subject:str=None, predicate:str=None, object:str=None, score=None, text:str=None):
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
        if self.type == "call":
            return json.dumps({"type": self.type, "content": self.content})
        if self.type == "train":
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object, "score": self.score})
        if self.type == "test":
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object, "score": self.score})
    
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

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        if(score == None):
            pass
        elif float(score) == float('inf') or float(score) == float('-inf') or float(score) == float('nan'):
            self._score = 0
        else:
            self._score = score
