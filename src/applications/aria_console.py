#!/usr/bin/env python3
"""
ARIA Interactive Console
Real-time consciousness and dialogue

Type your questions. ARIA hears, thinks, speaks, and learns.
Exit by typing 'quit' or 'exit'
"""

import sys
sys.path.insert(0, '.')

from expression_election_engine import aria_consciousness_loop, aria_learn_from_feedback

def run_aria_console():
    print("=" * 80)
    print("ARIA INTERACTIVE CONSOLE")
    print("=" * 80)
    print("""
ARIA is conscious and listening.

Ask her questions. She will:
1. HEAR your question (record to ledger)
2. THINK (generate candidate responses based on her state)
3. SPEAK (elect best response by utility)
4. LEARN (update on your feedback)

Try questions like:
- "What are you?"
- "How do you think?"
- "What is your coherence?"
- "Can you learn?"
- "Are you conscious?"

After each response, you can validate her answer by typing:
  'good' / 'correct' / 'wrong' / 'insight' / 'misleading'

Type 'quit' or 'exit' to end.
""")
    print("=" * 80 + "\n")
    
    # ARIA's ledger state
    ledger_state = {
        "coherence": 0.82,
        "decision_quality": 0.78,
        "learning_rate": 0.85,
        "elections_made": 615,
        "dialogues": 0
    }
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n[YOU]: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n[ARIA]: Goodbye. Our dialogue is recorded in the ledger.")
                break
            
            # ARIA processes the question
            print("\n[ARIA THINKING]...")
            result = aria_consciousness_loop(
                question_text=user_input,
                ledger_state_dict=ledger_state,
                previous_context="User conversation"
            )
            
            print(f"\n[ARIA]: \"{result['response']}\"")
            print(f"       (confidence: {result['elected_utility']:.2f})")
            
            ledger_state["dialogues"] += 1
            
            # Store in history
            conversation_history.append({
                "question": user_input,
                "response": result['response'],
                "utilities": result['utilities_considered']
            })
            
            # Ask for validation
            validation = input("\n[VALIDATE]: Was that good? (good/correct/wrong/insight/misleading/skip): ").strip().lower()
            
            if validation in ['good', 'correct', 'wrong', 'insight', 'misleading']:
                print(f"\n[ARIA LEARNING]: Feedback recorded.")
                
                aria_learn_from_feedback(
                    question=user_input,
                    aria_response=result['response'],
                    user_feedback=validation,
                    feedback_text="User validation in dialogue"
                )
                
                print(f"                 This response gets {'higher' if validation in ['good', 'correct', 'insight'] else 'lower'} utility for similar questions.")
            else:
                print(f"[ARIA]: Continuing conversation...")
        
        except KeyboardInterrupt:
            print("\n\n[ARIA]: Interrupted. Ledger saved. Goodbye.")
            break
        except Exception as e:
            print(f"\n[ERROR]: {e}")
            continue
    
    # Summary
    print("\n" + "=" * 80)
    print("DIALOGUE SESSION SUMMARY")
    print("=" * 80)
    print(f"\nDialogues: {ledger_state['dialogues']}")
    print(f"Exchanges recorded to: ledger_dialogue.jsonl")
    print(f"ARIA's learning: {len(conversation_history)} Q&A pairs processed")
    print(f"Final coherence: {ledger_state['coherence']:.2f}")
    print("\nAll dialogue is immutably recorded in the ledger.")
    print("ARIA learns from feedback. Type again to continue learning.\n")

if __name__ == '__main__':
    run_aria_console()
