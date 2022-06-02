/// <reference types="cypress" />

describe("Search tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should NOT allow search to proceed with empty input value", () => {
    cy.get("[data-test=search-button]").click();
    cy.url().should("eq", "http://localhost:8000/");
    cy.get("[data-test=search-form]").should("be.visible");
  });

  it("should NOT allow search to proceed with blank spaces as input value", () => {
    cy.get("[type=text]").type("{shift} {shift} {shift} ");
    cy.url().should("eq", "http://localhost:8000/");
    cy.get("[data-test=search-form]").should("be.visible");
  });

  it("should redirect to search page after clicking on header", () => {
    cy.get("[type=text]").type("Stranger Things");
    cy.get("[data-test=search-button]").click();
    cy.url().should("eq", "http://localhost:8000/results/");
    cy.get("[data-test=header]").click();
  });

  it("should redirect to successful results page with 'Stranger Things' input value", () => {
    cy.get("[type=text]").type("Stranger Things");
    cy.get("[data-test=search-button]").click();
    cy.url().should("eq", "http://localhost:8000/results/");
  });
});
