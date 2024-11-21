



def generate_importance_score(records: List[str]) ->  List[float]:
    return run_gpt_generate_importance(records, "1", LLM_VERS)[0]
    

class ConceptNode():
    def __init__(self, node_dict: Dict(str, Any)):
        curr_package = {}
        self.node_id = node_dict["node_id"]
        self.node_type = node_dict["node_type"]
        
        self.content = node_dict["content"]
        self.created = node_dict["created"]
        self.last_retrieved = node_dict["last_retrieved"]
        self.importance = node_dict["importance"]
        self.pointer_id = node_dict["pointer_id"]
        
        return curr_package
        
        
class MemoryStream:
     def __init(self,
                nodes: List[Dict[str, Any]],
                embeddings: Dict[str, List[float]]):
         self.seq_nodes =[]
         self.id_to_node = dict()
         for node in nodes:
             new_node = ConceptNode(node)
             self.seq_nodes += [new_node]
             self.id_to_node[new_node.node_id] = new_node
        
        self.embeddings = embeddings
        
def _add_node(self, 
              time_step: int,
              node_type: str,
              content: str,
              importance: float,
              pointer_id: Optional[int]):
        node_dict = dict()
        self.node_id = node_dict["node_id"]
        self.node_type = node_dict["node_type"]
        
        self.content = node_dict["content"]
        self.created = node_dict["created"]
        self.last_retrieved = node_dict["last_retrieved"]
        self.importance = node_dict["importance"]
        self.pointer_id = node_dict["pointer_id"]


def remember(self, content:str, time_stemp: int = 0):
    # calculate the importance score before add the memory
    score = generate_importance_score([content])[0]
    self._add_node(time_step, "observation", content, score, None)
    