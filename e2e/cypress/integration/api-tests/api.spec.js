/// <reference types="cypress" />
let testData = require("../../fixtures/test-data.json");
let seriesTitles = testData.map((serie) => serie.title);
// seriesTitles = seriesTitles.filter(
//   (title) =>
//     //title === "Magnum P.I." ||
//     title === "The A-Team" //||
//   // title === "Band Of Brothers"
// );

describe("Fetch Score Data API 'GET' request", () => {
  for (const serieTitle of seriesTitles) {
    it(`should return score data for ${serieTitle}`, () => {
      const searchTerm = serieTitle;
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
        const currentSeries = testData.filter(
          (_serie) => _serie.title === serieTitle
        )[0];
        const imdbScore = currentSeries.data.imdb;
        const tomatometerScore = currentSeries.data.rt.tomatometer;
        const audienceScore = currentSeries.data.rt.audience_score;
        const scoreData = response.body.data;

        if (imdbScore != null) {
          expect(scoreData.imdb).to.closeTo(imdbScore, 0.1);
        } else {
          expect(scoreData.imdb).to.eq(imdbScore);
        }

        if (tomatometerScore != null) {
          expect(scoreData.rt.tomatometer).to.closeTo(tomatometerScore, 1);
        } else {
          expect(scoreData.rt.tomatometer).to.eq(tomatometerScore);
        }

        if (audienceScore != null) {
          expect(scoreData.rt.audience_score).to.closeTo(audienceScore, 1);
        } else {
          expect(scoreData.rt.audience_score).to.eq(audienceScore);
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
