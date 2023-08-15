import openai
import os
import tkinter as tk
from tkinter import filedialog
import pdfminer
from pdfminer.high_level import extract_text

# Set the OpenAI API key
openai.api_key = "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"

def finalSummary_gpt(text):
    completions = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        temperature=0.7,
        max_tokens=3000,
        messages = [
            {"role": "system", "content": "You are a final summary bot which means that, there was a different summary bot before you that had to summarize multiple files. I have combines all of those summaries into one file and your job is to summarize all of those summaries that the other bot did. You are going to try your best to understand what the first version of the file was and summarize the whole file. You will be explaining what you think are the more important topics of the file."},
            {"role": "user", "content": text}
        ]
    )
    textFile = open("finalSummary.txt", "w")
    textFile.write(completions['choices'][0]['message']['content'])
    textFile.close()
    print()
    print("Final Summary: " + str(completions['usage']['total_tokens']) + " tokens")
    print(completions['choices'][0]['message']['content'])

def summarize_gpt(text):
    completions = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        temperature=0.7,
        max_tokens=2380,
        messages = [
            {"role": "system", "content": "You job is to summarize a text file as best as you can. Your summary will be concise and will only consist of content that you think is the most important. You do not need to explain anything, just summarize what is in the text file. If I didn't provide you with a text file for you to summarize, say nothing."},
            {"role": "user", "content": text}
        ]
    )
    textFile = open("multiTXTSummary.txt", "a")
    textFile.write(completions['choices'][0]['message']['content'] + "\n" + "\n")
    textFile.close()
    print()
    print("Summary: " + str(completions['usage']['total_tokens']) + " tokens")
    print(completions['choices'][0]['message']['content'])

#create a function named multiTXTSummarizer that takes in a list of text files and outputs it into a seperate text file called multiTXTSummary.txt
def multiTXTSummarizer(textFiles):
    multiTXTSummary = open("multiTXTSummary.txt", "a")
    for textFile in textFiles:
        with open(textFile, 'r') as f:
            fileContent = f.read()
            if fileContent != '':
                summarize_gpt(fileContent)
    multiTXTSummary.close()
    finalSummary_gpt(open("multiTXTSummary.txt", "r").read())
    

# Create a function to import a PDF file
def import_pdf():
    # Open a file dialog and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
    file_locations = []

    # Check if a file was selected
    if file_path:
        print(f'Selected file: {file_path}')

        # Extract text from PDF
        text = extract_text(file_path)

        # Split text into pages
        pages = text.split('\f')
        print(len(pages))

        if len(pages) == 2:
            fileName = f'page_1.txt'
            with open(fileName, 'w', encoding='utf-8') as f:
                f.write(text)
            with open(fileName, 'r', encoding='utf-8') as f:
                fileContent = f.read()
                summarize_gpt(fileContent)
        else:
            # Save each page to a separate text file
            for i, page in enumerate(pages):
                fileName = f'page_{i+1}.txt'
                with open(fileName, 'w') as f:
                    f.write(page)
                file_locations.append(fileName)    

            multiTXTSummarizer(file_locations)

        root.destroy()
    else:
        print('No file selected')

# Create the main window
root = tk.Tk()
root.title('PDF Importer')
root.geometry('200x65')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window
x = (screen_width / 2) - (200 / 2)
y = (screen_height / 2) - (65 / 2)

# Set the dimensions of the screen and where it is placed
root.geometry(f"200x65+{int(x)}+{int(y)}")

# Create a label and a button
label = tk.Label(root, text='Import PDF File')
button = tk.Button(root, text='Import', command=import_pdf)

# Pack the widgets
label.pack()
button.pack()

# Run the main loop
root.mainloop()