const {
    isInputEmpty,
    validateTextLength,
    updateSubmitState,
    handleSubmit,
    showMessage,
    displayDataInTable,
} = require('./script.js');

describe('Form Validation Tests', () => {
    let textArea, fileInput, submitButton, responseMessage, form;

    beforeEach(() => {
        // Set up a DOM mock
        document.body.innerHTML = `
        <div class="container mt-5">
            <form id="textForm">
                <div class="mb-3">
                    <textarea id="largeText" class="form-control" rows="10"></textarea>
                </div>
                <div class="mb-3">
                    <input type="file" class="form-control" id="fileUpload" accept=".txt,.pdf,.docx,.doc">
                </div>
                <button id="submitButton" class="btn btn-primary w-100" disabled></button>
                <div id="responseMessage" class="alert mt-4 d-none"></div>
            </form>
        </div>`;

        textArea = document.getElementById('largeText');
        fileInput = document.getElementById('fileUpload');
        submitButton = document.getElementById('submitButton');
        responseMessage = document.getElementById('responseMessage');
        form = document.getElementById('textForm');
    });

    test('isInputEmpty should return true if both text and file are empty', () => {
        expect(isInputEmpty(textArea, fileInput)).toBe(true);

        textArea.value = 'Sample text';
        expect(isInputEmpty(textArea, fileInput)).toBe(false);

        textArea.value = '';
        const file = new File(['dummy content'], 'example.txt', { type: 'text/plain' });
        Object.defineProperty(fileInput, 'files', {
            value: [file],
            writable: false,
        });
        expect(isInputEmpty(textArea, fileInput)).toBe(false);
    });

    test('validateTextLength should validate text length correctly', () => {
        textArea.value = 'Valid text';
        expect(validateTextLength(textArea)).toBe(true);

        textArea.value = ''.padStart(5001, 'a');
        expect(validateTextLength(textArea)).toBe(false);

        textArea.value = '';
        expect(validateTextLength(textArea)).toBe(false);
    });


    test('updateSubmitState should enable or disable submit button', () => {
        // Initially disabled
        updateSubmitState(textArea,fileInput,submitButton);
        expect(submitButton.disabled).toBe(true);

        // Enable button if text is valid
        textArea.value = 'Valid text';
        updateSubmitState(textArea,fileInput,submitButton);
        expect(submitButton.disabled).toBe(false);

        // Disable if text is too long
        textArea.value = ''.padStart(5001, 'a');
        updateSubmitState(textArea,fileInput,submitButton);
        expect(submitButton.disabled).toBe(true);
    });

    test('handleSubmit should prevent submission with empty input', () => {
        const mockEvent = { preventDefault: jest.fn() };
        handleSubmit(mockEvent,textArea,fileInput,responseMessage);
        expect(mockEvent.preventDefault).toHaveBeenCalled();
        expect(responseMessage.textContent).toBe('Please enter some text or upload a file!');
    });
});

