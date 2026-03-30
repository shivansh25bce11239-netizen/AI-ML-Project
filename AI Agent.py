import re
import datetime
import random
import os
import sys

class UltimateAssistant:
    def __init__(self):
        self.task_file = "user_tasks.txt"
        self.log_file = "logs.txt"
        self.expense_file = "user_expenses.txt"
        self.last_math_result = 0
        self.tasks = []
        self.load_tasks()

        self.academic_help = {
            r'(fee|tuition|pay|cost|dues)': [
                "Tuition and hostel fees can be paid using the student portal.",
                "Fee payment deadlines for this semester are already provided in email. Check your email for dates."
            ],
            r'(course|register|enroll|credits)': [
                "Course registration opens two weeks before the semester starts.",
                "Advisor approval is needed for core courses."
            ],
            r'(grade|gpa|cgpa|marks|result)': [
                "Results are on the portal. Minimum CGPA is 6.0.",
                "Contact your professor for grade discrepancies within 48 hours."
            ],
            r'(exam|schedule|timetable|date)': [
                "Final exam schedules are released one month prior to exams."
            ],
            r'(password|login|access|account)': [
                "Use 'Forgot Password' with your university email to reset access."
            ]
        }

        self.it = {
            r'.*my (.*) is not working.*': "Have you tried restarting your {0} or checking its connection?",
            r'.*screen is (.*).*': "If your screen is {0}, try checking the display cable.",
            r'hello|hi': "Hello! I am your AI Assistant. How can I help?"
        }

    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, 'r') as f:
                self.tasks = [line.strip() for line in f.readlines()]

    def save_tasks(self):
        with open(self.task_file, 'w') as f:
            for task in self.tasks:
                f.write(task + "\n")

    def log_chat(self, user_given_input, bot_out):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] USER: {user_given_input} | AI: {bot_out}\n")

    def calculate_math(self, expression):
        expression = expression.replace("ans", str(self.last_math_result))
        expression = expression.replace("previous", str(self.last_math_result))
        
        expression = expression.replace("plus", "+").replace("add", "+")
        expression = expression.replace("minus", "-").replace("subtract", "-")
        expression = expression.replace("times", "*").replace("multiplied by", "*").replace("multiply", "*")
        expression = expression.replace("divided by", "/").replace("divide", "/").replace("over", "/")
        
        cleaned_expression = re.sub(r'[^0-9+\-*/().]', '', expression)
        try:
            if not cleaned_expression:
                return "No valid numbers found in your request."
            
            result = eval(cleaned_expression)
            self.last_math_result = result
            return str(result)
        except:
            return "Mathematical error. Please ensure the equation is valid."

    def save_expense(self, amount, item):
        with open(self.expense_file, 'a') as f:
            f.write(f"{datetime.datetime.now().ctime()} | Amount: {amount} | Item: {item}\n")

    def read_expenses(self):
        if not os.path.exists(self.expense_file):
            return "No expenses logged yet."
        with open(self.expense_file, 'r') as f:
            return "Your Expense Ledger:\n" + f.read()

    def process(self, user_input):
        text = user_input.lower().strip()

        if "time" in text:
            return datetime.datetime.now().strftime("It is currently %I:%M %p.")

        task_match = re.search(r'remind me to (.*)|add task (.*)', text)
        if task_match:
            t = task_match.group(1) if task_match.group(1) else task_match.group(2)
            self.tasks.append(t.strip())
            self.save_tasks()
            return f"Task '{t.strip()}' added to your planner."

        if "show tasks" in text or "my list" in text:
            if not self.tasks:
                return "Your task list is empty."
            return "Your Tasks:\n" + "\n".join([f"{i+1}. {x}" for i, x in enumerate(self.tasks)])

        math_match = re.search(r'calculate (.*)|what is (.*)|solve (.*)', text)
        if math_match:
            expression = next(g for g in math_match.groups() if g is not None)
            return f"The result is: {self.calculate_math(expression)}"

        for pattern, responses in self.academic_help.items():
            if re.search(pattern, text):
                return random.choice(responses)

        for pattern, response in self.it.items():
            match = re.search(pattern, text)
            if match:
                if '{0}' in response and match.groups():
                    return response.format(match.group(1))
                return response
            
        temp = re.sub(r'ans|previous|plus|minus|times|divided by|divide|over|add|subtract|multiplied by', '', text)
        leftovers = re.sub(r'[0-9\s\+\-\*\/\(\)]', '', temp)
        if leftovers == "" and len(text) > 0:
            return f"The result is: {self.calculate_math(text)}"
            
        expense_match = re.search(r'spent ([0-9]+) on (.*)|cost ([0-9]+) for (.*)', text)
        if expense_match:
            amt = expense_match.group(1) if expense_match.group(1) else expense_match.group(3)
            item = expense_match.group(2) if expense_match.group(2) else expense_match.group(4)
            self.save_expense(amt, item.strip())
            return f"Logged expense: {amt} for {item.strip()}."

        if "show expenses" in text or "show expenses" in text or "my ledger" in text:
            return self.read_expenses()

        sys_match = re.search(r'open (.*)|launch (.*)', text)
        if sys_match:
            app = next(g for g in sys_match.groups() if g is not None).strip()
            
            if "notepad" in app or "text" in app:
                if os.name == 'nt':
                    os.system("start notepad")
                elif sys.platform == "darwin":
                    os.system("open -a TextEdit")
                return "Launched Text Editor."
                
            elif "calculator" in app or "calc" in app:
                if os.name == 'nt':
                    os.system("start calc")
                elif sys.platform == "darwin":
                    os.system("open -a Calculator")
                return "Launched Calculator."
                
            return f"Cannot launch '{app}'. App not recognized or OS not supported."

        if "clear screen" in text or "cleaned_expression terminal" in text:
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Terminal cleared."

        return "I am an intro-level AI. I do not recognize that command or question."

    def run(self):
        print("===============================================")
        print("      AI Assistant & Academic Helpdesk    ")
        print("===============================================")
        print("Capabilities: Task Management | Math | IT Support | Academic Queries")
        print("Type 'exit' to quit and save logs.\n")
        
        while True:
            try:
                user_given_input = input("You: ")
                if not user_given_input:
                    continue
                if user_given_input.lower() in ['exit', 'quit', 'stop','bye']:
                    print("AI: Saving data. Shutting down.")
                    break
                    
                out = self.process(user_given_input)
                print(f"AI: {out}\n")
                self.log_chat(user_given_input, out)
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    UltimateAssistant().run()
