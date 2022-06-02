import configparser, logging, argparse

from FactValidationService.Validator import Validator
from InputService.Input import Input

def main():
    # Parse arguments
    args = parseArguments()
    
    # Read config
    configParser = loadConfig()

    # Configure logging
    configureLoggin(configParser)
    
    # Execute method
    if args.cache:
        validateCache(args, configParser)
    else:
        validateInputData(args, configParser)    
    
    # Write results
    # TODO: write results to file
    
def validateInputData(args, configParser):
    # Read input
    input = Input()
    assertions = input.getInput(args.data)

    # Validate assertions
    logging.info("Validating assertions")
    validator = Validator(dict(configParser['Approaches']), configParser['General']['cachePath'], configParser['General']['useCache'])
    result = validator.validate(assertions)

def validateCache(args, configParser):
    logging.info("Checking cache for correctness")
    validator = Validator(dict(configParser['Approaches']), configParser['General']['cachePath'])
    validator.validateCache()
    
def parseArguments():
    argumentParser = argparse.ArgumentParser()
    exclusionGroup = argumentParser.add_mutually_exclusive_group(required=True)

    exclusionGroup.add_argument("-d", "--data", help="Path to input data")
    exclusionGroup.add_argument("-c", "--cache", action="store_true", help="Check whether the cache entries are correct")
    return argumentParser.parse_args()
    
def loadConfig():
    configParser = configparser.ConfigParser()
    configParser.read("favel.conf")
    return configParser

def configureLoggin(configParser:configparser.ConfigParser):
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['warning'] = logging.WARNING
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['General']['logging']])
    

if __name__ == '__main__':
    main()