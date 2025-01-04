from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
from groq import Groq
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# تهيئة النماذج
models = {}

# تهيئة نموذج Google Gemini إذا كان المفتاح متوفراً
gemini_api_key = os.getenv('GOOGLE_API_KEY')
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        models['gemini'] = genai.GenerativeModel('gemini-pro')
        print("Gemini model initialized successfully")
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")

# تهيئة نموذج Groq Llama إذا كان المفتاح متوفراً
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key:
    try:
        models['llama'] = Groq(api_key=groq_api_key)
        print("Llama model initialized successfully")
    except Exception as e:
        print(f"Error initializing Llama model: {e}")

analysis_bp = Blueprint('analysis', __name__)

def get_analysis_prompt(stage, text, model_type="gemini"):
    """إنشاء النص التوجيهي المناسب للمرحلة"""
    base_prompts = {
        1: f"قم بالتحليل الأولي للنص التالي:\n{text}\n\nيجب أن يتضمن التحليل:\n- تحديد نوع القضية\n- فهم الأطراف المعنية\n- استخراج التواريخ والمعلومات الأساسية",
        
        2: f"قم بتحليل الوقائع والأحداث في القضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- ترتيب الأحداث زمنياً\n- تحديد النقاط الرئيسية في القضية",
        
        3: f"قم بالتحليل القانوني الأساسي للقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تحديد المواد القانونية ذات الصلة\n- تصنيف القضية قانونياً",
        
        4: f"قم بتحليل الأدلة والمستندات في القضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تقييم قوة الأدلة المقدمة\n- تحديد الثغرات في الأدلة",
        
        5: f"قم بتحليل السوابق القضائية المتعلقة بالقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- البحث عن قضايا مشابهة\n- تحليل الأحكام السابقة ذات الصلة",
        
        6: f"قم بتحليل الحجج القانونية في القضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تحديد نقاط القوة في القضية\n- تحديد نقاط الضعف المحتملة",
        
        7: f"قم بتحليل الدفوع القانونية الممكنة في القضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- اقتراح الدفوع الممكنة\n- تقييم فعالية كل دفع",
        
        8: f"قم بالتحليل الإجرائي للقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تحديد الإجراءات القانونية المطلوبة\n- تحديد المواعيد والمهل القانونية",
        
        9: f"قم بصياغة الاستراتيجية القانونية للقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- وضع خطة التعامل مع القضية\n- تحديد أولويات العمل",
        
        10: f"قم بتحليل المخاطر والفرص في القضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تقييم احتمالات النجاح\n- تحديد المخاطر المحتملة",
        
        11: f"قم باقتراح الحلول والبدائل للقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تقديم خيارات التسوية الممكنة\n- اقتراح حلول بديلة",
        
        12: f"قم بإعداد الملخص النهائي للقضية التالية:\n{text}\n\nيجب أن يتضمن التحليل:\n- تلخيص جميع النتائج\n- تقديم التوصيات النهائية"
    }
    
    prompt = base_prompts.get(stage, "قم بتحليل القضية التالية")
    
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

@analysis_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """تحليل النص المدخل"""
    data = request.json
    stage = int(data['stage'])
    text = data['text']
    model_type = data.get('model_type', 'gemini')
    
    if model_type not in models:
        return jsonify({
            "status": "error",
            "message": f"النموذج {model_type} غير متوفر. المتوفر: {', '.join(models.keys())}"
        }), 400
    
    try:
        # إنشاء النص التوجيهي
        prompt = get_analysis_prompt(stage, text, model_type)
        
        # استخدام النموذج المحدد للتحليل
        if model_type == 'gemini':
            response = models['gemini'].generate_content(prompt)
            result = response.text
        else:  # llama
            completion = models['llama'].chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model="llama3-groq-70b-8192-tool-use-preview",
                temperature=0.7,
                max_tokens=4096,
                top_p=0.9,
                stream=False
            )
            result = completion.choices[0].message.content
        
        return jsonify({
            "status": "success",
            "result": result,
            "model_used": model_type
        })
    except Exception as e:
        print(f"Error in analysis: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500