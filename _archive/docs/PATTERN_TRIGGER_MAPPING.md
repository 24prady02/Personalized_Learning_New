# Complete Pattern → Strategy Trigger Mapping

## 🎯 Pattern Triggers Strategy: Complete Reference

This document shows **exactly which patterns trigger which personalization strategies**.

---

## 📊 Pattern 1: EMOTION PATTERNS

### Pattern: **High Frustration** (`frustration_level > 0.7`)

**Detected by:** Behavioral RNN

**Triggers:**
- ✅ **Feature 2 (Emotional Intelligence)**
  - Tone: `gentle_supportive`
  - Encouragement level: `high`
  - Step size: `small`
  - Reassurance needed: `True`
  
- ✅ **Feature 8 (Error Feedback)**
  - Hint level: `explicit` (more direct help)
  
- ✅ **Feature 9 (Metacognitive)**
  - Strategy type: `self_regulation`
  - Tips: ["Take a break", "Explain out loud", "Start simpler"]
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Pacing: `slower`
  - Scaffolding: `increased`

---

### Pattern: **Low Engagement** (`engagement_score < 0.4`)

**Detected by:** Behavioral RNN

**Triggers:**
- ✅ **Feature 2 (Emotional Intelligence)**
  - Tone: `enthusiastic_engaging`
  - Encouragement level: `high`
  - Message: "Be more enthusiastic, use interesting examples"
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Pacing: `faster` (speed up to maintain interest)

---

### Pattern: **Confused but Trying** (`emotion == 'confused' && engagement > 0.5`)

**Detected by:** Behavioral RNN

**Triggers:**
- ✅ **Feature 2 (Emotional Intelligence)**
  - Tone: `supportive_clarifying`
  - Step size: `small`
  - Message: "Be supportive, provide clear step-by-step explanation"

---

### Pattern: **High Achievement** (`mastery > 0.7 && mastery_change > 0.1`)

**Detected by:** Behavioral RNN + BKT

**Triggers:**
- ✅ **Feature 2 (Emotional Intelligence)**
  - Tone: `celebratory`
  - Celebration needed: `True`
  - Message: "Celebrate their progress!"
  
- ✅ **Feature 5 (Progress-Aware)**
  - Acknowledgment needed: `True`
  - Acknowledgment message: "Great progress! Mastery improved from X% to Y%!"

---

## 📊 Pattern 2: LEARNING STYLE PATTERNS

### Pattern: **Visual Learner** (`learning_preference == 'visual'`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 3 (Learning Style)**
  - Content format: `['diagrams', 'visual_metaphors', 'step_by_step_visual']`
  - Explanation approach: `"Use visual analogies and diagrams. 'Imagine it like...'"`
  - Visual elements: `True`
  - Instructions: "Include ASCII diagrams, flowcharts, visual representations"
  
- ✅ **Feature 7 (Format Preferences)**
  - Visual density: `high`

---

### Pattern: **Conceptual Learner** (`learning_preference == 'conceptual'`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 3 (Learning Style)**
  - Content format: `['why_explanations', 'connections', 'mental_models']`
  - Explanation approach: `"Explain WHY, not just HOW. Connect to other concepts."`
  - Instructions: "Focus on 'why' questions. Explain underlying principles. Connect to related concepts."

---

### Pattern: **Practical/Active Learner** (`learning_preference == 'practical'`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 3 (Learning Style)**
  - Content format: `['hands_on_examples', 'interactive_exercises', 'try_it_now']`
  - Explanation approach: `"Provide hands-on examples. 'Try this now...'"`
  - Instructions: "Include hands-on examples. Provide 'try it now' prompts. Show real-world applications."

---

### Pattern: **Sequential Learner** (`'sequential' in learning_style`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 3 (Learning Style)**
  - Content format: `['numbered_steps', 'linear_progression', 'clear_sequence']`
  - Explanation approach: `"Use numbered steps. 'First... then... finally...'"`
  - Instructions: "Use numbered steps. Clear linear progression. 'First, then, finally' structure."

---

## 📊 Pattern 3: PERSONALITY TRAIT PATTERNS

### Pattern: **High Neuroticism** (`neuroticism > 0.6`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 4 (Personality Communication)**
  - Reassurance level: `high`
  - Communication style: `supportive_reassuring`
  - Instructions: "Provide extra reassurance. Normalize struggles. Break into smaller steps. Frequent check-ins."

---

### Pattern: **High Openness** (`openness > 0.7`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 4 (Personality Communication)**
  - Communication style: `exploratory`
  - Instructions: "Explore connections to other concepts. Mention advanced topics. Use creative examples."
  
- ✅ **Feature 7 (Format Preferences)**
  - Length: `detailed` (more detailed explanations)

---

### Pattern: **High Conscientiousness** (`conscientiousness > 0.7`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 4 (Personality Communication)**
  - Structure level: `high`
  - Communication style: `structured_organized`
  - Instructions: "Use structured format. Clear organization. Detailed notes. Numbered sections."
  
- ✅ **Feature 7 (Format Preferences)**
  - Structure: `structured`

---

### Pattern: **High Extraversion** (`extraversion > 0.6`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 4 (Personality Communication)**
  - Engagement style: `high`
  - Communication style: `conversational_engaging`
  - Instructions: "Use conversational tone. Engaging questions. Interactive elements. More enthusiasm."

---

### Pattern: **High Agreeableness** (`agreeableness > 0.7`)

**Detected by:** Nestor

**Triggers:**
- ✅ **Feature 4 (Personality Communication)**
  - Communication style: `collaborative`
  - Instructions: "Use collaborative language. 'Let's work together...' 'We can...'"

---

## 📊 Pattern 4: MASTERY PATTERNS

### Pattern: **Low Mastery** (`mastery < 0.3`)

**Detected by:** BKT/DINA

**Triggers:**
- ✅ **Feature 5 (Progress-Aware)**
  - Challenge level: `foundational`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty level: `foundational`
  - Scaffolding level: `5` (high support)
  - Challenge type: `building_foundation`
  - Instructions: "Use foundational concepts. High scaffolding. Small steps."

---

### Pattern: **Building Mastery** (`0.3 <= mastery < 0.6`)

**Detected by:** BKT/DINA

**Triggers:**
- ✅ **Feature 5 (Progress-Aware)**
  - Challenge level: `building`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty level: `building`
  - Scaffolding level: `3` (moderate)
  - Challenge type: `just_right`
  - Instructions: "Build on existing knowledge. Moderate scaffolding."

---

### Pattern: **Reinforcing Mastery** (`0.6 <= mastery < 0.8`)

**Detected by:** BKT/DINA

**Triggers:**
- ✅ **Feature 5 (Progress-Aware)**
  - Challenge level: `reinforcing`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty level: `reinforcing`
  - Scaffolding level: `2` (lower)
  - Challenge type: `reinforcement`
  - Instructions: "Reinforce understanding. Lower scaffolding. More independence."

---

### Pattern: **High Mastery** (`mastery >= 0.8`)

**Detected by:** BKT/DINA

**Triggers:**
- ✅ **Feature 5 (Progress-Aware)**
  - Challenge level: `mastery`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty level: `mastery`
  - Scaffolding level: `1` (minimal)
  - Challenge type: `extension`
  - Instructions: "Extend to advanced concepts. Minimal scaffolding. Challenge them."

---

### Pattern: **Significant Improvement** (`mastery_change > 0.15`)

**Detected by:** BKT

**Triggers:**
- ✅ **Feature 5 (Progress-Aware)**
  - Acknowledgment needed: `True`
  - Acknowledgment: `"Great progress! Mastery improved from X% to Y%!"`

---

### Pattern: **Improving Trajectory** (`mastery_history[-1] > mastery_history[-2]`)

**Detected by:** BKT

**Triggers:**
- ✅ **Feature 1 (Conversation Memory)**
  - Learning trajectory: `"Mastery is improving"`
  
- ✅ **Feature 9 (Metacognitive)**
  - Strategy type: `incremental_questioning`
  - Message: "Your incremental questioning approach is working great!"
  - Tips: ["Break complex topics into smaller questions", "Ask 'why' and 'how'"]

---

## 📊 Pattern 5: ERROR PATTERNS

### Pattern: **Error Detected** (`code_analysis.errors`)

**Detected by:** Code Analysis

**Triggers:**
- ✅ **Feature 8 (Error Feedback)**
  - Has errors: `True`
  - Error type: `[detected error type]`
  - Error location: `[detected line]`
  - Error issue: `[detected issue]`
  - Error fix: `[suggested fix]`
  - Hint level: `explicit` if frustration > 0.7, else `moderate`

---

### Pattern: **High Severity Error** (`error_severity == 'high'`)

**Detected by:** Code Analysis

**Triggers:**
- ✅ **Feature 8 (Error Feedback)**
  - Hint level: `explicit` (always explicit for high severity)
  - Priority: `high`

---

## 📊 Pattern 6: BEHAVIORAL PATTERNS

### Pattern: **Repeated Confusion** (`confusion_count > 2`)

**Detected by:** Conversation History

**Triggers:**
- ✅ **Feature 1 (Conversation Memory)**
  - Confusion patterns: `["Student has asked about this concept multiple times", "May need alternative explanation approach"]`
  
- ✅ **Feature 9 (Metacognitive)**
  - Strategy type: `systematic_tracing`
  - Message: "Try this systematic approach:"
  - Tips: ["Draw it out on paper", "Trace through with specific values", "Check understanding at each step"]

---

### Pattern: **Struggling with Concept** (`mastery < 0.4 && interaction_count > 1`)

**Detected by:** BKT + Conversation History

**Triggers:**
- ✅ **Feature 9 (Metacognitive)**
  - Strategy type: `systematic_tracing`
  - Message: "Try this systematic approach:"
  - Tips: ["Draw it out on paper", "Trace through with specific values", "Check understanding at each step"]

---

### Pattern: **What Worked Before** (`previous_intervention_was_helpful`)

**Detected by:** Conversation History

**Triggers:**
- ✅ **Feature 1 (Conversation Memory)**
  - What worked before: `[list of effective interventions]`
  
- ✅ **Feature 3 (Learning Style)**
  - Uses same approach that worked before
  - Example: If `visual_explanation` worked → use visual content again

---

## 📊 Pattern 7: CODE QUALITY PATTERNS

### Pattern: **Shows Understanding** (`code_analysis.shows_understanding == True`)

**Detected by:** Code Analysis

**Triggers:**
- ✅ **Feature 5 (Progress)**
  - BKT evidence boost: `+0.1` (increases mastery estimate)
  
- ✅ **Feature 7 (Format Preferences)**
  - Code style: `commented` (match their style)

---

### Pattern: **Has Errors** (`code_analysis.has_errors == True`)

**Detected by:** Code Analysis

**Triggers:**
- ✅ **Feature 5 (Progress)**
  - BKT evidence adjustment: `-0.05` (slight decrease)
  
- ✅ **Feature 8 (Error Feedback)**
  - Error feedback provided

---

## 📊 Pattern 8: INTERACTION PATTERNS

### Pattern: **Multiple Interactions** (`interaction_count >= 3`)

**Detected by:** Conversation History

**Triggers:**
- ✅ **Feature 1 (Conversation Memory)**
  - References previous topics
  - Tracks learning trajectory
  
- ✅ **Feature 9 (Metacognitive)**
  - Can provide strategy tips based on history

---

### Pattern: **Previous Topics Discussed** (`previous_topics`)

**Detected by:** Conversation History

**Triggers:**
- ✅ **Feature 1 (Conversation Memory)**
  - References: `"Last time you asked about X, now you're building on that..."`

---

## 📊 Pattern 9: KNOWLEDGE GAP PATTERNS

### Pattern: **Critical Knowledge Gap** (`gap_severity > 0.8`)

**Detected by:** DINA/BKT

**Triggers:**
- ✅ **Feature 5 (Progress)**
  - Challenge level: `foundational` (if gap is blocking)
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty: `foundational`
  - Scaffolding: `5` (high)
  - Challenge type: `building_foundation`

---

### Pattern: **Missing Prerequisites** (`missing_prerequisites == True`)

**Detected by:** CSE-KG + DINA

**Triggers:**
- ✅ **Feature 5 (Progress)**
  - Challenge level: `foundational`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Difficulty: `foundational`
  - Scaffolding: `5`

---

## 📊 Pattern 10: ENGAGEMENT PATTERNS

### Pattern: **Quick Response** (`response_time < 5 seconds`)

**Detected by:** Behavioral RNN

**Triggers:**
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Pacing: `faster` (student is ready for more)

---

### Pattern: **Declining Engagement** (`engagement_trend == 'declining'`)

**Detected by:** Behavioral RNN

**Triggers:**
- ✅ **Feature 2 (Emotional Intelligence)**
  - Tone: `enthusiastic_engaging`
  - Encouragement: `high`
  
- ✅ **Feature 10 (Difficulty & Pacing)**
  - Pacing: `faster` (speed up to recapture interest)

---

## 📋 Complete Trigger Matrix

| Pattern | Detected By | Triggers Features | Strategy Applied |
|---------|-------------|-------------------|------------------|
| **High Frustration** | Behavioral RNN | 2, 8, 9, 10 | Gentle tone, explicit hints, self-regulation, slower pacing |
| **Low Engagement** | Behavioral RNN | 2, 10 | Enthusiastic tone, faster pacing |
| **Confused but Trying** | Behavioral RNN | 2 | Supportive clarifying tone, small steps |
| **High Achievement** | Behavioral RNN + BKT | 2, 5 | Celebratory tone, progress acknowledgment |
| **Visual Learner** | Nestor | 3, 7 | Diagrams, visual metaphors, high visual density |
| **Conceptual Learner** | Nestor | 3 | Why explanations, connections, mental models |
| **Practical Learner** | Nestor | 3 | Hands-on examples, interactive exercises |
| **Sequential Learner** | Nestor | 3 | Numbered steps, linear progression |
| **High Neuroticism** | Nestor | 4 | Extra reassurance, supportive tone, small steps |
| **High Openness** | Nestor | 4, 7 | Exploratory style, detailed explanations |
| **High Conscientiousness** | Nestor | 4, 7 | Structured format, organized content |
| **High Extraversion** | Nestor | 4 | Conversational tone, engaging questions |
| **High Agreeableness** | Nestor | 4 | Collaborative language |
| **Low Mastery** | BKT/DINA | 5, 10 | Foundational difficulty, high scaffolding |
| **Building Mastery** | BKT/DINA | 5, 10 | Building difficulty, moderate scaffolding |
| **Reinforcing Mastery** | BKT/DINA | 5, 10 | Reinforcing difficulty, lower scaffolding |
| **High Mastery** | BKT/DINA | 5, 10 | Mastery difficulty, minimal scaffolding |
| **Significant Improvement** | BKT | 5 | Progress acknowledgment, celebration |
| **Improving Trajectory** | BKT | 1, 9 | Learning trajectory tracking, incremental questioning tips |
| **Error Detected** | Code Analysis | 8 | Specific error feedback, exact location |
| **High Severity Error** | Code Analysis | 8 | Explicit hints, high priority |
| **Repeated Confusion** | Conversation History | 1, 9 | Alternative explanation, systematic tracing |
| **Struggling with Concept** | BKT + History | 9 | Systematic tracing strategy |
| **What Worked Before** | Conversation History | 1, 3 | Use same approach, reference previous success |
| **Shows Understanding** | Code Analysis | 5, 7 | BKT evidence boost, match code style |
| **Has Errors** | Code Analysis | 5, 8 | BKT evidence adjustment, error feedback |
| **Multiple Interactions** | Conversation History | 1, 9 | Reference history, provide strategy tips |
| **Previous Topics** | Conversation History | 1 | Reference previous conversations |
| **Critical Knowledge Gap** | DINA/BKT | 5, 10 | Foundational teaching, high scaffolding |
| **Missing Prerequisites** | CSE-KG + DINA | 5, 10 | Foundational difficulty, high scaffolding |
| **Quick Response** | Behavioral RNN | 10 | Faster pacing |
| **Declining Engagement** | Behavioral RNN | 2, 10 | Enthusiastic tone, faster pacing |

---

## 🎯 Pattern Combination Examples

### Example 1: Frustrated Visual Learner with Low Mastery

**Patterns Detected:**
- High frustration (0.75)
- Visual learner
- Low mastery (0.25)

**Strategies Triggered:**
- Feature 2: Gentle, supportive tone
- Feature 3: Visual diagrams and metaphors
- Feature 5: Foundational challenge level
- Feature 8: Explicit error hints
- Feature 10: High scaffolding (5/5), slower pacing

---

### Example 2: Engaged Conceptual Learner with Improving Mastery

**Patterns Detected:**
- High engagement (0.85)
- Conceptual learner
- Significant improvement (+0.20)

**Strategies Triggered:**
- Feature 2: Celebratory tone
- Feature 3: Why explanations, connections
- Feature 5: Progress acknowledgment
- Feature 10: Faster pacing (ready for more)

---

### Example 3: Confused High Neuroticism Student with Error

**Patterns Detected:**
- Confused emotion
- High neuroticism (0.70)
- Error detected

**Strategies Triggered:**
- Feature 2: Supportive clarifying tone, small steps
- Feature 4: Extra reassurance, normalize struggles
- Feature 8: Explicit error feedback
- Feature 10: Slower pacing, high scaffolding

---

## ✅ Summary

**Every personalization strategy is triggered by specific patterns!**

- **30+ patterns** detected by learned models
- **Each pattern** triggers **1-4 personalization features**
- **Multiple patterns** can trigger **multiple strategies** simultaneously
- **Pattern combinations** create **highly personalized** responses

**The system is completely pattern-driven!** 🎯

















