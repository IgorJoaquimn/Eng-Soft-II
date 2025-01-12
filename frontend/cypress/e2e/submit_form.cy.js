describe('Submit Text or File to API', () => {

    beforeEach(() => {
        // Visit the page before each test
        cy.visit('http://localhost:3000/')
    });
    
    it('displays the response data in the responseContainer', () => {
        cy.get('#largeText').type('This is a sample text for submission.');
      
        const mockResponse = {
          section1: { key1: 'value1', key2: 'value2' },
          section2: { key3: 'value3', key4: 'value4' },
        };
      
        cy.intercept('POST', '/api/submit', {
          statusCode: 200,
          body: mockResponse,
          headers: { 'Content-Type': 'application/json' },
        });
      
        cy.get('#submitButton').click();
      
        // Check if the responseContainer is displayed
        cy.get('#responseContainer').should('exist');
      
        // Check if section headers are present
        cy.get('#responseContainer h3').should('have.length', Object.keys(mockResponse).length);
      
        // Check if the contents match the mock response
        Object.entries(mockResponse).forEach(([section, content]) => {
          cy.get('#responseContainer').contains(section);
          Object.entries(content).forEach(([key, value]) => {
            cy.get('#responseContainer').contains(key);
            cy.get('#responseContainer').contains(value);
          });
        });
      });
    
});