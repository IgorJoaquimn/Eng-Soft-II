const { validateInput, showMessage, displayDataInTable } = require('./script');

// Mock DOM environment for testing
document.body.innerHTML = `
  <div id="container">
    <form id="textForm">
      <textarea id="largeText"></textarea>
      <button type="submit">Submit</button>
    </form>
    <div id="responseMessage" class="d-none"></div>
  </div>
`;

// Helper to reset DOM elements between tests
const resetDOM = () => {
    document.getElementById('largeText').value = '';
    const responseMessage = document.getElementById('responseMessage');
    responseMessage.textContent = '';
    responseMessage.className = 'd-none';
    document.getElementById('container').innerHTML = `
      <form id="textForm">
        <textarea id="largeText"></textarea>
        <button type="submit">Submit</button>
      </form>
    `;
};

describe('script.js Unit Tests', () => {
    afterEach(() => {
        resetDOM();
    });

    test('validateInput returns true for non-empty input', () => {
        expect(validateInput('Hello')).toBe(true);
    });

    test('validateInput returns false for empty input', () => {
        expect(validateInput('')).toBe(false);
    });

    test('showMessage displays success message correctly', () => {
        const message = 'Submission successful!';
        showMessage(message, 'alert-success');

        const responseMessage = document.getElementById('responseMessage');
        expect(responseMessage.textContent).toBe(message);
        expect(responseMessage.className).toContain('alert-success');
        expect(responseMessage.className).not.toContain('d-none');
    });

    test('showMessage displays error message correctly', () => {
        const message = 'An error occurred!';
        showMessage(message, 'alert-danger');

        const responseMessage = document.getElementById('responseMessage');
        expect(responseMessage.textContent).toBe(message);
        expect(responseMessage.className).toContain('alert-danger');
        expect(responseMessage.className).not.toContain('d-none');
    });

    test('displayDataInTable replaces the form with a table', () => {
        const mockData = [
            { id: 1, name: 'John Doe', age: 30 },
            { id: 2, name: 'Jane Smith', age: 25 },
        ];

        displayDataInTable(mockData);

        const container = document.getElementById('container');
        expect(container.querySelector('form')).toBeNull(); // Form should be removed
        const table = container.querySelector('table');
        expect(table).not.toBeNull(); // Table should be created

        // Check table content
        const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
        expect(headers).toEqual(['Id', 'Name', 'Age']);

        const rows = Array.from(table.querySelectorAll('tbody tr'));
        expect(rows).toHaveLength(mockData.length);

        rows.forEach((row, index) => {
            const cells = Array.from(row.querySelectorAll('td')).map(td => td.textContent);
            expect(cells).toEqual(Object.values(mockData[index]).map(String));
        });
    });
});

