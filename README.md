[![expense_tracker](https://img.shields.io/endpoint?url=https://dashboard.cypress.io/badge/detailed/72wyad&style=plastic&logo=cypress)](https://dashboard.cypress.io/projects/72wyad/runs)

# Series Ratings



## Usage   

### Requesting a Serie's scores
Write the series of your choosing in the search bar in order to have the application fetch it's IMDb score and Rottentomatoes tomatometer and audience scores.

It shouldn't take more than 5 seconds to load the values.

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

## Installation - Cypress
For installing Cypress run go to the e2e folder and run:

    npm install


## Running tests


### Unit tests
For running the tests run:

    python manage.py test

### E2E tests
For running the tests run:

    npm run test
For running the tests on headless mode run:

    npm run test:headless
For opening cypress client run:

    npm run test:open

## Uses
 - Django.
 - Bootstrap.
 - Cypress.


## Features
- UI tests.
- Visual tests.
- Unit tests.
