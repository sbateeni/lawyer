class DocumentAnalyzer {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.uploadQueue = [];
        this.currentUploads = 0;
        this.maxConcurrentUploads = 3;
    }

    initializeElements() {
        this.uploadArea = document.querySelector('.upload-area');
        this.fileInput = document.querySelector('#file-input');
        this.fileList = document.querySelector('.file-list');
        this.analysisResults = document.querySelector('.analysis-results');
    }

    bindEvents() {
        // تفعيل منطقة السحب والإفلات
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        this.uploadArea.addEventListener('dragover', () => {
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });

        // تفعيل زر اختيار الملفات
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }

    handleFiles(files) {
        Array.from(files).forEach(file => {
            if (this.validateFile(file)) {
                this.addToUploadQueue(file);
            }
        });
        this.processUploadQueue();
    }

    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedTypes = ['application/pdf', 'application/msword', 
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

        if (!allowedTypes.includes(file.type)) {
            this.showError('نوع الملف غير مدعوم. يرجى رفع ملفات PDF أو Word فقط.');
            return false;
        }

        if (file.size > maxSize) {
            this.showError('حجم الملف كبير جداً. الحد الأقصى هو 10 ميجابايت.');
            return false;
        }

        return true;
    }

    addToUploadQueue(file) {
        const fileItem = this.createFileItem(file);
        this.fileList.appendChild(fileItem);
        
        this.uploadQueue.push({
            file,
            element: fileItem
        });
    }

    async processUploadQueue() {
        while (this.uploadQueue.length > 0 && this.currentUploads < this.maxConcurrentUploads) {
            const upload = this.uploadQueue.shift();
            this.currentUploads++;
            await this.uploadAndAnalyzeFile(upload.file, upload.element);
            this.currentUploads--;
        }
    }

    createFileItem(file) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <div class="file-name">${file.name}</div>
                <div class="file-meta">${this.formatFileSize(file.size)}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
            </div>
        `;
        return fileItem;
    }

    async uploadAndAnalyzeFile(file, element) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            // رفع الملف
            const uploadResponse = await this.uploadFile(formData, element);
            if (!uploadResponse.success) throw new Error(uploadResponse.message);

            // تحليل الملف
            const analysisResponse = await this.analyzeFile(uploadResponse.fileId);
            if (!analysisResponse.success) throw new Error(analysisResponse.message);

            this.displayAnalysisResults(analysisResponse.results);
            
        } catch (error) {
            this.showError(`خطأ في معالجة الملف ${file.name}: ${error.message}`);
            element.classList.add('error');
        }
    }

    async uploadFile(formData, element) {
        const progressBar = element.querySelector('.progress-fill');
        
        try {
            const response = await fetch('/api/document-analysis/upload', {
                method: 'POST',
                body: formData,
                onUploadProgress: (progressEvent) => {
                    const progress = (progressEvent.loaded / progressEvent.total) * 100;
                    progressBar.style.width = `${progress}%`;
                }
            });

            return await response.json();
        } catch (error) {
            throw new Error('فشل في رفع الملف');
        }
    }

    async analyzeFile(fileId) {
        try {
            const response = await fetch(`/api/document-analysis/analyze/${fileId}`);
            return await response.json();
        } catch (error) {
            throw new Error('فشل في تحليل الملف');
        }
    }

    displayAnalysisResults(results) {
        const resultsHTML = `
            <div class="result-section">
                <div class="result-header">
                    <h3>نتائج التحليل</h3>
                </div>
                <div class="result-content">
                    <ul class="key-points">
                        ${results.keyPoints.map(point => `
                            <li class="key-point">${point}</li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `;

        this.analysisResults.innerHTML += resultsHTML;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showError(message) {
        // يمكن استخدام مكتبة للإشعارات مثل toastr
        alert(message);
    }
}

// تهيئة محلل المستندات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new DocumentAnalyzer();
});
