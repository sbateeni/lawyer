import google.generativeai as genai
from groq import Groq
import os
from dotenv import load_dotenv
from services.db_manager import db_manager

load_dotenv()

class AnalysisService:
    def __init__(self):
        # تهيئة النماذج
        self.models = {}
        
        # تهيئة نموذج Google Gemini
        gemini_api_key = os.getenv('GOOGLE_API_KEY')
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.models['gemini'] = genai.GenerativeModel('gemini-pro')
                print("Gemini model initialized successfully")
            except Exception as e:
                print(f"Error initializing Gemini model: {e}")

        # تهيئة نموذج Groq Llama
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key:
            try:
                self.models['llama'] = Groq(api_key=groq_api_key)
                print("Llama model initialized successfully")
            except Exception as e:
                print(f"Error initializing Llama model: {e}")
        
    def analyze_stage(self, case_id: int, stage: int, model_type: str, text: str) -> str:
        """
        تحليل مرحلة من القضية باستخدام النموذج المحدد
        """
        try:
            if model_type not in self.models:
                raise Exception(f"النموذج {model_type} غير متوفر")
                
            # تحديد النموذج المناسب والبرومبت
            prompt = self._get_stage_prompt(stage, text, model_type)
            
            if model_type == 'gemini':
                result = self._analyze_with_gemini(prompt)
            else:
                result = self._analyze_with_llama(prompt)
            
            # حفظ نتيجة التحليل في قاعدة البيانات
            success = db_manager.add_analysis(case_id, stage, result)
            if not success:
                raise Exception("فشل في حفظ نتيجة التحليل")
                
            return result
            
        except Exception as e:
            print(f"Error in analyze_stage: {str(e)}")
            raise e
            
    def _analyze_with_gemini(self, prompt: str) -> str:
        """
        تحليل النص باستخدام نموذج Gemini
        """
        response = self.models['gemini'].generate_content(prompt)
        return response.text
        
    def _analyze_with_llama(self, prompt: str) -> str:
        """
        تحليل النص باستخدام نموذج Llama
        """
        completion = self.models['llama'].chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=4096,
            top_p=0.9,
            stream=False
        )
        return completion.choices[0].message.content
        
    def _get_stage_prompt(self, stage: int, text: str, model_type: str) -> str:
        """
        إنشاء البرومبت المناسب للمرحلة
        """
        base_prompts = {
            1: f"""قم بتحليل النص القانوني التالي وحدد النقاط الرئيسية والمواضيع القانونية المطروحة:
                {text}
                
                قم بتقديم:
                1. ملخص موجز للقضية
                2. المواضيع القانونية الرئيسية
                3. الأطراف المعنية وأدوارهم
                """,
                
            3: f"""قم بإجراء تحليل قانوني أساسي للنص التالي:
                {text}
                
                حدد:
                1. القوانين والمواد القانونية ذات الصلة
                2. المبادئ القانونية المنطبقة
                3. التكييف القانوني للوقائع
                """,
                
            5: f"""ابحث عن السوابق القضائية المشابهة للقضية التالية:
                {text}
                
                قدم:
                1. أهم السوابق القضائية المشابهة
                2. المبادئ القانونية المستخلصة منها
                3. كيفية الاستفادة منها في القضية الحالية
                """,
                
            7: f"""حلل الدفوع القانونية الممكنة للقضية التالية:
                {text}
                
                قدم:
                1. الدفوع الشكلية الممكنة
                2. الدفوع الموضوعية الممكنة
                3. الأسانيد القانونية لكل دفع
                """
        }
        
        prompt = base_prompts.get(stage, f"قم بتحليل النص التالي للمرحلة {stage}:\n{text}")
        
        if model_type == "llama":
            prompt = f"""أنت محامٍ خبير في القانون الفلسطيني ومتخصص في التحليل القانوني باللغة العربية.

            تعليمات هامة:
            1. يجب أن تكون إجابتك باللغة العربية الفصحى
            2. استخدم المصطلحات القانونية العربية الصحيحة
            3. قم بتنظيم إجابتك في نقاط وفقرات واضحة
            4. اذكر المواد القانونية والتشريعات بدقة
            5. اكتب الأرقام والتواريخ بالأرقام العربية (١، ٢، ٣)

            القضية المطروحة:
            {text}

            المطلوب تحليله:
            {prompt}

            قم بتقديم تحليل قانوني شامل ومفصل باللغة العربية، مع التركيز على الجوانب القانونية المهمة والاستناد إلى القوانين والتشريعات الفلسطينية."""
            
        return prompt 