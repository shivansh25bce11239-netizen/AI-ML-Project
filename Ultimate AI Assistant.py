import re
import datetime
import random
import os

class UltimateAssistant:
    def __init__(self):
        self.task_file = "user_tasks.txt"
        self.log_file = "logs.txt"
        self.tasks = []
        self.load_tasks()

        self.academic_help = {
            r'(fee|tuition|pay|cost|dues)': [
                "Tuition and hostel fees can be paid using the student portal.",
                "Fee payment deadlines for this semester are already provided in email. Check your email for dates."
            ],
            r'(course|register|enroll|credits)': [
                "Course registration opens two weeks prior to the semester.",
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

    def log_chat(self, user_in, bot_out):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] USER: {user_in} | AI: {bot_out}\n")

    def calculate_math(self, expr):
        clean = re.sub(r'[^0-9+\-*/().]', '', expr)
        try:
            if not clean:
                return "No valid numbers found in your request."
            return str(eval(clean))
        except:
            return "Mathematical error. Please ensure the equation is valid."

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
            expr = next(g for g in math_match.groups() if g is not None)
            return f"The result is: {self.calculate_math(expr)}"

        for pattern, responses in self.academic_kb.items():
            if re.search(pattern, text):
                return random.choice(responses)

        for pattern, response in self.it_kb.items():
            match = re.search(pattern, text)
            if match:
                if '{0}' in response and match.groups():
                    return response.format(match.group(1))
                return response

        return "I am an intro-level AI. I do not recognize that command or question."

    def run(self):
        print("===============================================")
        print("      AI Assistant & Academic Helpdesk    ")
        print("===============================================")
        print("Capabilities: Task Management | Math | IT Support | Academic Queries")
        print("Type 'exit' to quit and save logs.\n")
        
        while True:
            try:
                user_in = input("You: ")
                if not user_in:
                    continue
                if user_in.lower() in ['exit', 'quit', 'stop','bye']:
                    print("AI: Saving data. Shutting down.")
                    break
                    
                out = self.process(user_in)
                print(f"AI: {out}\n")
                self.log_chat(user_in, out)
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    UltimateAssistant().run()

