import threading
import socket
import logging
from FactValidationService.Cache import Cache
from FactValidationService.AssertionsRunner import AssertionsRunner
from FactValidationService.Message import Message

class AssertionsCacheRunner(AssertionsRunner):
    """
    Uses the functionality of AssertionsRunner to validate a list of assertions.
    Overrides validation of an assertion to cache results in a database to speed up future validations.
    """

    def __init__(self, approach:str, port:int, trainingAssertions:list, testingAssertions:list, cachePath:str):
        super().__init__(approach, port, trainingAssertions, testingAssertions)
        threading.Thread.__init__(self)
        self.cachePath = cachePath
    
    def run(self):
        try:
            self.cache = Cache(self.cachePath, self.approach)
            super().run()
            self.cache.close()
        except Exception as ex:
            self.exception = ex
            
    def _validateAssertion(self, assertion):
        """
        Overrides super method.
        Before sending an assertion to the approach, see if the result has been cached in the database.
        If not, send assertion to the approach and add the result to the database.
        """
        cacheResult = self.cache.getScore(assertion.subject, assertion.predicate, assertion.object)
        if cacheResult != None:
            return Message(type="test_result", score=cacheResult)
        
        result = super()._validateAssertion(assertion)
        if result.type == "test_result":
            self.cache.insert(assertion.subject, assertion.predicate, assertion.object, result.score)
        return result
        