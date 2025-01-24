// Utility Functions
const showLoading = () => {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    document.body.appendChild(spinner);
};

const hideLoading = () => {
    const spinner = document.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
};

const showAlert = (message, type = 'success') => {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    const container = document.querySelector('.main-content') || document.body;
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
};

// Form Validation
const validateForm = (form) => {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            showAlert(`الرجاء تعبئة حقل ${input.getAttribute('placeholder')}`, 'error');
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
};

// API Calls
const apiCall = async (url, method = 'GET', data = null) => {
    showLoading();
    
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'حدث خطأ ما');
        }
        
        return result;
    } catch (error) {
        showAlert(error.message, 'error');
        throw error;
    } finally {
        hideLoading();
    }
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Handle Form Submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
    
    // Handle Navigation Active State
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Export Functions
window.utils = {
    showLoading,
    hideLoading,
    showAlert,
    validateForm,
    apiCall
};
