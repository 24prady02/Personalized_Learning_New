# 02_type_mismatch_TM-B — type_mismatch (expected TM-B)

## Student message
I thought + would just combine an int and a string into one string the way Python does. Why won't Java do this automatically? It worked fine when I tested it in Python.

## Student code
```java
int score = 100;
String msg = "Score: " + score + 5;
// expected "Score: 105" but got "Score: 1005"
```

## Diagnosis
- LP: L2 -> L3
- Classifier WM: TM-A (score=0.75)
- RAG hybrid WM: TM-B  (flipped=True)
- BKT mastery: 0.20 -> 0.23

## LLM response

It seems like there was a misunderstanding when you asked me about your code, but I don't see any code or question attached to your message. Could you please provide more details so we can move forward with your learning?