# Zerenthis V2

Autonomous AI system that:
- Selects high-performing ideas from memory (leaderboard)
- Generates products from winning topics
- Runs full execution cycles (priority → product → revenue)
- Simulates traffic + conversions
- Reinforces winners through feedback loops

## Current Status
✅ Phase 1 COMPLETE  
- Intelligence Priority Engine  
- Topic Locking System  
- Product Generation Engine  
- Full-Cycle Pipeline  
- Revenue Loop (store + traffic + conversion + leaderboard)

## Core Loop
Run:
POST /api/revenue/run

System will:
1. Select best topic
2. Generate product
3. Simulate traffic
4. Generate revenue
5. Update leaderboard

## Architecture
backend/app/
- routes/
- engines/
- data/

## Safety
- Phase 1 locked snapshot (git tag)
- Clean baseline commit
- Fully reproducible system

## Next Phase
Phase 2: Real Traffic + External Feedback Integration

