/// <reference types="cypress" />

let mockData = require("../../fixtures/test-data.json");

const medias = [
  "Stranger Things",
  "South Park",
  "Alien",
  "Dawn of the Dead",
  "Poltergeist",
];

for (const media in medias) {
  let testData = mockData[media];

  describe("Scoreboard - Search results tests", () => {
    beforeEach(() => {
      cy.visit("/");
      cy.get("#id_search").type(testData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();
    });

    it("should display current media title", () => {
      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", testData.title);
    });

    it("should display current media imdb data", () => {
      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      cy.get("[data-test=imdb-score-value]")
        .should("be.visible")
        .and("contain.text", testData.imdb);
    });

    it("should display current media rottentomatoes data", () => {
      cy.get("[data-test=rottentomatoes-header]")
        .should("be.visible")
        .and("contain.text", "Rottentomatoes");

      cy.get("[data-test=tomatometer-header]")
        .should("be.visible")
        .and("contain.text", "Avg tomatometer");

      cy.get("[data-test=tomatometer-value]")
        .should("be.visible")
        .and("contain.text", testData.rt.tomatometer);

      cy.get("[data-test=audience_score-header]")
        .should("be.visible")
        .and("contain.text", "Avg audience score");

      cy.get("[data-test=audience_score-value]")
        .should("be.visible")
        .and("contain.text", testData.rt.audience_score);
    });
  });
}

for (const media in medias) {
  let testData = mockData[media];

  describe("Scoreboard - Using intercept tests", () => {
    beforeEach(() => {
      cy.intercept("http://localhost:8000/fetch-score-data/*", mockData[media]);
      cy.visit("/");
      cy.log(media);
      cy.get("#id_search").type(testData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();
    });

    it("should display current media title", () => {
      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", testData.title);
    });

    it("should display current media imdb data", () => {
      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      cy.get("[data-test=imdb-score-value]")
        .should("be.visible")
        .and("contain.text", testData.imdb);
    });

    it("should display current media rottentomatoes data", () => {
      cy.get("[data-test=rottentomatoes-header]")
        .should("be.visible")
        .and("contain.text", "Rottentomatoes");

      cy.get("[data-test=tomatometer-header]")
        .should("be.visible")
        .and("contain.text", "Avg tomatometer");

      cy.get("[data-test=tomatometer-value]")
        .should("be.visible")
        .and("contain.text", testData.rt.tomatometer);

      cy.get("[data-test=audience_score-header]")
        .should("be.visible")
        .and("contain.text", "Avg audience score");

      cy.get("[data-test=audience_score-value]")
        .should("be.visible")
        .and("contain.text", testData.rt.audience_score);
    });
  });
}

for (const media in medias) {
  describe("Scoreboard - Loading icons test", () => {
    before(() => {
      cy.intercept("http://localhost:8000/fetch-score-data/*", {});
      cy.visit("/");
      cy.get("#id_search").type(media);
      cy.get("[data-test=search-button]").should("be.visible").click();
    });

    it("should show loading icons before data is fetched", () => {
      cy.get("#imdb-score > .spinner-border").should("be.visible");
      cy.get("#tomatometer-value > .spinner-border").should("be.visible");
      cy.get("#audience_score-value > .spinner-border").should("be.visible");
    });
  });
}
