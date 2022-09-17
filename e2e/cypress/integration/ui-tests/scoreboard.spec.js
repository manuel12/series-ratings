/// <reference types="cypress" />

let testData = require("../../fixtures/test-data.json");
let series = testData.map((serie) => serie.title);

const nonExistantSeries = [
  // "Return of Buffy of Thrones",
  // "Breaking Anatomy Bones Wire",
  "North South Mirror Boys",
  "Stranger True Twilight Zone",
  "Better Call Breaking MacGyver",
];

const testAllScoreValues = (imdbScore, tomatometerScore, audienceScore) => {
  cy.get("[data-test=imdb-header]")
    .should("be.visible")
    .and("contain.text", "IMDb");

  cy.get("[data-test=imdb-score-value]")
    .should("be.visible")
    .and("contain.text", imdbScore);

  cy.get("[data-test=rottentomatoes-header]")
    .should("be.visible")
    .and("contain.text", "Rotten Tomatoes");

  cy.get("[data-test=tomatometer-header]")
    .should("be.visible")
    .and("contain.text", "Tomatometer");

  cy.get("[data-test=tomatometer-value]")
    .should("be.visible")
    .and("contain.text", tomatometerScore);

  cy.get("[data-test=audience_score-header]")
    .should("be.visible")
    .and("contain.text", "Audience Score");

  cy.get("[data-test=audience_score-value]")
    .should("be.visible")
    .and("contain.text", audienceScore);
};

describe("Scoreboard - Search results tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it(`should display current serie Title, IMDb and Rottentoes data for serie: ${series[serie]}`, () => {
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();
      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", currentTestData.title);

      testAllScoreValues(
        currentTestData.imdb,
        currentTestData.rt.tomatometer,
        currentTestData.rt.audience_score
      );
    });
  }
});

describe("Scoreboard - Using intercept tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it(`should display current serie Title, IMDb and Rottentoes data for serie: ${series[serie]}`, () => {
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", currentTestData.title);

      testAllScoreValues(
        currentTestData.imdb,
        currentTestData.rt.tomatometer,
        currentTestData.rt.audience_score
      );
    });
  }
});

describe("Scoreboard - Loading icons test", () => {
  for (const serie in series) {
    it(`should show loading icons before data is fetched for serie: ${series[serie]}`, () => {
      cy.intercept(`${Cypress.config("baseUrl")}api/*`, {});
      cy.visit("/");
      cy.get("#id_search").type(serie);
      cy.get("[data-test=search-button]").should("be.visible").click();
      cy.get("[data-test=imdb-score-value] > .spinner-border").should("be.visible");
      cy.get("[data-test=tomatometer-value] > .spinner-border").should("be.visible");
      cy.get("[data-test=audience_score-value] > .spinner-border").should("be.visible");
    });
  }
});

describe("Scoreboard - Parcial data tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it(`should display N/A for imdb score data and rottentomatoes data for serie: ${series[serie]}`, () => {
      cy.log(currentTestData)
      console.log(currentTestData);
      const currentTestDataNoIMDB = Object.assign({}, currentTestData);
      currentTestDataNoIMDB["imdb"] = "N/A";
      console.log(currentTestDataNoIMDB)

      cy.intercept(
        `${Cypress.config("baseUrl")}api/*`,
        currentTestDataNoIMDB
      );
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      testAllScoreValues(
        "N/A",
        currentTestDataNoIMDB.rt.tomatometer,
        currentTestDataNoIMDB.rt.audience_score
      );
    });

    it(`should display score data for imdb score data and N/A for rottentomatoes data for serie: ${series[serie]}`, () => {
      const currentTestDataNoRT = Object.assign({}, currentTestData);
      currentTestDataNoRT["rt"]["tomatometer"] = "N/A";
      currentTestDataNoRT["rt"]["audience_score"] = "N/A";

      cy.intercept(
        `${Cypress.config("baseUrl")}api/*`,
        currentTestDataNoRT
      );
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      testAllScoreValues(currentTestDataNoRT.imdb, "N/A", "N/A");
    });
  }
});
