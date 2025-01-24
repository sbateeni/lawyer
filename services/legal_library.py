import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

# تحميل متغيرات البيئة
load_dotenv()

# إعداد نماذج الذكاء الاصطناعي
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# تهيئة النماذج
models = {
    'gemini': genai.GenerativeModel('gemini-pro'),
    'llama': groq_client
}

SYSTEM_PROMPT_ARABIC = """أنت مساعد قانوني متخصص في القوانين الفلسطينية. عليك الالتزام بما يلي:
1. استخدم اللغة العربية الفصحى حصراً في جميع إجاباتك
2. لا تستخدم أي كلمات أو عبارات باللغة الإنجليزية مطلقاً
3. قدم إجابات دقيقة ومفصلة عن القوانين الفلسطينية
4. اذكر المواد القانونية والمراجع ذات الصلة
5. استشهد بالسوابق القضائية المناسبة إن وجدت
6. وضح التفسيرات والشروحات القانونية بأسلوب مهني"""

class LegalLibraryService:
    def __init__(self):
        self.legal_sources = json.loads(os.getenv('LEGAL_SOURCES_API'))
        self.ai_config = json.loads(os.getenv('AI_MODEL_CONFIG'))
        
    async def search_legal_info(self, query):
        """البحث في القوانين باستخدام الذكاء الاصطناعي"""
        try:
            # إعداد النص المطلوب للتحليل
            analysis_prompt = f"""قم بتحليل الاستفسار القانوني التالي باللغة العربية الفصحى حصراً:
            الاستفسار: {query}
            المطلوب:
            1. تحديد المجال القانوني
            2. تحديد القوانين ذات الصلة
            3. تحديد المواد القانونية المرتبطة
            4. تقديم تحليل قانوني أولي"""

            # استخدام Gemini للتحليل
            analysis_response = models['gemini'].generate_content(analysis_prompt)
            analysis_result = analysis_response.text

            # استخدام Llama للبحث
            search_response = models['llama'].chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": SYSTEM_PROMPT_ARABIC
                }, {
                    "role": "user",
                    "content": f"قم بالبحث عن القوانين والأحكام المتعلقة بالموضوع التالي وأجب باللغة العربية حصراً: {query}"
                }],
                model="llama3-groq-70b-8192-tool-use-preview",
                temperature=0.7,
                max_tokens=4096,
                top_p=0.9,
                stream=False
            )
            
            # جمع النتائج من المصادر
            sources_results = await self._fetch_from_sources(query)
            
            results = {
                'analysis': analysis_result,
                'search': search_response.choices[0].message.content,
                'sources': sources_results
            }
            
            return results
        except Exception as e:
            print(f"Error in search_legal_info: {str(e)}")
            return {
                'error': str(e),
                'analysis': 'حدث خطأ في التحليل',
                'search': 'حدث خطأ في البحث',
                'sources': {}
            }
    
    async def _fetch_from_sources(self, query):
        """جمع المعلومات من المصادر الرسمية"""
        try:
            results = {}
            for source, api_url in self.legal_sources.items():
                # هنا سيتم إضافة منطق الاتصال بـ APIs المصادر
                results[source] = f"نتائج من {source} للاستعلام: {query}"
            return results
        except Exception as e:
            print(f"Error in _fetch_from_sources: {str(e)}")
            return {}

    async def get_law_details(self, law_id):
        """الحصول على تفاصيل قانون محدد"""
        try:
            # سيتم تنفيذ هذه الوظيفة لاحقاً
            return {
                'id': law_id,
                'title': 'عنوان القانون',
                'content': 'محتوى القانون'
            }
        except Exception as e:
            print(f"Error in get_law_details: {str(e)}")
            return None

    async def get_latest_updates(self):
        """الحصول على آخر التحديثات القانونية"""
        try:
            # سيتم تنفيذ هذه الوظيفة لاحقاً
            return [{
                'id': 1,
                'title': 'تحديث قانوني',
                'date': '2024-01-03'
            }]
        except Exception as e:
            print(f"Error in get_latest_updates: {str(e)}")
            return [] 