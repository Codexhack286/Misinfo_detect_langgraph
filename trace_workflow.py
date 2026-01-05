from graph import graph
import sys

def test_workflow_trace(headline_text="The moon is made of green cheese"):
    """
    Runs the graph with a specific input and prints the execution path
    by streaming the output from the graph.
    """
    print(f"\n🚀 Starting Workflow Trace")
    print(f"📝 Input Claim: '{headline_text}'\n")
    print("-" * 50)

    state = {
        "article_text": headline_text, # Using headline as article text for simplicity
        "headline": "" 
    }

    step_count = 1
    
    # Stream the graph execution to see each step
    try:
        # stream() yields dictionaries where keys are node names and values are state updates
        for output in graph.stream(state):
            for node_name, state_update in output.items():
                print(f"[{step_count}] 🛠️  Node Executed: {node_name}")
                
                # specific logging based on node
                if node_name == "extract":
                    print(f"   └── Extracted Headline: {state_update.get('headline')}")
                elif node_name == "search":
                    print(f"   └── Search performed. Results count: {len(state_update.get('search_results', []))}")
                elif node_name == "fact_check":
                    verdict = state_update.get('verdict')
                    print(f"   └── Fact Check Result: {verdict}")
                    if verdict == "UNCERTAIN":
                        print("   ⚠️  Triggering Fallback Logic...")
                elif node_name == "perplexity_check":
                    print(f"   └── Perplexity Verdict: {state_update.get('verdict')}")
                    print(f"   └── Summary: {state_update.get('summary')}")
                elif node_name == "summary":
                    print(f"   └── Final Summary generated.")
                elif node_name == "alternatives":
                    print(f"   └── Alternatives fetched.")
                
                print("-" * 50)
                step_count += 1
                
        print("\n✅ Workflow Completed Successfully.")
        
    except Exception as e:
        print(f"\n❌ Workflow Error: {e}")

if __name__ == "__main__":
    # You can pass a command line argument for custom text
    text = sys.argv[1] if len(sys.argv) > 1 else "The moon is made of green cheese"
    test_workflow_trace(text)
