// تعريف المراحل
const stages = [
    { id: 1, title: 'التحليل الأولي للنص', model: 'gemini' },
    { id: 2, title: 'تحليل الوقائع والأحداث', model: 'llama' },
    { id: 3, title: 'التحليل القانوني الأساسي', model: 'gemini' },
    { id: 4, title: 'تحليل الأدلة والمستندات', model: 'llama' },
    { id: 5, title: 'تحليل السوابق القضائية', model: 'gemini' },
    { id: 6, title: 'تحليل الحجج القانونية', model: 'llama' },
    { id: 7, title: 'تحليل الدفوع القانونية', model: 'gemini' },
    { id: 8, title: 'التحليل الإجرائي', model: 'llama' },
    { id: 9, title: 'صياغة الاستراتيجية القانونية', model: 'gemini' },
    { id: 10, title: 'تحليل المخاطر والفرص', model: 'llama' },
    { id: 11, title: 'اقتراح الحلول والبدائل', model: 'gemini' },
    { id: 12, title: 'إعداد الملخص النهائي', model: 'llama' }
];

class CaseAnalyzer {
    constructor() {
        this.analysesList = document.querySelector('.analyses-list');
        this.currentCase = null;
        this.completedStages = 0;
        this.initializeUI();
        this.bindEvents();
    }

    initializeUI() {
        this.createAnalysisCards();
    }

    bindEvents() {
        document.getElementById('startAnalysis').addEventListener('click', () => this.startAnalysis());
    }

    createAnalysisCards() {
        stages.forEach(stage => {
            const card = document.createElement('div');
            card.className = 'analysis-card pending';
            card.id = `stage-${stage.id}`;
            card.innerHTML = `
                <div class="stage-header">
                    <h3>${stage.title}</h3>
                    <span class="model-badge ${stage.model}">${stage.model === 'gemini' ? 'Google Gemini Pro' : 'Llama 3 (Groq)'}</span>
                </div>
                <div class="stage-content">
                    <div class="stage-status">في انتظار التحليل...</div>
                </div>
            `;
            this.analysesList.appendChild(card);
        });
    }

    async analyzeStage(stage, caseData) {
        const card = document.getElementById(`stage-${stage.id}`);
        card.className = 'analysis-card processing';
        card.querySelector('.stage-status').textContent = 'جاري التحليل...';

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: caseData.description,
                    stage: stage.id,
                    model_type: stage.model
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                this.handleSuccessfulAnalysis(card, data);
            } else {
                throw new Error(data.message);
            }
            return true;
        } catch (error) {
            this.handleAnalysisError(card, error, stage.id);
            return false;
        }
    }

    handleSuccessfulAnalysis(card, data) {
        card.className = 'analysis-card completed';
        card.querySelector('.stage-content').innerHTML = `
            <div class="analysis-result">${data.result}</div>
            <div class="analysis-meta">
                <span class="analysis-time">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        this.completedStages++;
        
        if (this.completedStages === stages.length) {
            this.showSuccessMessage();
        }
    }

    handleAnalysisError(card, error, stageId) {
        card.className = 'analysis-card error';
        card.querySelector('.stage-content').innerHTML = `
            <div class="error-message">حدث خطأ: ${error.message}</div>
            <button class="btn-retry" onclick="caseAnalyzer.retryAnalysis(${stageId})">إعادة المحاولة</button>
        `;
    }

    showSuccessMessage() {
        document.getElementById('success-message').style.display = 'block';
        document.getElementById('success-message').scrollIntoView({ behavior: 'smooth' });
    }

    validateForm() {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;

        if (!title || !description) {
            alert('يرجى ملء جميع الحقول المطلوبة');
            return false;
        }
        return { title, description };
    }

    disableForm() {
        document.getElementById('title').disabled = true;
        document.getElementById('description').disabled = true;
        document.getElementById('startAnalysis').disabled = true;
    }

    async startAnalysis() {
        const formData = this.validateForm();
        if (!formData) return;

        this.disableForm();
        this.completedStages = 0;
        document.getElementById('success-message').style.display = 'none';

        for (const stage of stages) {
            await this.analyzeStage(stage, { description: formData.description });
        }
    }

    async retryAnalysis(stageId) {
        const stage = stages.find(s => s.id === stageId);
        const description = document.getElementById('description').value;
        if (stage) {
            await this.analyzeStage(stage, { description });
        }
    }
}

// تهيئة المحلل عند تحميل الصفحة
const caseAnalyzer = new CaseAnalyzer();
