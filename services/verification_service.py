import google.generativeai as genai
from typing import Dict, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class VerificationService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def verify_legal_text(self, stage_text: str, stage_type: str) -> Tuple[bool, str, str]:
        """
        Verify the legal text using Gemini with web search
        Returns: (is_matching, result_text, source)
        """
        prompt = f"""
        تحقق من صحة النص القانوني التالي عبر الإنترنت:
        {stage_text}
        
        نوع المرحلة: {stage_type}
        
        قم بالبحث عن هذا النص في المصادر القانونية الموثوقة وقارن النتائج.
        إذا كان النص صحيحاً، أكد ذلك.
        إذا كان هناك اختلاف، قدم النص الصحيح مع المصدر.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text
            
            # تحليل الرد لتحديد ما إذا كان النص متطابقاً
            is_matching = "النص صحيح" in result or "متطابق" in result
            
            return is_matching, result, "Gemini Search Results"
        except Exception as e:
            return False, f"حدث خطأ أثناء التحقق: {str(e)}", "Error" 