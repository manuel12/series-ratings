/// <reference types="cypress" />

describe("Search tests", () => {
    beforeEach(() => {
      cy.visit("/");
    });

    it("should send correct chart data(api test) for the chart", () => {
        cy.intercept("POST", "/results/").as("results");

        cy.get("[type=text]").type("Stranger Things");
        cy.get("[data-test=search-button]").click();

        cy.wait("@results").its("response.statusCode").should("eq", 200);
    })
  
  });
  