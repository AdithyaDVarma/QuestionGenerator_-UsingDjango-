import os
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Open the PDF file
        reader = PdfReader(pdf_path)
        
        # Extract text from all pages
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        return full_text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def generate_analysis(file_content):
    """
    Generate summary, Bloom's Taxonomy questions, and their answers using Groq API.
    
    Args:
        file_content (str): Text content to analyze
    
    Returns:
        str: Comprehensive analysis with summary, questions, and answers
    """
    # Detailed analysis prompt with answers
    # prompt = (f"Provide a comprehensive analysis of the following text:\n\n"
    #           "SECTION 1: COMPREHENSIVE SUMMARY\n"
    #           "- Create a detailed, cohesive summary of the text\n"
    #           "- Aim for 3-4 paragraphs\n"
    #           "- Capture the most important points, key themes, and main ideas\n"
    #           "- Ensure the summary provides a clear overview of the entire text\n\n"
    #           "SECTION 2: BLOOM'S TAXONOMY QUESTIONS AND ANSWERS\n"
    #           "Bloom's Taxonomy Levels:\n"
    #           "1. Knowledge: Recall of facts, terms, basic concepts\n"
    #           "2. Comprehension: Understanding the meaning of information\n"
    #           "3. Application: Using learned knowledge in new situations\n"
    #           "4. Analysis: Breaking down information into parts to explore understandings\n"
    #           "5. Synthesis: Combining information to create new or original ideas\n"
    #           "6. Evaluation: Judging the value of information, ideas, or solutions\n\n"
    #           "Question and Answer Generation Instructions:\n"
    #           "- Create 5 questions each for the different Taxonomy levels, distributed across all 6 levels of Bloom's Taxonomy\n"
    #           "- For each question, provide a detailed and accurate answer\n"
    #           "- Ensure questions progressively increase in complexity\n"
    #           "- Clearly label each question and its answer with the corresponding Bloom's Taxonomy level\n\n"
    #           "TEXT TO ANALYZE:\n"
    #           f"{file_content}")

    prompt = (f"Provide a comprehensive analysis of the following text:\n\n"
          "SECTION 1: COMPREHENSIVE SUMMARY\n"
          "- Create a detailed, cohesive summary of the text\n"
          "- Aim for 3-4 paragraphs\n"
          "- Capture the most important points, key themes, and main ideas\n"
          "- Ensure the summary provides a clear overview of the entire text\n\n"
          "SECTION 2: BLOOM'S TAXONOMY QUESTIONS AND ANSWERS\n"
          "Bloom's Taxonomy Levels:\n"
          "1. Knowledge: Recall of facts, terms, basic concepts\n"
          "2. Comprehension: Understanding the meaning of information\n"
          "3. Application: Using learned knowledge in new situations\n"
          "4. Analysis: Breaking down information into parts to explore understandings\n"
          "5. Synthesis: Combining information to create new or original ideas\n"
          "6. Evaluation: Judging the value of information, ideas, or solutions\n\n"
          "Question and Answer Generation Instructions:\n"
          "- Strictly generate exactly 5 questions for each of the 6 levels of Bloom's Taxonomy\n"
          "- For each question, provide a detailed and accurate answer\n"
          "- Ensure the questions progressively increase in complexity\n"
          "- If fewer than 5 questions are possible for a level, fill the remainder with unique rephrasings or variations of valid questions and answers\n"
          "- Clearly label each question and its answer with the corresponding Bloom's Taxonomy level\n\n"
          "OUTPUT FORMAT:\n"
          "Provide the results in JSON format with the following structure:\n"
          "{\n"
          "  \"summary\": \"<Detailed summary of the text>\",\n"
          "  \"questions_and_answers\": [\n"
          "    {\n"
          "      \"level\": \"<Bloom's Taxonomy Level>\",\n"
          "      \"questions\": [\n"
          "        {\n"
          "          \"question\": \"<Question text>\",\n"
          "          \"answer\": \"<Detailed answer text>\"\n"
          "        },\n"
          "        ... (5 questions per level)\n"
          "      ]\n"
          "    },\n"
          "    ... (for all 6 levels)\n"
          "  ]\n"
          "}\n\n"
          "IMPORTANT:\n"
          "- Ensure there are exactly 5 unique questions per Bloom's Taxonomy level in the output.\n"
          "- Avoid repeating questions across levels or within the same level.\n\n"
          "TEXT TO ANALYZE:\n"
          f"{file_content}")


    # Generate content using the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        response_format={"type": "json_object"},
    )

    # Return the full response
    return chat_completion.choices[0].message.content

# def main():
#     # PDF file path
#     pdf_path = "frenchrevolution.pdf"
    
#     # Extract text from PDF
#     file_content = extract_text_from_pdf(pdf_path)
    
#     if not file_content:
#         print("Could not extract text from the PDF.")
#         return
    
#     # Truncate input if it's extremely long (Groq has token limits)
#     if len(file_content) > 50000:
#         file_content = file_content[:50000]
    
#     # Generate analysis
#     analysis_result = generate_analysis(file_content)
    
#     # Print the analysis result
#     print("\n--- PDF Analysis Result ---")
#     print(analysis_result)
    
#     # Save to file
#     output_file = 'pdf_analysis_output.txt'
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write(analysis_result)
    
#     print(f"\nFull analysis has been saved to {output_file}")