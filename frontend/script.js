// Select DOM elements
const form = document.getElementById('textForm');
const textArea = document.getElementById('largeText');
const responseMessage = document.getElementById('responseMessage');

// API URL
const apiUrl = "https://localhost";

// Mock data for demonstration
const mockData = [
    { id: 1, name: "John Doe", age: 30 },
    { id: 2, name: "Jane Smith", age: 25 },
    { id: 3, name: "Alice Johnson", age: 35 }
];

// Event listener for form submission
form.addEventListener('submit', handleSubmit);

/**
 * Handles the form submission event.
 * @param {Event} event 
 */
function handleSubmit(event) {
    event.preventDefault();
    const text = textArea.value.trim();

    if (!validateInput(text)) {
        showMessage("Please enter some text!", "alert-danger");
        return;
    }

    submitTextToApi(text);
}

/**
 * Validates the user input.
 * @param {string} text - The input text to validate.
 * @returns {boolean} - True if input is valid, false otherwise.
 */
function validateInput(text) {
    return text.length > 0;
}

/**
 * Submits the text to the API.
 * @param {string} text - The input text to send to the API.
 */
async function submitTextToApi(text) {
    try {
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
    }
}

/**
 * Displays a message to the user.
 * @param {string} message - The message to display.
 * @param {string} alertClass - The Bootstrap alert class (e.g., 'alert-success').
 */
function showMessage(message, alertClass) {
    responseMessage.textContent = message;
    responseMessage.className = `alert ${alertClass}`;
    responseMessage.classList.remove('d-none');
}

/**
 * Replaces the form with a table displaying data.
 * @param {Array<Object>} data - The data to display in the table.
 */
function displayDataInTable(data) {
    // Clear the form content
    const container = form.parentElement;
    container.innerHTML = "";

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

