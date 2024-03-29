[![media-ratings](https://img.shields.io/endpoint?url=https://cloud.cypress.io/badge/detailed/wy69vd&style=plastic&logo=cypress)](https://cloud.cypress.io/projects/wy69vd/runs)

\*_Check note under 'E2E tests' section_

![Series Ratings](hero.png)

Series Ratings is an application where you can search for the IMDb & Rotten Tomatoes ratings of your favorite series.

The app visits the IMDb and Rotten Tomatoes websites and uses their own search features to find out the series you requested, then it parses the score on each page and delivers it to you on a results page. It also creates a record of the searched series on the database so the next time you search for it the result will be retrieved faster.

  <h2>Desktop</h2>
  <img src="https://user-images.githubusercontent.com/4129325/221217865-d51a9f01-a1d1-438b-86b0-d85acd3d4351.png" title="Media Ratings Desktop" alt="Media Ratings Desktop" width="650" height="357" style="display: inline"/>
  
  <h2>Mobile</h2>
  <img src="https://github.com/manuel12/media-ratings/assets/4129325/7074b91e-8a14-47e6-9307-51330714b22b" title="Media Ratings Mobile" alt="Media Ratings Mobile" width="165" height="357"/>

## Usage

### Requesting a Serie's scores

Write the series of your choosing in the search bar in order to have the application fetch it's IMDb score and Rottentomatoes tomatometer and audience scores.

It shouldn't take more than 6 seconds to load the values the first time. The next time you search for the same series the app will show the score's inmediatly.

![Display gif showing search query being submitted and app loading fetched scores](demo/submit-search.gif)

## Installation

For installing the Django application clone the repository and run:

     pipenv install

This will install the virtual environments and all dependencies.

Now start the virtual environment shell:

     pipenv shell

Run migrations:
python manage.py makemigrations
python manage.py migrate

Create superuser:

    python manage.py createsuperuser

Now you can start server...

    python manage.py runserver

...and visit http://localhost:8000/

## Installation - React

For installing the React application go to the front-end folder and run:

    npm install

And after install is finished run:

    npm start

## Installation - Cypress

For installing Cypress go to the e2e folder and run:

    npm install

## Tests

| Type | Location                                                               |
| ---- | ---------------------------------------------------------------------- |
| api  | [e2e/cypress/integration/api-tests](e2e/cypress/integration/api-tests) |
| ui   | [e2e/cypress/integration/ui-tests](e2e/cypress/integration/ui-tests)   |
| unit | [media_ratings/tests](media_ratings/tests)                             |

## Running tests

### Unit tests

For running the tests run:

    python manage.py test

### E2E tests

For running the tests go to the e2e folder and run:

    npm run test

For running the tests on headless mode run:

    npm run test:headless

For opening cypress client run:

    npm run test:open

**Note:** currently the test of the tv series The Crown are failing (hence the 3 failed tests shown on cypress badge). These tests are failing because the Rotten Tomatoes parser is parsing the results of another tv series other than The Crown. An update will be made once I figure out how to make the parser pick the correct series.

## Uses

- Django.
- DRF.
- React
- React-Bootstrap.
- Font Awesome icons.
- Cypress.

## Features

- Web Parsing.
- UI tests.
- API tests.
- Unit tests.
