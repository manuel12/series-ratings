/// <reference types="cypress" />

let mockData = require("../../fixtures/mock-data.json");

const medias = [
  "stranger-things",
  "evil-dead-II",
  "alien",
  "dawn-of-the-dead",
  "poltergeist",
];

for (const media of medias) {
  let testData = media === "stranger-things" ? mockData[0] : mockData[1];

  describe("Scoreboard - Search results tests", () => {
    beforeEach(() => {
      cy.visit("/");
      cy.get("#id_search").type(media);
      cy.get("[data-test=search-button]").should("be.visible").click();
    });

    it("should display current media title", () => {
      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", testData.mediaTitle);
    });

    it("should display current media metacritic data", () => {
      cy.get("[data-test=metacritic-header]")
        .should("be.visible")
        .and("contain.text", "Metacritic");

      cy.get("[data-test=metascore-header]")
        .should("be.visible")
        .and("contain.text", "Metascore");

      cy.get("[data-test=metascore-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.metacritic.scores[0].scoreValue);

      cy.get("[data-test=user-score-header]")
        .should("be.visible")
        .and("contain.text", "Userscore");

      cy.get("[data-test=user-score-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.metacritic.scores[1].scoreValue);
    });

    it("should display current media imdb data", () => {
      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      cy.get("[data-test=imdb-score-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.imdb.scores[0].scoreValue);
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
        .and(
          "contain.text",
          testData.ratings.rottentomatoes.scores[0].scoreValue
        );

      cy.get("[data-test=audience_score-header]")
        .should("be.visible")
        .and("contain.text", "Avg audience score");

      cy.get("[data-test=audience_score-value]")
        .should("be.visible")
        .and(
          "contain.text",
          testData.ratings.rottentomatoes.scores[1].scoreValue
        );
    });
  });
}

for (const media in medias) {
  let testData = mockData[media];

  describe("Scoreboard - Using intercept tests", () => {
    beforeEach(() => {
      cy.log(media);

      cy.intercept("http://localhost:8000/scoreboard-data/*", mockData[media]);
      cy.visit("/scoreboard");
    });

    it("should display current media title", () => {
      cy.get("[data-test=media-title]")
        .should("be.visible")
        .and("contain.text", testData.mediaTitle);
    });

    it("should display current media metacritic data", () => {
      cy.get("[data-test=metacritic-header]")
        .should("be.visible")
        .and("contain.text", "Metacritic");

      cy.get("[data-test=metascore-header]")
        .should("be.visible")
        .and("contain.text", "Metascore");

      cy.get("[data-test=metascore-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.metacritic.scores[0].scoreValue);

      cy.get("[data-test=user-score-header]")
        .should("be.visible")
        .and("contain.text", "Userscore");

      cy.get("[data-test=user-score-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.metacritic.scores[1].scoreValue);
    });

    it("should display current media imdb data", () => {
      cy.get("[data-test=imdb-header]")
        .should("be.visible")
        .and("contain.text", "IMDb");

      cy.get("[data-test=imdb-score-value]")
        .should("be.visible")
        .and("contain.text", testData.ratings.imdb.scores[0].scoreValue);
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
        .and(
          "contain.text",
          testData.ratings.rottentomatoes.scores[0].scoreValue
        );

      cy.get("[data-test=audience_score-header]")
        .should("be.visible")
        .and("contain.text", "Avg audience score");

      cy.get("[data-test=audience_score-value]")
        .should("be.visible")
        .and(
          "contain.text",
          testData.ratings.rottentomatoes.scores[1].scoreValue
        );
    });
  });
}

describe("Scoreboard - Loading icons test", () => {
  before(() => {
    cy.visit("/scoreboard");
  })
  
  it("should show loading icons before data is fetcehd", () => {
    cy.get("#metascore-value > .fa-spinner").should("be.visible");
    cy.get("#user-score-value > .fa-spinner").should("be.visible");
    cy.get("#imdb-score > .fa-spinner").should("be.visible");
    cy.get("#tomatometer-value > .fa-spinner").should("be.visible");
    cy.get("#audience_score-value > .fa-spinner").should("be.visible");
  });
});
