/// <reference types="cypress" />
let testData = require("../../fixtures/test-data.json");
let seriesTitles = testData.map((serie) => serie.title);

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
        const imdbScore = currentSeries.imdb;
        const tomatometerScore = currentSeries.rt.tomatometer;
        const audienceScore = currentSeries.rt.audience_score;

        expect(response.body.imdb).to.eq(imdbScore);
        expect(response.body.rt.tomatometer).to.eq(tomatometerScore);
        expect(response.body.rt.audience_score).to.eq(audienceScore);
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
      console.log(response);
      expect(response.status).to.eq(200);
      expect(response.headers).to.have.property(
        "content-type",
        "application/json"
      );

      expect(response.body.imdb).to.eq("N/A");
      expect(response.body.rt.tomatometer).to.eq("N/A");
      expect(response.body.rt.audience_score).to.eq("N/A");
    });
  });
});
