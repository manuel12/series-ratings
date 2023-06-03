/// <reference types="cypress" />

let testData = require("../../fixtures/test-data.json");
let series = testData;

const testAllScoreValues = (imdbScore, tomatometerScore, audienceScore) => {
  cy.get("[data-test=imdb-header]")
    .should("be.visible")
    .and("contain.text", "IMDb");

  if (imdbScore == null) {
    cy.get("[data-test=imdb-score-value]")
      .should("be.visible")
      .and("contain.text", "N/A");
  } else {
    cy.get("[data-test=imdb-score-value]")
      .should("be.visible")
      .then((elem) => {
        const elemText = elem.text();
        const elemImdbScore = Number(elemText.replace("/10", ""));
        expect(imdbScore).to.be.closeTo(elemImdbScore, 1);
      });
  }

  cy.get("[data-test=rottentomatoes-header]")
    .should("be.visible")
    .and("contain.text", "Rotten Tomatoes");

  cy.get("[data-test=tomatometer-header]")
    .should("be.visible")
    .and("contain.text", "Tomatometer");

  if (tomatometerScore == null) {
    cy.get("[data-test=tomatometer-value]")
      .should("be.visible")
      .and("contain.text", "N/A");
  } else {
    cy.get("[data-test=tomatometer-value]")
      .should("be.visible")
      .then((elem) => {
        const elemText = elem.text();
        const elemTomatometerScore = Number(elemText.replace("%", ""));
        expect(tomatometerScore).to.be.closeTo(elemTomatometerScore, 1);
      });
  }

  cy.get("[data-test=audience_score-header]")
    .should("be.visible")
    .and("contain.text", "Audience Score");

  if (audienceScore == null) {
    cy.get("[data-test=audience_score-value]")
      .should("be.visible")
      .and("contain.text", "N/A");
  } else {
    cy.get("[data-test=audience_score-value]")
      .should("be.visible")
      .then((elem) => {
        const elemAudienceScore = Number(elem.text().replace("%", ""));
        expect(audienceScore).to.be.closeTo(elemAudienceScore, 1);
      });
  }
};

describe("Scoreboard - Search results tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it.only(`should display current serie Title, IMDb and Rottentoes data for serie: ${currentTestData.title}`, () => {
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();
      cy.get("[data-test=media-title]").should("be.visible");
      //.and("contain.text", currentTestData.title);

      testAllScoreValues(
        currentTestData.data.imdb,
        currentTestData.data.rt.tomatometer,
        currentTestData.data.rt.audience_score
      );
    });
  }
});

describe("Scoreboard - Using intercept tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it(`should display current serie Title, IMDb and Rottentoes data for serie: ${currentTestData.title}`, () => {
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      cy.get("[data-test=media-title]").should("be.visible");
      //.and("contain.text", currentTestData.title);

      testAllScoreValues(
        currentTestData.data.imdb,
        currentTestData.data.rt.tomatometer,
        currentTestData.data.rt.audience_score
      );
    });
  }
});

describe("Scoreboard - Loading icons test", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];
    it(`should show loading icons before data is fetched for serie: ${currentTestData.title}`, () => {
      cy.intercept(`${Cypress.config("baseUrl")}api/*`, {});
      cy.visit("/");
      cy.get("#id_search").type(serie);
      cy.get("[data-test=search-button]").should("be.visible").click();
      cy.get("[data-test=imdb-score-value] > .spinner-border").should(
        "be.visible"
      );
      cy.get("[data-test=tomatometer-value] > .spinner-border").should(
        "be.visible"
      );
      cy.get("[data-test=audience_score-value] > .spinner-border").should(
        "be.visible"
      );
    });
  }
});

describe("Scoreboard - Parcial data tests", () => {
  for (const serie in series) {
    const currentTestData = testData[serie];

    it(`should display N/A for imdb score data and rottentomatoes data for serie: ${currentTestData.title}`, () => {
      cy.intercept(`${Cypress.config("baseUrl")}api/*`, {
        title: currentTestData.title,
        data: {
          imdb: null,
          rt: {
            tomatometer: currentTestData.data.rt.tomatometer,
            audience_score: currentTestData.data.rt.audience_score,
          },
        },
      });
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      testAllScoreValues(
        null,
        currentTestData.data.rt.tomatometer,
        currentTestData.data.rt.audience_score
      );
    });

    it(`should display score data for imdb score data and N/A for rottentomatoes data for serie: ${currentTestData.title}`, () => {
      cy.intercept(`${Cypress.config("baseUrl")}api/*`, {
        title: currentTestData.title,
        data: {
          imdb: currentTestData.data.imdb,
          rt: {
            tomatometer: null,
            audience_score: null,
          },
        },
      });
      cy.visit("/");
      cy.get("#id_search").type(currentTestData.title);
      cy.get("[data-test=search-button]").should("be.visible").click();

      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      testAllScoreValues(currentTestData.data.imdb, null, null);
    });
  }
});
