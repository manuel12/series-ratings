/// <reference types="cypress" />

describe("Search tests", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("should NOT allow search to proceed with empty input value", () => {
    cy.get("[data-test=search-button]").click();
    cy.get("[data-test=search-container]").should("be.visible");
  });

  it("should NOT allow search to proceed with blank spaces as input value", () => {
    cy.get("[type=text]").type("{shift} {shift} {shift} ");
    cy.get("[data-test=search-container]").should("be.visible");
  });

  it("should redirect to search page after clicking on header text", () => {
    cy.get("[type=text]").type("Stranger Things");
    cy.get("[data-test=search-button]").click();
    cy.get("[data-test=scoreboard-container]").should("be.visible");
    cy.get("[data-test=header-text]").click();
    cy.get("[data-test=search-container]").should("be.visible");
  });

  it("should redirect to successful scoreboard page with 'Stranger Things' input value", () => {
    cy.get("[type=text]").type("Stranger Things");
    cy.get("[data-test=search-button]").click();
    cy.get("[data-test=scoreboard-container]").should("be.visible");
  });
});
