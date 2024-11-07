import sys
sys.path.append('./')  # Add the current directory to the path

# Import the necessary functions and classes from the correct path
from generative_agent.modules.memory_stream import MemoryStream, extract_recency, extract_importance, extract_relevance

# Mock Data for Testing
nodes = [
    {
        "node_id": 0,
        "node_type": "observation",
        "content": "This is the first observation.",
        "importance": 0.8,
        "created": 1,
        "last_retrieved": 2,
        "pointer_id": None
    },
    {
        "node_id": 1,
        "node_type": "observation",
        "content": "This is the second observation.",
        "importance": 0.9,
        "created": 2,
        "last_retrieved": 3,
        "pointer_id": None
    }
]

# Example Embeddings
embeddings = {
    "This is the first observation.": [0.1, 0.2, 0.3],
    "This is the second observation.": [0.2, 0.2, 0.5],
    "focal_point": [0.2, 0.3, 0.5]
}

# Initialize a MemoryStream object with mock data
memory_stream = MemoryStream(nodes, embeddings)

# Test extract_recency
def test_extract_recency():
    print("\n--- Testing Recency Extraction ---")
    recency_scores = extract_recency(memory_stream.seq_nodes)
    if recency_scores:
        print("Recency Scores (Node ID -> Score):")
        for node_id, score in recency_scores.items():
            print(f"Node {node_id}: Recency Score = {score}")
    else:
        print("No recency scores available. Check if data is loaded properly.")

# Test extract_importance
def test_extract_importance():
    print("\n--- Testing Importance Extraction ---")
    importance_scores = extract_importance(memory_stream.seq_nodes)
    if importance_scores:
        print("Importance Scores (Node ID -> Score):")
        for node_id, score in importance_scores.items():
            print(f"Node {node_id}: Importance Score = {score}")
    else:
        print("No importance scores available. Check if nodes have importance values.")

# Test extract_relevance
def test_extract_relevance():
    print("\n--- Testing Relevance Extraction ---")
    relevance_scores = extract_relevance(memory_stream.seq_nodes, memory_stream.embeddings, "focal_point")
    if relevance_scores:
        print("Relevance Scores (Node ID -> Cosine Similarity):")
        for node_id, score in relevance_scores.items():
            print(f"Node {node_id}: Relevance (Cosine Similarity) = {score}")
    else:
        print("No relevance scores available. Ensure embeddings and focal points are correct.")

if __name__ == "__main__":
    print("Starting Tests for MemoryStream Functions...\n")

    # Test Recency Extraction
    test_extract_recency()

    # Test Importance Extraction
    test_extract_importance()

    # Test Relevance Extraction
    test_extract_relevance()

    print("\nAll tests completed.")
