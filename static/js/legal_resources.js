class LegalResources {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadStats();
    }

    initializeElements() {
        this.filterSelects = document.querySelectorAll('.filter-select');
        this.resourcesGrid = document.querySelector('.resources-grid');
        this.statsContainer = document.querySelector('.resource-stats');
    }

    bindEvents() {
        // تفعيل عناصر التصفية
        this.filterSelects.forEach(select => {
            select.addEventListener('change', () => this.applyFilters());
        });

        // تفعيل بطاقات الموارد
        if (this.resourcesGrid) {
            this.resourcesGrid.addEventListener('click', (e) => {
                const card = e.target.closest('.resource-card');
                if (card) {
                    this.handleResourceClick(card);
                }
            });
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/legal-resources/stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateStats(data.stats);
            }
        } catch (error) {
            console.error('خطأ في تحميل الإحصائيات:', error);
        }
    }

    updateStats(stats) {
        if (this.statsContainer) {
            this.statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${stats.totalResources}</div>
                    <div class="stat-label">إجمالي الموارد</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.activeUsers}</div>
                    <div class="stat-label">مستخدم نشط</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.downloads}</div>
                    <div class="stat-label">تحميل</div>
                </div>
            `;
        }
    }

    async applyFilters() {
        const filters = {};
        this.filterSelects.forEach(select => {
            filters[select.name] = select.value;
        });

        try {
            const response = await fetch('/api/legal-resources/filter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(filters)
            });

            const data = await response.json();
            
            if (data.success) {
                this.updateResourcesGrid(data.resources);
            } else {
                this.showError('خطأ في تطبيق عوامل التصفية');
            }
        } catch (error) {
            this.showError('خطأ في الاتصال بالخادم');
        }
    }

    async handleResourceClick(card) {
        const resourceId = card.dataset.id;
        const action = event.target.dataset.action;

        if (!resourceId || !action) return;

        try {
            switch (action) {
                case 'view':
                    await this.viewResource(resourceId);
                    break;
                case 'download':
                    await this.downloadResource(resourceId);
                    break;
                case 'save':
                    await this.saveResource(resourceId);
                    break;
            }
        } catch (error) {
            this.showError('حدث خطأ في معالجة الطلب');
        }
    }

    async viewResource(resourceId) {
        try {
            const response = await fetch(`/api/legal-resources/${resourceId}`);
            const data = await response.json();
            
            if (data.success) {
                this.showResourceModal(data.resource);
            } else {
                this.showError('لا يمكن عرض المورد في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة عرض المورد');
        }
    }

    async downloadResource(resourceId) {
        try {
            const response = await fetch(`/api/legal-resources/download/${resourceId}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `resource-${resourceId}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            } else {
                this.showError('لا يمكن تحميل المورد في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة تحميل المورد');
        }
    }

    async saveResource(resourceId) {
        try {
            const response = await fetch(`/api/legal-resources/save/${resourceId}`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                this.showSuccess('تم حفظ المورد بنجاح');
            } else {
                this.showError('لا يمكن حفظ المورد في الوقت الحالي');
            }
        } catch (error) {
            this.showError('حدث خطأ أثناء محاولة حفظ المورد');
        }
    }

    updateResourcesGrid(resources) {
        if (this.resourcesGrid) {
            this.resourcesGrid.innerHTML = resources.map(resource => `
                <div class="resource-card" data-id="${resource.id}">
                    <span class="resource-type">${resource.type}</span>
                    <div class="resource-content">
                        <h3 class="resource-title">${resource.title}</h3>
                        <p class="resource-description">${resource.description}</p>
                        <div class="resource-meta">
                            <span class="meta-item">
                                <i class="fas fa-calendar"></i>
                                ${resource.date}
                            </span>
                            <span class="meta-item">
                                <i class="fas fa-download"></i>
                                ${resource.downloads}
                            </span>
                        </div>
                        <div class="resource-actions">
                            <a href="#" class="action-button primary" data-action="view">
                                <i class="fas fa-eye"></i> عرض
                            </a>
                            <a href="#" class="action-button secondary" data-action="download">
                                <i class="fas fa-download"></i> تحميل
                            </a>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    }

    showResourceModal(resource) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h2>${resource.title}</h2>
                <div class="resource-details">
                    ${resource.content}
                </div>
                <div class="modal-actions">
                    <button class="action-button primary" data-action="download">تحميل</button>
                    <button class="action-button secondary modal-close">إغلاق</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });
    }

    showSuccess(message) {
        // يمكن استخدام مكتبة للإشعارات مثل toastr
        alert(message);
    }

    showError(message) {
        // يمكن استخدام مكتبة للإشعارات مثل toastr
        alert(message);
    }
}

// تهيئة صفحة الموارد القانونية عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new LegalResources();
});
