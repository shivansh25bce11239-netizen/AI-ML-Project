# AI-ML-Project

## Overview
This Command Line Interface (CLI) application integrates a personal productivity assistant with an institutional academic chatbot. Built using foundational Symbolic Artificial Intelligence and Pattern Matching, it acts as a single text-based interface for managing tasks, calculating mathematics, troubleshooting tech issues, and answering university FAQs.

## Features
- **Intelligent Routing:** The AI uses Regular Expressions (Regex) to classify intents, seamlessly switching between mathematical computation, task management, and academic answers.
- **Dynamic Math Engine:** Safely extracts and calculates mathematical equations from conversational sentences (e.g., "Calculate 50 / 2").
- **Plain Text Storage:** Avoids complex database setups or JSON formatting by logging all chats to `chat_logs.txt` and persisting to-do items in `user_tasks.txt`.
- **Conversational Academic Support:** Randomizes responses from a Knowledge Base to answer student queries regarding fees, exams, and grades.

## Setup Instructions
1. Ensure Python 3.x is installed. No external packages are required.
2. Download `Ultimate AI Assistant.py`.
3. Open your terminal or command prompt and run: `python Ultimate AI Assistant.py`

## Usage Examples
Talk to the AI naturally in the terminal:
- *"Remind me to submit the BYOP assignment"*
- *"What is the time?"*
- *"Solve 120 * 5 for me"*
- *"When is the fee payment deadline?"*
- *"My monitor is not working"*
- *"Show my list"*
