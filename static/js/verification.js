async function verifyStage(stageId, stageType) {
    const stageElement = document.getElementById(`stage-${stageId}`);
    const stageText = stageElement.querySelector('.stage-content').textContent;
    const verifyButton = stageElement.querySelector('.verify-button');
    const resultDiv = stageElement.querySelector('.verification-result');
    
    try {
        // تغيير حالة الزر أثناء التحقق
        verifyButton.disabled = true;
        verifyButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري التحقق...';
        
        const response = await fetch('/api/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: stageText,
                stage_type: stageType
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // تحديث واجهة المستخدم بناءً على النتيجة
            resultDiv.innerHTML = `
                <div class="alert ${data.is_matching ? 'alert-success' : 'alert-warning'} mt-3">
                    <h5 class="alert-heading">
                        ${data.is_matching ? 
                            '<i class="fas fa-check-circle text-success"></i> النص متطابق' : 
                            '<i class="fas fa-exclamation-triangle text-warning"></i> تم العثور على اختلاف'}
                    </h5>
                    <p>${data.result}</p>
                    <small class="text-muted">المصدر: ${data.source}</small>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger mt-3">
                    <i class="fas fa-times-circle"></i> حدث خطأ: ${data.error}
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger mt-3">
                <i class="fas fa-times-circle"></i> حدث خطأ أثناء التحقق
            </div>
        `;
    } finally {
        // إعادة الزر إلى حالته الطبيعية
        verifyButton.disabled = false;
        verifyButton.innerHTML = '<i class="fas fa-check"></i> تحقق من الدقة';
    }
} 