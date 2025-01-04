// التحقق المتقدم من النموذج
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // إعدادات التحقق المتقدمة
    const validationConfig = {
        'اسم الموظف': {
            regex: /^[\u0600-\u06FF\s]{2,50}$/,
            errorMessage: 'يجب أن يكون الاسم باللغة العربية (2-50 حرف)'
        },
        'اسم الشركة': {
            regex: /^[\u0600-\u06FF\s]{2,50}$/,
            errorMessage: 'يجب أن يكون اسم الشركة باللغة العربية (2-50 حرف)'
        },
        'المسمى الوظيفي': {
            regex: /^[\u0600-\u06FF\s]{2,50}$/,
            errorMessage: 'يجب أن يكون المسمى الوظيفي باللغة العربية (2-50 حرف)'
        },
        'مكان العمل': {
            regex: /^[\u0600-\u06FF\s]{2,50}$/,
            errorMessage: 'يجب أن يكون مكان العمل باللغة العربية (2-50 حرف)'
        },
        'الراتب الشهري': {
            min: 1000,
            max: 50000,
            errorMessage: 'يجب أن يكون الراتب بين 1000 و 50000'
        },
        'ساعات العمل الأسبوعية': {
            min: 4,
            max: 48,
            errorMessage: 'يجب أن تكون ساعات العمل بين 4 و 48 ساعة'
        }
    };

    // دالة إنشاء رسائل الخطأ المخصصة
    function createCustomErrorElement(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'custom-error-message text-danger small mt-1';
        errorDiv.textContent = message;
        return errorDiv;
    }

    // التحقق المتقدم من المدخلات
    function advancedValidation(input) {
        const inputName = input.name;
        const value = input.value.trim();
        const config = validationConfig[inputName];

        // إزالة رسائل الخطأ السابقة
        const existingError = input.parentNode.querySelector('.custom-error-message');
        if (existingError) {
            existingError.remove();
        }

        // التحقق من الحقول النصية
        if (config && config.regex) {
            if (value === '') {
                input.classList.remove('is-valid', 'is-invalid');
                return true;
            }

            if (config.regex.test(value)) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
                return true;
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
                const errorMessage = createCustomErrorElement(config.errorMessage);
                input.parentNode.appendChild(errorMessage);
                return false;
            }
        }

        // التحقق من الأرقام
        if (config && (config.min !== undefined || config.max !== undefined)) {
            const numValue = parseFloat(value);

            if (isNaN(numValue)) {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
                const errorMessage = createCustomErrorElement('يرجى إدخال رقم صحيح');
                input.parentNode.appendChild(errorMessage);
                return false;
            }

            if ((config.min !== undefined && numValue < config.min) || 
                (config.max !== undefined && numValue > config.max)) {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
                const errorMessage = createCustomErrorElement(config.errorMessage);
                input.parentNode.appendChild(errorMessage);
                return false;
            }

            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }

        // التحقق من التاريخ
        if (input.type === 'date') {
            const selectedDate = new Date(value);
            const today = new Date();
            const minDate = new Date();
            minDate.setFullYear(today.getFullYear() - 1); // تاريخ قبل سنة

            if (selectedDate > today || selectedDate < minDate) {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
                const errorMessage = createCustomErrorElement('يرجى اختيار تاريخ صالح');
                input.parentNode.appendChild(errorMessage);
                return false;
            }

            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }

        return true;
    }

    // معالجة النموذج بالكامل
    const form = document.getElementById('document-drafting-form');
    const inputs = form.querySelectorAll('input, select, textarea');

    // إضافة المستمعات للتحقق
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            advancedValidation(this);
        });

        input.addEventListener('blur', function() {
            advancedValidation(this);
        });
    });

    // منع إرسال النموذج إذا كانت هناك أخطاء
    form.addEventListener('submit', function(event) {
        let isFormValid = true;

        inputs.forEach(input => {
            if (!advancedValidation(input)) {
                isFormValid = false;
            }
        });

        if (!isFormValid) {
            event.preventDefault();
            
            // تنبيه مع رسالة مخصصة
            Swal.fire({
                icon: 'error',
                title: 'خطأ في النموذج',
                text: 'يرجى التأكد من صحة جميع المدخلات',
                confirmButtonText: 'حسنًا'
            });
        }
    });

    // إضافة مؤشر تقدم للنموذج
    function updateFormProgress() {
        const filledInputs = Array.from(inputs).filter(input => 
            input.value.trim() !== '' && input.classList.contains('is-valid')
        ).length;
        
        const progressPercentage = Math.round((filledInputs / inputs.length) * 100);
        
        // إنشاء شريط التقدم إذا لم يكن موجودًا
        let progressBar = document.getElementById('form-progress');
        if (!progressBar) {
            progressBar = document.createElement('div');
            progressBar.id = 'form-progress';
            progressBar.className = 'progress mt-3';
            progressBar.innerHTML = `
                <div class="progress-bar progress-bar-striped progress-bar-animated" 
                     role="progressbar" 
                     style="width: 0%">
                    0%
                </div>
            `;
            form.insertBefore(progressBar, form.lastElementChild);
        }

        const progressBarElement = progressBar.querySelector('.progress-bar');
        progressBarElement.style.width = `${progressPercentage}%`;
        progressBarElement.textContent = `${progressPercentage}%`;
        progressBarElement.classList.toggle('bg-success', progressPercentage === 100);
    }

    // تحديث شريط التقدم عند كل إدخال
    inputs.forEach(input => {
        input.addEventListener('input', updateFormProgress);
    });
});
