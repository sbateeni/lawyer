class LawInformation {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupSearch();
    }

    initializeElements() {
        this.searchInput = document.querySelector('.search-input');
        this.categoryTags = document.querySelectorAll('.category-tag');
        this.articleList = document.querySelector('.article-list');
        this.infoGrid = document.querySelector('.info-grid');
    }

    bindEvents() {
        // تفعيل التصنيفات
        this.categoryTags.forEach(tag => {
            tag.addEventListener('click', () => this.handleCategoryClick(tag));
        });

        // تفعيل البطاقات
        if (this.infoGrid) {
            this.infoGrid.addEventListener('click', (e) => {
                const card = e.target.closest('.info-card');
                if (card) {
                    this.handleCardClick(card);
                }
            });
        }
    }

    setupSearch() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(() => {
                this.performSearch(this.searchInput.value);
            }, 300));
        }
    }

    handleCategoryClick(tag) {
        tag.classList.toggle('active');
        this.filterContent();
    }

    async performSearch(query) {
        try {
            const response = await fetch(`/api/law-information/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateContent(data.results);
            } else {
                console.error('خطأ في البحث:', data.message);
            }
        } catch (error) {
            console.error('خطأ في الاتصال بالخادم:', error);
        }
    }

    filterContent() {
        const activeCategories = Array.from(document.querySelectorAll('.category-tag.active'))
            .map(tag => tag.dataset.category);

        const items = document.querySelectorAll('[data-category]');
        
        items.forEach(item => {
            const itemCategory = item.dataset.category;
            const shouldShow = activeCategories.length === 0 || 
                             activeCategories.includes(itemCategory);
            
            item.style.display = shouldShow ? '' : 'none';
        });
    }

    async handleCardClick(card) {
        const articleId = card.dataset.id;
        if (!articleId) return;

        try {
            const response = await fetch(`/api/law-information/article/${articleId}`);
            const data = await response.json();
            
            if (data.success) {
                this.showArticleModal(data.article);
            } else {
                this.showError('لا يمكن تحميل المقال في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة تحميل المقال');
        }
    }

    updateContent(results) {
        if (this.articleList) {
            this.articleList.innerHTML = results.map(article => `
                <div class="article-item" data-category="${article.category}">
                    <h3 class="article-title">${article.title}</h3>
                    <p class="article-description">${article.description}</p>
                    <div class="article-meta">
                        <span>${article.date}</span>
                        <span>${article.category}</span>
                    </div>
                </div>
            `).join('');
        }
    }

    showArticleModal(article) {
        // يمكن استخدام مكتبة مثل Bootstrap Modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h2>${article.title}</h2>
                <div class="article-content">
                    ${article.content}
                </div>
                <button class="modal-close">إغلاق</button>
            </div>
        `;

        document.body.appendChild(modal);
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });
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

// تهيئة صفحة المعلومات القانونية عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new LawInformation();
});
