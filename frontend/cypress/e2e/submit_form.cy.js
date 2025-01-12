describe('Submit Text or File to API', () => {

    beforeEach(() => {
        // Visit the page before each test
        cy.visit('http://localhost:3000/')
    });
    
    it('should display the form elements correctly', () => {
    // Check if form elements are present on the page
    cy.get('#largeText').should('exist'); // Textarea for large text
    cy.get('#fileUpload').should('exist'); // File upload input
    cy.get('#submitButton').should('exist'); // Submit button
    });

    // it('should submit text input and show a success message', () => {
    // // Type into the textarea field
    // cy.get('#largeText').type('This is some text input for testing.');

    // // Mocking an API request (this assumes that the request goes to "/api/submit")
    // cy.intercept('POST', '/api/submit', {
    //     statusCode: 200,
    //     body: { message: 'Text processed successfully' },
    // }).as('submitText');

    // // Submit the form
    // cy.get('#textForm').submit();

    // // Wait for the API response
    // cy.wait('@submitText');

    // // Verify the response message appears
    // cy.get('#responseMessage')
    //     .should('be.visible')
    //     .should('contain.text', 'Text processed successfully');
    // });
});