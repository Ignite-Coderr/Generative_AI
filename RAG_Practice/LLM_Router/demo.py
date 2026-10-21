"""
Demo Script for Intelligent Model Router

This script demonstrates the core routing functionality
without the Streamlit UI. Useful for testing and understanding
the routing logic.
"""

from app.router import IntelligentRouter
from app.model_runner import ModelRunner
from app.utils import format_routing_analysis


def demo_query(router: IntelligentRouter, query: str):
    """
    Demonstrate routing for a single query
    
    Args:
        router: IntelligentRouter instance
        query: Query string to route
    """
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    # Route the query
    result = router.route(query)
    
    # Display routing analysis
    print("\n" + format_routing_analysis(result['routing_analysis']))
    
    # Generate and display response
    print("\n" + "-"*80)
    print("MODEL RESPONSE:")
    print("-"*80)
    response = ModelRunner.run(result['selected_model'], query)
    print(response)
    
    print("\n" + "="*80 + "\n")


def main():
    """Main demo function"""
    
    print("\n" + "#"*80)
    print("#" + " "*26 + "INTELLIGENT MODEL ROUTER DEMO" + " "*25 + "#")
    print("#"*80 + "\n")
    
    # Initialize router
    print("Initializing router...")
    router = IntelligentRouter()
    
    # Demo queries
    demo_queries = [
        # Arithmetic queries
        "2 + 3",
        "Calculate 25 * 17",
        "What is 100 / 5?",
        
        # Mathematical queries
        "Solve the differential equation dy/dx = x^2",
        "Calculate the derivative of x^3 + 2x",
        "Find the integral of sin(x)",
        
        # Explanatory queries
        "Explain transformer architecture in detail",
        "What is reinforcement learning?",
        "Describe how neural networks work",
        "How does backpropagation work?",
        
        # Creative queries
        "Roast me",
        "Tell me a joke",
        "Be funny",
    ]
    
    print("\n" + "#"*80)
    print("# Running demo queries...")
    print("#"*80)
    
    for query in demo_queries:
        demo_query(router, query)
        
        # Pause between queries
        input("Press Enter to continue to next query...")
    
    print("\n" + "#"*80)
    print("#" + " "*31 + "DEMO COMPLETE" + " "*34 + "#")
    print("#"*80 + "\n")
    
    print("Summary:")
    print("- Tested 4 different model types")
    print("- Demonstrated embedding-based routing")
    print("- Showed intent detection and complexity analysis")
    print("\nFeel free to run this script again or use the Streamlit UI!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {str(e)}")
        import traceback
        traceback.print_exc()
