"""
Test script to verify Groq API integration
"""

import os
import sys

def test_groq_integration():
    """Test Groq API integration"""
    
    print("="*80)
    print("Testing Groq API Integration")
    print("="*80)
    
    # Test 1: Check API key
    print("\n[1] Checking API Key...")
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        print("   [ERROR] GROQ_API_KEY environment variable not set!")
        print("   [INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    else:
        print("   [OK] API key found in environment")
    
    if not groq_api_key or len(groq_api_key) < 10:
        print("   [ERROR] Invalid API key!")
        return False
    
    print(f"   [OK] API key length: {len(groq_api_key)} characters")
    
    # Test 2: Initialize Groq client
    print("\n[2] Initializing Groq Client...")
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
        print("   [OK] Groq client initialized successfully")
    except Exception as e:
        print(f"   [ERROR] Error initializing Groq client: {e}")
        return False
    
    # Test 3: Test API call
    print("\n[3] Testing API Call...")
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Hello, Groq API is working!'"}],
            max_tokens=20,
            temperature=0.7
        )
        result = response.choices[0].message.content
        print(f"   [OK] API call successful!")
        print(f"   Response: {result}")
    except Exception as e:
        print(f"   [ERROR] Error making API call: {e}")
        return False
    
    # Test 4: Test ChatInterface initialization
    print("\n[4] Testing ChatInterface Initialization...")
    try:
        from chat_interface_simple import ChatInterface
        chat = ChatInterface(groq_api_key)
        print("   [OK] ChatInterface initialized successfully")
    except Exception as e:
        print(f"   [ERROR] Error initializing ChatInterface: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Test message processing
    print("\n[5] Testing Message Processing...")
    try:
        result = chat.process_message("What is recursion?")
        if result and 'response' in result:
            print("   [OK] Message processing successful!")
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Analysis keys: {list(result.get('analysis', {}).keys())}")
        else:
            print("   [ERROR] Invalid response format")
            return False
    except Exception as e:
        print(f"   [ERROR] Error processing message: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Test with code
    print("\n[6] Testing Code Processing...")
    try:
        code = "def factorial(n):\n    return n * factorial(n-1)"
        result = chat.process_message("Why does this fail?", code=code)
        if result and 'response' in result:
            print("   [OK] Code processing successful!")
            print(f"   Response length: {len(result['response'])} characters")
        else:
            print("   [ERROR] Invalid response format")
            return False
    except Exception as e:
        print(f"   [ERROR] Error processing code: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*80)
    print("SUCCESS: All Groq API Integration Tests Passed!")
    print("="*80)
    print("\nSummary:")
    print("   [OK] API key configured correctly")
    print("   [OK] Groq client initializes successfully")
    print("   [OK] API calls work correctly")
    print("   [OK] ChatInterface integrates with Groq")
    print("   [OK] Message processing works")
    print("   [OK] Code processing works")
    print("\nGroq API is fully integrated and working!")
    print("="*80)
    
    return True


if __name__ == "__main__":
    success = test_groq_integration()
    sys.exit(0 if success else 1)

