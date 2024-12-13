// Select DOM elements
const form = document.getElementById('textForm');
const textArea = document.getElementById('largeText');
const fileInput = document.getElementById('fileUpload');
const submitButton = document.getElementById('submitButton');
const responseMessage = document.getElementById('responseMessage');

<<<<<<< HEAD
// API URL
const apiUrl = "https://localhost";
=======
const MAX_TEXT_LENGTH = 5000; // Example: 5000 characters max
const MIN_TEXT_LENGTH = 0;
>>>>>>> d3c2bc23503302ef0f56a88ed4854df32d3cfab3

// Mock data for demonstration
const mockData = [
    { id: 1, name: "John Doe", age: 30 },
    { id: 2, name: "Jane Smith", age: 25 },
    { id: 3, name: "Alice Johnson", age: 35 }
];

/**
 * Checks if the input is empty (no text and no file)
 * @returns {boolean}
 */
function isInputEmpty() {
    const text = textArea.value.trim();
    const file = fileInput.files[0];

    return text.length === 0 && !file;
}

/**
 * Validates text input length
 * @returns {boolean}
 */
function validateTextLength() {
    const text = textArea.value.trim();
    return text.length > 0 && text.length <= MAX_TEXT_LENGTH;
}

/**
 * Updates submit button state and text area styling
 */
function updateSubmitState() {
    let isValid = true;

    // Check if input is empty
    if (isInputEmpty()) {
        submitButton.disabled = true;
        isValid = false;
    }

    // Check text length if text exists
    if (textArea.value.trim().length > 0) {
        if (textArea.value.trim().length > MAX_TEXT_LENGTH) {
            textArea.classList.add('is-invalid');
            submitButton.disabled = true;
            isValid = false;
        } else {
            textArea.classList.remove('is-invalid');
        }
    }

    // Enable submit if file is selected or text is valid
    if (fileInput.files[0] || validateTextLength()) {
        submitButton.disabled = false;
        isValid = true;
    }

    return isValid;
}

/**
 * Handles the form submission event.
 * @param {Event} event 
 */
function handleSubmit(event) {
    event.preventDefault();
    
    // Prepare form data
    const formData = new FormData();

    const text = textArea.value.trim();
    const file = fileInput.files[0];


    if (isInputEmpty()) {
        showMessage("Please enter some text or upload a file!", "alert-danger");
        return;
    }

    if (file) {
        formData.append('file', file);
        submitTextToApi(formData);
    }
    else if (validateTextLength(text)) {
        formData.append('text', text);
        submitTextToApi(formData);
    }
    else {
        showMessage("Some error occurred", "alert-danger");
    }
}

// Event listener for form submission
form.addEventListener('submit', handleSubmit);

function buildRequestFromFormData(formData) {
    const text = formData.get('text');
    const file = formData.get('file');

    if (file) {
        return {
            method: 'Post',
            headers: { 'Content-Type': 'multipart/form-data' },
            body: formData
        }
    }

    if (text) {
        return {
            method: 'Post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"text": text })
        }
    }

    throw new Error('No content to submit');
}

async function submitTextToApi(formData) {
    try {
<<<<<<< HEAD
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        if (response.ok) {
            showMessage("Text submitted successfully!", "alert-success");
            displayDataInTable(mockData); // Replace form with mock table
        } else {
            showMessage(`Error: ${response.statusText}`, "alert-danger");
            displayDataInTable(mockData); // Replace form with mock table
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, "alert-danger");
        displayDataInTable(mockData); // Replace form with mock table
=======
        const request = buildRequestFromFormData(formData);

        console.log(request)

        const response = await fetch('http://localhost:5000/api/submit', request);

        if (response.ok) {
            const data = await response.json();
            showMessage("Submitted successfully!", "alert-success");
            displayDataInTable(JSON.parse(data));
        } else {
            const errorData = await response.json().catch(() => ({}));
            showMessage(`Error: ${errorData.message || response.statusText}`, "alert-danger");
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, "alert-danger");
>>>>>>> d3c2bc23503302ef0f56a88ed4854df32d3cfab3
    }
}

/**
 * Shows an error message
 * @param {string} message 
 * @param {string} type 
 */
function showMessage(message, type) {
    responseMessage.textContent = message;
    responseMessage.className = `alert ${type} d-block`;
    
    setTimeout(() => {
        responseMessage.className = 'alert mt-4 d-none';
    }, 7000);
}

form.addEventListener('submit', handleSubmit);

// Listen for input changes on textarea
textArea.addEventListener('input', () => {
    updateSubmitState();
});

// Listen for input changes on file input
fileInput.addEventListener('change', () => {
    updateSubmitState();
});

// Initial state setup
submitButton.disabled = true;


/**
 * Replaces the form with a table displaying data.
 * @param {Array<Object>} data - The data to display in the table.
 */
function displayDataInTableOld(data) {
    // Clear the form content
    const container = form.parentElement;
    // container.innerHTML = "";
    form.style.display = 'none';

    // Create table
    const table = document.createElement('table');
    table.className = "table table-striped mt-4";

    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create table body
    const tbody = document.createElement('tbody');
    data.forEach(item => {
        const row = document.createElement('tr');
        Object.values(item).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    container.appendChild(table);
}

function displayDataInTable(data) {
    const container = form.parentElement;
    const responseContainter = document.createElement('div');
    responseContainter.id = "responseContainer";
    form.style.display = 'none';
    container.appendChild(responseContainter);
  
    // Recursive function to create nested table structure
    function createNestedTable(obj) {
      // If it's not an object or is null, return the value as a string
      if (typeof obj !== 'object' || obj === null) {
        return document.createTextNode(String(obj));
      }
  
      // Create table for nested objects
      const table = document.createElement('table');
      table.className = 'w-full border-collapse mb-4';
  
      // Iterate through object entries
      Object.entries(obj).forEach(([key, value]) => {
        const row = table.insertRow();
        
        // Key column
        const keyCell = row.insertCell();
        keyCell.className = 'p-2 bg-gray-100 font-bold border';
        keyCell.textContent = key;
  
        // Value column
        const valueCell = row.insertCell();
        valueCell.className = 'p-2 border';
        
        // Recursively handle nested objects or simple values
        if (typeof value === 'object' && value !== null) {
          valueCell.appendChild(createNestedTable(value));
        } else {
          valueCell.textContent = String(value);
        }
      });
  
      return table;
    }
  
    // Create and append sections for each top-level key
    Object.entries(data).forEach(([section, content]) => {
      console.log(section, content)
      const sectionHeader = document.createElement('h3');
      sectionHeader.className = 'text-xl font-semibold mb-2 bg-gray-200 p-2 rounded';
      sectionHeader.textContent = section;
      responseContainter.appendChild(sectionHeader);
  
      // Section content
      const sectionContent = createNestedTable(content);
      responseContainter.appendChild(sectionContent);
    });
}

function returnHome() {
    const responseContainer = document.getElementsById('responseContainer');
    if (responseContainer) {
        responseContainer.remove();
    }
    form.style.display = 'block';
}
