# Comprehensive Student Graph Visualization Guide

## Overview

This system generates comprehensive visual graphs for each student that show:
1. **DINA Mastery Evolution** - How understanding evolves over conversations
2. **CSE-KG Graph** - Computer Science Knowledge Graph visualization
3. **Pedagogical KG Graph** - Misconceptions and learning patterns
4. **COKE Cognitive Graph** - Cognitive states and behavioral responses
5. **Dynamic DINA Metrics Dashboard** - Real-time mastery metrics

## Generated Files

For each student conversation, the following visualizations are created:

### 1. Comprehensive Graphs (`comprehensive_graphs_sample_conversation_XX.png`)
- **DINA Mastery Heatmap**: Shows mastery evolution for all concepts across all turns
- **Overall Mastery Progression**: Line graph showing mastery changes over time
- **Mastery Delta**: Bar chart showing improvement/decline per turn
- **CSE-KG Graph**: Network visualization of CS concepts and relationships
- **Pedagogical KG Graph**: Misconceptions learned and their relationships
- **COKE Cognitive Graph**: Cognitive states and behavioral responses
- **DINA Metrics Dashboard**: Summary of current mastery metrics

### 2. Understanding Graphs (`understanding_graph_sample_conversation_XX.png`)
- Overall mastery progression
- Mastery delta per turn
- Concept-specific mastery trends
- Code correctness vs mastery correlation

### 3. Interactive Sessions (`interactive_session_sample_conversation_XX.md`)
- Detailed turn-by-turn analysis
- Student graph updates
- Metrics progression
- Misconceptions learned

## How to Generate Graphs

### Generate All Graphs for All Students
```bash
python scripts/generate_comprehensive_student_graphs.py
```

### Generate Graphs for Specific Conversation
```bash
python scripts/generate_comprehensive_student_graphs.py output/sample_conversation_01.json
```

### Generate Understanding Graphs Only
```bash
python scripts/generate_student_understanding_graph.py
```

### Generate Interactive Sessions
```bash
python generate_interactive_session.py
```

## Graph Components Explained

### 1. DINA Mastery Heatmap
- **X-axis**: Turn numbers
- **Y-axis**: Concepts
- **Colors**: 
  - Red = Low mastery (0.0-0.3)
  - Yellow = Moderate mastery (0.3-0.7)
  - Green = High mastery (0.7-1.0)
- **Purpose**: Visualize how mastery of each concept changes over time

### 2. Overall Mastery Progression
- Shows the student's overall mastery level across all turns
- Green dashed line = Mastery threshold (0.7)
- Orange dashed line = Learning threshold (0.5)
- Helps identify learning trends and plateaus

### 3. Mastery Delta
- Green bars = Improvement (positive delta)
- Red bars = Decline (negative delta)
- Gray bars = No change
- Shows the impact of each turn on mastery

### 4. CSE-KG Graph
- **Nodes**: CS concepts encountered in conversation
- **Edges**: Relationships (prerequisites, related concepts)
- **Layout**: Spring layout for readability
- Shows the knowledge structure the student is learning

### 5. Pedagogical KG Graph
- **Nodes**: Concepts (circles) and Misconceptions (squares)
- **Edges**: "has_misconception" relationships
- **Colors**:
  - Red = High severity misconceptions
  - Orange = Medium severity misconceptions
  - Blue = Low severity misconceptions
- Shows what misconceptions were learned and their impact

### 6. COKE Cognitive Graph
- **Purple nodes**: Cognitive states (perceiving, understanding, engaged, confused, frustrated)
- **Teal nodes**: Behavioral responses (continue, try_again, search_info, ask_question)
- **Edge width**: Confidence in the cognitive chain
- Shows the student's cognitive journey and predicted behaviors

### 7. DINA Metrics Dashboard
- Overall mastery score
- Mastery delta (change from previous turn)
- Strong areas (concepts with mastery >= 0.7)
- Weak areas (concepts with mastery < 0.5)
- Code correctness score
- Current cognitive state

## Dynamic Updates

The DINA metrics are **dynamically calculated** based on:
- **Code Correctness**: CodeBERT analysis of student code
- **Error Presence**: Whether errors occurred
- **Previous Mastery**: State from previous turns
- **Concept Performance**: Individual concept mastery changes

### Mastery Update Rules:
- **Good Performance** (correctness > 0.8): +0.05 mastery
- **Moderate Performance** (correctness 0.6-0.8): +0.02 mastery
- **Poor Performance** (correctness < 0.5) or Error: -0.03 mastery

## Best Practices

Based on research in knowledge graph visualization and DINA model best practices:

1. **Temporal Tracking**: All graphs show evolution over time
2. **Heatmaps**: Use color gradients to show mastery intensity
3. **Network Visualization**: Use spring layouts for readability
4. **Interactive Elements**: Color coding and legends for clarity
5. **Dashboard Summary**: Quick overview of current state

## File Locations

All generated graphs are saved in the `output/` directory:
- `comprehensive_graphs_sample_conversation_XX.png` - Full comprehensive graphs
- `understanding_graph_sample_conversation_XX.png` - Understanding progression
- `interactive_session_sample_conversation_XX.md` - Interactive session details

## Next Steps

1. Review the comprehensive graphs to understand each student's learning journey
2. Use the heatmaps to identify concepts that need reinforcement
3. Analyze the knowledge graphs to understand concept relationships
4. Track misconceptions to provide targeted interventions
5. Monitor cognitive states to adjust teaching strategies

## Technical Details

- **Graph Library**: NetworkX for graph operations
- **Visualization**: Matplotlib for plotting
- **Layout Algorithm**: Spring layout for network graphs
- **Color Schemes**: ColorBrewer-inspired palettes
- **Resolution**: 300 DPI for high-quality output

