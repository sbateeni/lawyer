from typing import Dict, List
import PyPDF2
import docx
import os
import re

class DocumentAnalyzer:
    def __init__(self):
        self.legal_terms = [
            "قانون", "محكمة", "حكم", "دعوى", "عقد", "اتفاقية",
            "حقوق", "التزامات", "تعويض", "مسؤولية", "موكل",
            "قضية", "محامي", "موكل", "شهادة", "إثبات"
        ]
        
        self.legal_indicators = [
            "يجب", "يلتزم", "يحق", "قانون", "حكم", "محكمة",
            "عقد", "اتفاق", "شرط", "بند", "مادة"
        ]

    def extract_text(self, file_path: str) -> str:
        """استخراج النص من الملف"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("نوع الملف غير مدعوم")

    def _extract_from_pdf(self, file_path: str) -> str:
        """استخراج النص من ملف PDF"""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """استخراج النص من ملف Word"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def analyze_document(self, file_path: str) -> Dict:
        """تحليل المستند وإرجاع النتائج"""
        try:
            # استخراج النص
            text = self.extract_text(file_path)
            
            # تقسيم النص إلى فقرات
            paragraphs = [p for p in text.split('\n') if p.strip()]
            
            # تحليل المستند
            analysis = {
                "legal_keywords": self._extract_legal_keywords(text),
                "key_points": self._extract_key_points(paragraphs),
                "document_statistics": self._get_document_statistics(text),
                "document_structure": self._analyze_document_structure(paragraphs)
            }
            
            return analysis
        
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }

    def _extract_legal_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات القانونية المهمة"""
        found_terms = []
        text_lower = text.lower()
        for term in self.legal_terms:
            if term in text_lower:
                found_terms.append(term)
        return found_terms

    def _extract_key_points(self, paragraphs: List[str]) -> List[str]:
        """استخراج النقاط الرئيسية من المستند"""
        key_points = []
        
        for paragraph in paragraphs:
            sentences = re.split('[.!؟]', paragraph)
            for sentence in sentences:
                if any(indicator in sentence for indicator in self.legal_indicators):
                    cleaned_sentence = sentence.strip()
                    if cleaned_sentence and len(cleaned_sentence) > 20:
                        key_points.append(cleaned_sentence)
                        if len(key_points) >= 10:
                            return key_points
        
        return key_points

    def _get_document_statistics(self, text: str) -> Dict:
        """حساب إحصائيات المستند"""
        words = text.split()
        return {
            "total_words": len(words),
            "total_characters": len(text),
            "unique_words": len(set(words))
        }

    def _analyze_document_structure(self, paragraphs: List[str]) -> Dict:
        """تحليل هيكل المستند"""
        structure = {
            "total_paragraphs": len(paragraphs),
            "sections": []
        }

        current_section = None
        for paragraph in paragraphs:
            # تحديد إذا كان الفقرة عنوان قسم
            if len(paragraph.split()) <= 7 and any(term in paragraph.lower() for term in ["باب", "فصل", "مادة", "قسم"]):
                current_section = paragraph.strip()
                structure["sections"].append({
                    "title": current_section,
                    "content_length": 0
                })
            elif current_section and len(structure["sections"]) > 0:
                structure["sections"][-1]["content_length"] += len(paragraph)

        return structure
