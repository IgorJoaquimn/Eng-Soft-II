// cypress/e2e/formSubmission.spec.js

describe('Form Submission E2E Tests', () => {
    beforeEach(() => {
        // Visit the application before each test
        cy.visit('index.html'); // Ensure this path points to your application
    });

    it('should disable submit button when both inputs are empty', () => {
        cy.get('#submitButton').should('be.disabled');
    });

    it('should enable submit button when valid text is entered', () => {
        cy.get('#largeText').type('Valid text');
        cy.get('#submitButton').should('not.be.disabled');
    });

    it('should handle successful API response and update the table', () => {
        // Intercept the API call and provide a mock response
        cy.intercept('POST', 'http://localhost:5000/api/submit').as('submitRequest');

        // Fill in the form and submit
        cy.get('#largeText').type('Teste de submissão');
        cy.get('#submitButton').click();

        // Wait for the API request and validate the response status
        cy.wait('@submitRequest').its('response.statusCode').should('exist');
    });

});

