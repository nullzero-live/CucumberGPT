import os
import wandb
# turn on wandb logging for langchain



class wandbUtil:
    
    def __init__(self):
        self.token = os.getenv("WANDB_API_KEY")
    
    def wandb_login(self):
        wandb.login(key=self.token)
        os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
        return 
        
        
