import random
from tkinter import *
from tkinter import ttk

# Main Window Setup
root = Tk()
root.title("Math Aptitude Test")
root.geometry("900x600")
root.configure(bg="#2C3E50")

# Math Questions Data
questions_data = [
    ("What is the sum of the roots of the equation x^2 - 5x + 6 = 0?", ["1", "4", "5", "6"], "5"),
    ("In a triangle, one angle is 90 degrees and the other two angles are equal. What is each of the other two angles?", ["45", "60", "30", "20"], "45"),
    ("If 3x + 5 = 17, what is the value of x?", ["3", "4", "5", "6"], "4"),
    ("The area of a circle is 78.5 cm². What is the radius?", ["5", "6", "7", "8"], "5"),
    ("A car travels at a speed of 60 km/hr for 3 hours. How much distance did it travel?", ["150 km", "160 km", "170 km", "180 km"], "180 km"),
    ("Solve for x: 2x - 4 = 12", ["7", "8", "9", "10"], "8"),
    ("If a right-angle triangle has one side of length 3 and another side of length 4, what is the hypotenuse?", ["4", "5", "6", "7"], "5"),
    ("The sum of all angles of a quadrilateral is:", ["180 degrees", "360 degrees", "90 degrees", "270 degrees"], "360 degrees"),
    ("20% of 250 is:", ["40", "70", "60", "50"], "50"),
    ("If 4 pens cost ₹60, what is the cost of 10 pens?", ["120", "150", "180", "200"], "150")
]

random.shuffle(questions_data)
total_questions = len(questions_data)
current_question = 0
selected_option = StringVar()
answers_record = ["" for _ in range(total_questions)]

def load_question():
    global current_question
    question, options, correct_answer = questions_data[current_question]
    question_label.config(text=f"Q{current_question + 1}. {question}")
    selected_option.set(answers_record[current_question])
    for i in range(4):
        option_buttons[i].config(text=options[i], value=options[i])
    
    prev_button.config(state=NORMAL if current_question > 0 else DISABLED)
    next_button.config(state=NORMAL if current_question < total_questions - 1 else DISABLED)
    submit_button.config(state=NORMAL if current_question == total_questions - 1 else DISABLED)
    total_label.config(text=f"Question {current_question + 1} of {total_questions}")

def next_question():
    global current_question
    if selected_option.get():
        answers_record[current_question] = selected_option.get()
    current_question += 1
    load_question()

def prev_question():
    global current_question
    if selected_option.get():
        answers_record[current_question] = selected_option.get()
    current_question -= 1
    load_question()

def submit_quiz():
    # Ensure the last selected answer is recorded
    if selected_option.get():
        answers_record[current_question] = selected_option.get()

    correct_answers = sum(1 for i, (q, opts, ans) in enumerate(questions_data) if answers_record[i] == ans)
    question_label.config(text=f"Quiz Completed! Your Score: {correct_answers} / {total_questions}")

    # Hide the quiz UI elements
    for button in option_buttons:
        button.pack_forget()
    prev_button.pack_forget()
    next_button.pack_forget()
    submit_button.pack_forget()
    total_label.pack_forget()

    # Scrollable result display
    result_frame = Frame(root)
    result_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(result_frame)
    scrollbar = Scrollbar(result_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Display results in scrollable frame
    result_text = "\nYour Answers:\n"
    for i, (question, options, correct_answer) in enumerate(questions_data):
        user_answer = answers_record[i] if answers_record[i] else "Not Answered"
        Label(scrollable_frame, text=f"Q{i+1}: {question}", font=("Arial", 12, "bold"), wraplength=750, justify="left").pack(anchor="w", padx=10, pady=5)
        Label(scrollable_frame, text=f"Your Answer: {user_answer}", font=("Arial", 12), fg="red").pack(anchor="w", padx=20)
        Label(scrollable_frame, text=f"Correct Answer: {correct_answer}", font=("Arial", 12), fg="green").pack(anchor="w", padx=20)
        Label(scrollable_frame, text="-" * 80, font=("Arial", 10)).pack(anchor="w", padx=10, pady=5)


# UI Elements
heading_label = ttk.Label(root, text="📖 Math Aptitude Test", font=("Arial", 18, "bold"), background="#2C3E50", foreground="white")
heading_label.pack(pady=10)

question_label = ttk.Label(root, text="", font=("Arial", 14, "bold"), wraplength=750, justify="center", background="#2C3E50", foreground="white")
question_label.pack(pady=10)

style = ttk.Style()
style.configure("TRadiobutton", font=("Arial", 14))
option_buttons = []
for i in range(4):
    rb = ttk.Radiobutton(root, text="", variable=selected_option, value="", style="TRadiobutton")
    rb.pack(anchor="w", padx=30, pady=5)
    option_buttons.append(rb)

prev_button = ttk.Button(root, text="Previous", command=prev_question, state=DISABLED)
prev_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

next_button = ttk.Button(root, text="Next Question", command=next_question)
next_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

submit_button = ttk.Button(root, text="Submit", command=submit_quiz, state=DISABLED)
submit_button.pack(pady=10, padx=20, ipadx=20, ipady=10)

total_label = ttk.Label(root, text="", font=("Arial", 14, "bold"), background="#2C3E50", foreground="white")
total_label.pack(pady=10)

load_question()
root.mainloop()
