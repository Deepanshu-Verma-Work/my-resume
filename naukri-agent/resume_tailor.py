import os
import re
from config import Config
import google.generativeai as genai
import subprocess

class ResumeTailor:
    def __init__(self):
        self.base_resume_path = Config.RESUME_PATH
        self.output_dir = Config.OUTPUT_DIR
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Setup Gemini
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # Debug: List available models
            print("Available Gemini Models:")
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        print(f"- {m.name}")
            except Exception as e:
                print(f"Error listing models: {e}")

            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            print("Warning: GEMINI_API_KEY not found. Resume tailoring will not work.")
            self.model = None

    def read_resume(self):
        with open(self.base_resume_path, 'r', encoding='utf-8') as f:
            return f.read()

    def tailor_resume(self, jd_text):
        if not self.model:
            return None
            
        resume_content = self.read_resume()
        
        prompt = f"""
        You are an expert Resume Writer. 
        I have a LaTeX resume and a Job Description (JD). 
        Your task is to modify the resume content to better align with the JD, WITHOUT lying or fabricating experience.
        
        Focus on:
        1. Updating the "Career Summary" to highlight relevant skills.
        2. Rephrasing bullet points in "Professional Experience" to match JD keywords.
        3. Updating "Technical Skills" order to prioritize JD requirements.
        
        CRITICAL LATEX INSTRUCTIONS:
        - The "Technical Skills" section uses a `tabularx` inside an `itemize`. 
        - YOU MUST MAINTAIN THIS EXACT STRUCTURE:
          \\section{{Technical Skills}}
           \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
            \\small{{\\item{{
             \\begin{{tabularx}}{{\\linewidth}}{{ @{{}} l @{{\\hspace{{1ex}}}} X @{{}} }}
              \\textbf{{Category}} & : Skills \\\\
              \\textbf{{Another Category}} & : Skills \\\\
             \\end{{tabularx}}
            }}}}
           \\end{{itemize}}
        - Do NOT change the column definitions or the nesting.
        - Ensure every row in tabularx ends with `\\\\` except the last one (optional but good practice).
        - Do NOT add empty lines inside the `\\item{{...}}` block.
        
        Here is the JD:
        {jd_text}
        
        Here is the LaTeX Resume:
        {resume_content}
        
        Return ONLY the full modified LaTeX code. Do not include markdown formatting like ```latex.
        """
        
        try:
            response = self.model.generate_content(prompt)
            modified_latex = response.text
            
            # Clean up markdown if present
            modified_latex = modified_latex.replace("```latex", "").replace("```", "")
            
            return modified_latex
        except Exception as e:
            print(f"Error tailoring resume: {e}")
            return None

    def save_resume(self, content, filename="tailored_resume.tex"):
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def compile_resume(self, tex_path):
        try:
            # MiKTeX path provided by user
            miktex_bin = r"D:\MiKTeX_Naukri\miktex\bin\x64" 
            pdflatex_cmd = os.path.join(miktex_bin, "pdflatex.exe")
            
            # If user installed elsewhere or added to PATH, fallback to just 'pdflatex'
            if not os.path.exists(pdflatex_cmd):
                pdflatex_cmd = "pdflatex"

            output_dir = os.path.dirname(tex_path)
            
            # Use subprocess.run for safer execution with arguments
            cmd = [
                pdflatex_cmd,
                "-interaction=nonstopmode",
                "-output-directory", output_dir,
                tex_path
            ]
            
            print(f"Compiling PDF: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                pdf_path = tex_path.replace(".tex", ".pdf")
                if os.path.exists(pdf_path):
                    print(f"PDF compiled successfully: {pdf_path}")
                    return pdf_path
            
            print(f"PDF compilation failed. Output:\n{result.stdout}\nError:\n{result.stderr}")
            return None
            
        except Exception as e:
            print(f"Error compiling PDF: {e}")
            return None

if __name__ == "__main__":
    # Test
    tailor = ResumeTailor()
    dummy_jd = "Looking for a GenAI Engineer with experience in AWS Bedrock and Python."
    # print(tailor.tailor_resume(dummy_jd))
