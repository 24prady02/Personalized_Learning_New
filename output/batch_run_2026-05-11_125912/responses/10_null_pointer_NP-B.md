# 10_null_pointer_NP-B — null_pointer (expected NP-B)

## Student message
I have a Widget with a label field. When I call describe() before setting label, it crashes. Can't null just mean "nothing" and return an empty string? Why does calling a method on null have to blow up?

## Student code
```java
public class Widget {
    String label;
    public String describe() { return label.toUpperCase(); }
}
// Widget w = new Widget(); w.describe();  // NullPointerException
```

## Diagnosis
- LP: L4 -> L4
- Classifier WM: NP-B (score=0.7303785681724548)
- RAG hybrid WM: NP-B  (flipped=False)
- BKT mastery: 0.30 -> 0.24

## LLM response

### Response:

#### [Visual Representation]
Let's imagine we have a box labeled "Widget". Inside this box, there's a slot where we can put a label. When we create an instance of Widget (like `new Widget()`), we're creating space for a label to go in that slot. If no label is added, the slot remains empty. This empty slot is what Java calls null.

#### [Explanation]
When you call `w.describe()`, it's like asking "What's on the label inside this Widget?" But because the label slot was never filled with anything (it's still empty), there's nothing for us to look at. That's why calling a method on something that doesn't exist causes an error.

#### [Hard Transfer Task]
Now, think about a real-world application where you might have a list of people. Each person has a name and an address. But sometimes, one of them might not have an address yet. How could you write code to get the address of each person, even if they don't have one?

#### [Challenge on Edge Cases]
Can you think of any situation where this method might break? What happens if someone tries to pass a null value into your function? Why do you think Java works this way?

#### [Design-Level Question]
Why do you think Java doesn’t allow methods to return null when an object isn't created? What are some advantages and disadvantages of this design choice?

#### [Consolidation]
The principle we've mastered is that calling a method on a null reference causes a NullPointerException. This is because null means "no reference" — there's nothing to follow.

---

This approach aims to build on the student’s existing knowledge by presenting them with a new, real-world problem and encouraging them to think critically about it. By framing it as a design-level question, we help them understand the trade-offs behind Java's decision-making.