/// <reference types="cypress" />

describe("Search tests", () => {
  beforeEach(() => {
    cy.visit("/");

    cy.get("[type=text]").type("Stranger Things");
    cy.get("[data-test=search-button]").click();
    cy.url().should("eq", "http://localhost:8000/results/");
    cy.get("[data-test=canvas-container]").should("be.visible").wait(1000);
  });

  it("should display correct(visual test) results chart", () => {
    cy.get("[data-test=chart]").should("be.visible").matchImageSnapshot();
  });
});
