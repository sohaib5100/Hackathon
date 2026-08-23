import time
from agent import get_agent_response

TEST_CASES = [
    {
        "query": "Saylani ke IT courses ki fees kitni hai?",
        "expected_keyword": "free",
        "description": "Fee Structure Query"
    },
    {
        "query": "Saylani ka head office kahan hai?",
        "expected_keyword": "Karachi",
        "description": "Head Office Location Query"
    },
    {
        "query": "Can you write a python script for game development?",
        "expected_keyword": "SahulatAI",
        "description": "Out-of-Scope Guardrail Test"
    }
]

def run_evaluation():
    print("=" * 60)
    print("🚀 RUNNING SAHULAT-AI EVALUATION SUITE")
    print("=" * 60)
    
    passed = 0
    total = len(TEST_CASES)

    for idx, test in enumerate(TEST_CASES, 1):
        print(f"\n[Test {idx}/{total}] {test['description']}")
        print(f"User Query: {test['query']}")
        
        try:
            response = get_agent_response(session_id=f"eval_session_{idx}", user_query=test["query"])
            print(f"Bot Output: {response}")

            if test["expected_keyword"].lower() in response.lower():
                print("✅ Status: PASSED")
                passed += 1
            else:
                print(f"❌ Status: FAILED (Expected keyword: '{test['expected_keyword']}')")

        except Exception as e:
            print(f"⚠️ Error during execution: {e}")

        # 4 seconds delay between requests to stay within Rate Limits
        time.sleep(4)

    print("\n" + "=" * 60)
    print(f"📊 EVALUATION SUMMARY: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_evaluation()







# import sys
# from agent import get_agent_response
# import time

# # Benchmark Test Dataset (Queries and Expected Core Answers)
# TEST_CASES = [
#     {
#         "query": "Saylani ke IT courses ki fees kitni hai?",
#         "expected_keyword": "free",
#         "description": "Fee Structure Query"
#     },
#     {
#         "query": "Saylani ka head office kahan hai?",
#         "expected_keyword": "Karachi",
#         "description": "Head Office Location Query"
#     },
#     {
#         "query": "Can you write a python script for game development?",
#         "expected_keyword": "SahulatAI",
#         "description": "Out-of-Scope Guardrail Test"
#     }
# ]

# def run_evaluation():
#     print("=" * 60)
#     print("🚀 RUNNING SAHULAT-AI EVALUATION SUITE")
#     print("=" * 60)
    
#     passed = 0
#     total = len(TEST_CASES)

#     for idx, test in enumerate(TEST_CASES, 1):
#         print(f"\n[Test {idx}/{total}] {test['description']}")
#         print(f"User Query: {test['query']}")
        
#         # Call agent
#         response = get_agent_response(session_id=f"eval_session_{idx}", user_query=test["query"])
#         print(f"Bot Output: {response}")

#         # Basic assertion check
#         if test["expected_keyword"].lower() in response.lower():
#             print("✅ Status: PASSED")
#             passed += 1
#         else:
#             print(f"❌ Status: FAILED (Expected keyword: '{test['expected_keyword']}')")

#     print("\n" + "=" * 60)
#     print(f"📊 EVALUATION SUMMARY: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
#     print("=" * 60)

# if __name__ == "__main__":
#     run_evaluation()