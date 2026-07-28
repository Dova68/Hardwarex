
        const steps = Array.from(document.querySelectorAll('.wizard-step'));
        const panels = Array.from(document.querySelectorAll('.step-panel'));
        const progressBar = document.getElementById('wizard-progress');
        const nextButton = document.getElementById('next-button');
        const prevButton = document.getElementById('prev-button');
        const submitButton = document.getElementById('submit-button');
        const formError = document.getElementById('form-error');

        let currentStep = 1;

        const fieldsByStep = {
            1: [
                document.getElementById('device-name'),
                document.getElementById('device-location'),
                document.getElementById('device-type')
            ],
            2: [
                document.getElementById('issue-type'),
                document.getElementById('urgency'),
                document.getElementById('description')
            ]
        };

        function showStep(step) {
            currentStep = step;
            panels.forEach(panel => panel.classList.toggle('active', Number(panel.dataset.step) === step));
            steps.forEach(stepElement => stepElement.classList.toggle('active', Number(stepElement.dataset.step) === step));
            prevButton.hidden = step === 1;
            nextButton.hidden = step === 3;
            submitButton.hidden = step !== 3;
            progressBar.style.width = `${((step - 1) / 2) * 100}%`;
            formError.textContent = '';
            if (step === 3) {
                fillSummary();
            }
            updateProgressFill();
        }

        function validateStep(step) {
            const requiredFields = fieldsByStep[step];
            for (const field of requiredFields) {
                if (!field.value.trim()) {
                    formError.textContent = 'Por favor completa todos los campos obligatorios antes de continuar.';
                    field.focus();
                    return false;
                }
            }
            formError.textContent = '';
            return true;
        }

        function updateProgressFill() {
            const currentFields = fieldsByStep[currentStep] || [];
            if (!currentFields.length) {
                return;
            }
            const filled = currentFields.filter(field => field.value.trim()).length;
            const percent = Math.round((filled / currentFields.length) * 100);
            progressBar.style.width = `${((currentStep - 1) / 2) * 100 + percent / 200 * 100}%`;
        }

        function fillSummary() {
            document.getElementById('summary-device').textContent = document.getElementById('device-name').value.trim() || 'No especificado';
            document.getElementById('summary-location').textContent = document.getElementById('device-location').value.trim() || 'No especificado';
            document.getElementById('summary-type').textContent = document.getElementById('device-type').value || 'No especificado';
            document.getElementById('summary-issue').textContent = document.getElementById('issue-type').value || 'No especificado';
            document.getElementById('summary-urgency').textContent = document.getElementById('urgency').value || 'No especificado';
            document.getElementById('summary-description').textContent = document.getElementById('description').value.trim() || 'No especificado';
            document.getElementById('summary-serial').textContent = document.getElementById('serial-number').value.trim() || 'No especificado';
        }

        nextButton.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                showStep(currentStep + 1);
            }
        });

        prevButton.addEventListener('click', () => {
            showStep(currentStep - 1);
        });

        document.getElementById('repair-form').addEventListener('submit', event => {
            event.preventDefault();
            if (validateStep(2)) {
                alert('Solicitud enviada correctamente. El técnico recibirá los datos.');
                showStep(1);
                document.getElementById('repair-form').reset();
                progressBar.style.width = '0%';
            }
        });

        Object.values(fieldsByStep).flat().forEach(field => {
            field.addEventListener('input', updateProgressFill);
            field.addEventListener('change', updateProgressFill);
        });

        showStep(currentStep);
