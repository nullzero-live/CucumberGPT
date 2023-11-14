import os

import wandb

from ._ops_constants import CONSTANTS 
from utils.logger_util import setup_logger

# turn on wandb logging for langchain



class cfgWAB:
    
    def __init__(self):
        self.token = os.getenv("WANDB_API_KEY")
        _logger = setup_logger(__name__)
    
    def wandb_login(self):
        wandb.login(key=self.token)
        os.environ["LANGCHAIN_WANDB_TRACING"] = CONSTANTS.get("LANG_WANDB_ON")
        return 
        
        
