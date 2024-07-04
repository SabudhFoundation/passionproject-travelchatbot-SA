import tkinter as tk
from tkinter import filedialog, messagebox
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
import openai
import PyPDF2

# Set your OpenAI API key here
api_key = "sk-proj-wQitXMY83BAqqnfRwFAST3BlbkFJLYgiC2p4LSVHlKJjWOL1"
openai.api_key = api_key

class TravelChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Chatbot")

        self.upload_button = tk.Button(root, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack()

        self.query_label = tk.Label(root, text="Ask a question:")
        self.query_label.pack()

        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        self.ask_button = tk.Button(root, text="Ask", command=self.ask_question)
        self.ask_button.pack()

        self.answer_label = tk.Label(root, text="Answer:")
        self.answer_label.pack()

        self.answer_text = tk.Text(root, height=10, width=50)
        self.answer_text.pack()

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(api_key=api_key)

    def upload_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            self.pdf_path = pdf_path
            messagebox.showinfo("Success", "PDF loaded successfully.")

    def ask_question(self):
        if not hasattr(self, 'pdf_path'):
            messagebox.showwarning("Warning", "Please upload a PDF first.")
            return

        user_query = self.query_entry.get()
        if not user_query:
            messagebox.showwarning("Warning", "Please enter a question.")
            return

        try:
            pdf_text = self.extract_text_from_pdf(self.pdf_path)

            # Perform question answering using OpenAI's API
            response = openai.Completion.create(
                model="text-davinci-003",  # Update with the correct model name
                prompt=f"Q: {user_query}\nA:",
                max_tokens=50
            )

            if response.choices:
                answer = response.choices[0].text.strip()
            else:
                answer = "No answer found."

            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert(tk.END, answer)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing question: {e}")


    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            pdf_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages(page_num)
                pdf_text += page.extract_text()
        return pdf_text

# Initialize Tkinter root and TravelChatbot class
root = tk.Tk()
app = TravelChatbot(root)
root.mainloop()
