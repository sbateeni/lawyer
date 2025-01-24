class LegalLibrary {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupSearch();
        this.setupFilters();
    }

    initializeElements() {
        this.searchInput = document.querySelector('.search-input');
        this.filterTags = document.querySelectorAll('.filter-tag');
        this.documentList = document.querySelector('.document-list');
    }

    bindEvents() {
        // تفعيل أزرار التصفية
        this.filterTags.forEach(tag => {
            tag.addEventListener('click', () => this.handleFilterClick(tag));
        });

        // تفعيل أزرار العمل
        document.querySelectorAll('.action-button').forEach(button => {
            button.addEventListener('click', (e) => this.handleActionClick(e));
        });
    }

    setupSearch() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(() => {
                this.performSearch(this.searchInput.value);
            }, 300));
        }
    }

    setupFilters() {
        this.activeFilters = new Set();
    }

    handleFilterClick(tag) {
        tag.classList.toggle('active');
        const filter = tag.dataset.filter;

        if (this.activeFilters.has(filter)) {
            this.activeFilters.delete(filter);
        } else {
            this.activeFilters.add(filter);
        }

        this.applyFilters();
    }

    async performSearch(query) {
        try {
            const response = await fetch(`/api/legal-library/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateDocumentList(data.results);
            } else {
                console.error('خطأ في البحث:', data.message);
            }
        } catch (error) {
            console.error('خطأ في الاتصال بالخادم:', error);
        }
    }

    applyFilters() {
        const documents = document.querySelectorAll('.document-item');
        
        documents.forEach(doc => {
            const docCategories = doc.dataset.categories.split(',');
            const shouldShow = this.activeFilters.size === 0 || 
                             [...this.activeFilters].some(filter => docCategories.includes(filter));
            
            doc.style.display = shouldShow ? 'flex' : 'none';
        });
    }

    handleActionClick(event) {
        const button = event.target;
        const action = button.dataset.action;
        const documentId = button.closest('.document-item').dataset.id;

        switch(action) {
            case 'view':
                this.viewDocument(documentId);
                break;
            case 'download':
                this.downloadDocument(documentId);
                break;
        }
    }

    async viewDocument(documentId) {
        try {
            const response = await fetch(`/api/legal-library/document/${documentId}`);
            const data = await response.json();
            
            if (data.success) {
                // افتح المستند في نافذة جديدة أو مشغل المستندات
                window.open(data.viewUrl, '_blank');
            } else {
                this.showError('لا يمكن عرض المستند في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة عرض المستند');
        }
    }

    async downloadDocument(documentId) {
        try {
            const response = await fetch(`/api/legal-library/download/${documentId}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `document-${documentId}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            } else {
                this.showError('لا يمكن تحميل المستند في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة تحميل المستند');
        }
    }

    updateDocumentList(results) {
        if (!this.documentList) return;

        this.documentList.innerHTML = results.map(doc => `
            <div class="document-item" data-id="${doc.id}" data-categories="${doc.categories.join(',')}">
                <div class="document-info">
                    <h3 class="document-title">${doc.title}</h3>
                    <div class="document-meta">
                        <span>${doc.date}</span> • 
                        <span>${doc.category}</span> • 
                        <span>${doc.size}</span>
                    </div>
                </div>
                <div class="document-actions">
                    <button class="action-button view" data-action="view">
                        <i class="fas fa-eye"></i> عرض
                    </button>
                    <button class="action-button download" data-action="download">
                        <i class="fas fa-download"></i> تحميل
                    </button>
                </div>
            </div>
        `).join('');
    }

    showError(message) {
        // يمكن استخدام مكتبة للإشعارات مثل toastr
        alert(message);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// تهيئة المكتبة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new LegalLibrary();
});
