const { JSDOM } = require('jsdom');

// Set up the mock DOM environment using jsdom
const { window } = new JSDOM(`
  <!DOCTYPE html>
  <html>
    <body>
      <div id="container">
        <form id="textForm">
          <textarea id="largeText"></textarea>
          <input type="file" id="fileUpload">
          <button type="submit" id="submitButton" disabled>Submit</button>
        </form>
        <div id="responseMessage" class="d-none"></div>
      </div>
      <script src="script.js"></script>
    </body>
  </html>
`);

const { document } = window;

// Mock global document and window
global.document = document;
global.window = window;

// Import the functions to be tested
const {
  validateInput,
  showMessage,
  displayDataInTable,
  isInputEmpty,
  validateTextLength,
  updateSubmitState,
  handleSubmit,
} = require('./script');

// Helper function to reset DOM elements between tests
const resetDOM = () => {
  document.getElementById('largeText').value = '';
  const responseMessage = document.getElementById('responseMessage');
  responseMessage.textContent = '';
  responseMessage.className = 'd-none';
  document.getElementById('container').innerHTML = `
    <form id="textForm">
      <textarea id="largeText"></textarea>
      <input type="file" id="fileUpload">
      <button type="submit" id="submitButton" disabled>Submit</button>
    </form>
    <div id="responseMessage" class="d-none"></div>
  `;
};

describe('script.js Unit Tests', () => {
  beforeAll(() => { 
      const form = document.querySelector('textForm');
      form.addEventListener('submit', handleSubmit);
    
  });

  beforeEach(() => {
    // Reinitialize the DOM and reset everything before each test
    resetDOM();
  });

  afterEach(() => {
    resetDOM();
  });

  test('validateInput returns true for non-empty input', () => {
    document.getElementById('largeText').value = 'Hello';
    expect(validateInput('Hello')).toBe(true);
  });

  test('validateInput returns false for empty input', () => {
    document.getElementById('largeText').value = '';
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

  test('isInputEmpty returns true when both textarea and file input are empty', () => {
    document.getElementById('largeText').value = '';
    document.getElementById('fileUpload').files = [];
    expect(isInputEmpty()).toBe(true);
  });

  test('isInputEmpty returns false when textarea has text', () => {
    document.getElementById('largeText').value = 'Some text';
    document.getElementById('fileUpload').files = [];
    expect(isInputEmpty()).toBe(false);
  });

  test('isInputEmpty returns false when file input has file', () => {
    const file = new File(['dummy content'], 'example.txt', { type: 'text/plain' });
    document.getElementById('largeText').value = '';
    document.getElementById('fileUpload').files = [file];
    expect(isInputEmpty()).toBe(false);
  });

  test('validateTextLength returns true for valid text length', () => {
    document.getElementById('largeText').value = 'Some text';
    expect(validateTextLength()).toBe(true);
  });

  test('validateTextLength returns false for empty text', () => {
    document.getElementById('largeText').value = '';
    expect(validateTextLength()).toBe(false);
  });

  test('updateSubmitState disables submit button when input is empty', () => {
    document.getElementById('largeText').value = '';
    document.getElementById('fileUpload').files = [];
    updateSubmitState();
    const submitButton = document.getElementById('submitButton');
    expect(submitButton.disabled).toBe(true);
  });

  test('updateSubmitState enables submit button when text is valid', () => {
    document.getElementById('largeText').value = 'Some valid text';
    document.getElementById('fileUpload').files = [];
    updateSubmitState();
    const submitButton = document.getElementById('submitButton');
    expect(submitButton.disabled).toBe(false);
  });

  test('displayDataInTable replaces form with a table', () => {
    const mockData = [
      { id: 1, name: 'John Doe', age: 30 },
      { id: 2, name: 'Jane Smith', age: 25 },
    ];

    displayDataInTable(mockData);

    const container = document.getElementById('container');
    expect(container.querySelector('form')).toBeNull(); // Form should be removed
    const table = container.querySelector('table');
    expect(table).not.toBeNull(); // Table should be created

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
