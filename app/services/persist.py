import openai
import pytesseract
from pdf2image import convert_from_path
import os
from concurrent.futures import ThreadPoolExecutor

# OpenAI API key
openai.api_key = "sk-proj-mcl6qphfyyiutAZScQ8HT3BlbkFJYbydPM2xE29yfzshm7Na"

# Function to extract text using OCR
from concurrent.futures import ThreadPoolExecutor
import pytesseract
from pdf2image import convert_from_path
import traceback

def extract_text_from_image(image):
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Failed to process image with OCR: {e}")
        traceback.print_exc()
        return ""

def extract_text_with_ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        extracted_text = ""
        with ThreadPoolExecutor(max_workers=min(4, len(images))) as executor:  # Limit the number of workers to a reasonable number
            results = executor.map(extract_text_from_image, images)
        for text in results:
            extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        traceback.print_exc()
        return None

# Function to generate trivia questions using GPT
def generate_questions_from_gpt(extracted_text):
    try:
        # Create the GPT prompt
        prompt = f"""
        Please generate a set of trivia questions based on the provided text. I WANT 5 TOPICS. For each topic identified, create a total of 15 questions, categorized into three difficulty levels: easy, medium, and hard. Each category should contain 5 questions.
        Please format the questions with multiple-choice answers, ensuring that the first option is always the correct answer. The structure should be as follows:

        **Topic 1:**

        **Easy Questions:**

        1. [Insert question]  
           a) Option A  
           b) Option B  
           c) Option C  
           d) Option D

        **Medium Questions:**

        1. [Insert question]  
           a) Option A  
           b) Option B  
           c) Option C  
           d) Option D

        **Hard Questions:**

        1. [Insert question]  
           a) Option A  
           b) Option B  
           c) Option C  
           d) Option D

        NOW AT THE SAME STRUCTURE MORE 4 TOPICS ! 
        Provided Text:
        {extracted_text}
        """
        
        # Call OpenAI's GPT API using the gpt-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that generates trivia questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000,
            n=1,
            temperature=0.7
        )
        # Return the generated questions
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating questions from GPT: {e}")
        return None

# Function to process the PDF and save generated questions
def process_pdf(pdf_path, filename, questions_folder, processing_status):
    """Process the PDF and update status"""
    extracted_text = extract_text_with_ocr(pdf_path)
    if extracted_text:
        gpt_response = generate_questions_from_gpt(extracted_text)
        if gpt_response:
            txt_filename = f"{filename}.txt"  # Use the filename dynamically
            txt_path = os.path.join(questions_folder, txt_filename)
            with open(txt_path, 'w') as text_file:
                text_file.write(gpt_response)

            # Mark processing as complete
            processing_status[filename] = 'complete'
            # Remove the uploaded PDF after processing
            os.remove(pdf_path)
    else:
        # Handle extraction failure
        processing_status[filename] = 'failed'
