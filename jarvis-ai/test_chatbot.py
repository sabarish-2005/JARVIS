#!/usr/bin/env python3
"""
Test script for JARVIS AI chatbot functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai_brain import AIBrain

def test_chatbot():
    """Test the AI chatbot functionality"""
    print("🧪 Testing JARVIS AI Chatbot...")

    # Initialize AI Brain
    ai = AIBrain()

    # Test messages
    test_messages = [
        "Hello JARVIS, how are you?",
        "Tell me a joke",
        "What's the weather like today?",
        "Can you help me with Python programming?",
        "What time is it?",
        "Open notepad for me"
    ]

    print("\n" + "="*50)
    print("🤖 JARVIS AI CHATBOT TEST RESULTS")
    print("="*50)

    for i, message in enumerate(test_messages, 1):
        print(f"\n🗣️  Test {i}: '{message}'")
        print("-" * 40)

        try:
            response = ai.chat(message)
            print(f"🤖 JARVIS: {response}")
            print("✅ Success")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n" + "="*50)
    print("🎉 Chatbot testing completed!")
    print("="*50)

if __name__ == "__main__":
    test_chatbot()