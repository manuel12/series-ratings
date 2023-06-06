/// <reference types="cypress" />
let testData = require("../../fixtures/test-data.json");
let series = testData;

describe("Fetch Score Data API 'GET' request", () => {
  for (const serie in series) {
    const currentTestData = series[serie];

    it(`should return score data for ${currentTestData.title}`, () => {
      cy.request({
        method: "GET",
        url: `${Cypress.config("baseUrl")}api/?media=${currentTestData.title}`,
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.headers).to.have.property(
          "content-type",
          "application/json"
        );

        const imdbScore = currentTestData.data.imdb;
        const tomatometerScore = currentTestData.data.rt.tomatometer;
        const audienceScore = currentTestData.data.rt.audience_score;
        const scoreData = response.body.data;

        if (imdbScore == null) {
          expect(scoreData.imdb).to.eq(imdbScore);
        } else {
          expect(scoreData.imdb).to.closeTo(imdbScore, 0.2);
        }

        if (tomatometerScore == null) {
          expect(scoreData.rt.tomatometer).to.eq(tomatometerScore);
        } else {
          expect(scoreData.rt.tomatometer).to.closeTo(tomatometerScore, 1);
        }

        if (audienceScore == null) {
          expect(scoreData.rt.audience_score).to.eq(audienceScore);
        } else {
          expect(scoreData.rt.audience_score).to.closeTo(audienceScore, 1);
        }
      });
    });
  }

  it("should return score data not found", () => {
    const searchTerm = "Non Existing Movie";
    cy.request({
      method: "GET",
      url: `${Cypress.config("baseUrl")}api/?media=${searchTerm}`,
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.headers).to.have.property(
        "content-type",
        "application/json"
      );

      const scoreData = response.body.data;
      expect(scoreData.imdb).to.eq(null);
      expect(scoreData.rt.tomatometer).to.eq(null);
      expect(scoreData.rt.audience_score).to.eq(null);
    });
  });
});
