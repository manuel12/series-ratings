import classes from "../css/Scoreboard.module.css";

const Scoreboard = (props) => {
  return (
    <div className="row justify-content-center">
      <div
        className={`${classes["scoreboard-container"]} col-md-9 text-white`}
        data-test="scoreboard-container"
      >
        <div className={`${classes["scoreboard-header"]} h-25`}>
          <h2
            id="media-title"
            className={`${classes["h2"]} display-6`}
            data-test="media-title"
          >
            {props.showLoadingIcons ? (
              <div className="spinner-border" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            ) : (
              props.data["title"]
            )}
          </h2>
        </div>

        <div>
          <div
            className={`${classes["scoreboard-content"]} justify-content-evenly`}
          >
            <div
              className={`${classes["score-block"]} col-sm-5`}
              id={classes["imdb-block"]}
            >
              <div
                className="display-6 text-dark"
                id="imdb-header"
                data-test="imdb-header"
              >
                IMDb
              </div>
              <div
                className={`${classes["score-block-content"]} justify-content-evenly`}
              >
                <div className={classes["score-block-unit"]}>
                  <div
                    className={`${classes["score-block-unit-header"]} display-6 text-dark`}
                  >
                    Overall Score
                  </div>
                  <div
                    className={classes["score-block-unit-score"]}
                    id={classes["imdb-score"]}
                    data-test="imdb-score-value"
                  >
                    {props.showLoadingIcons ? (
                      <div className="spinner-border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    ) : (
                      props.data["imdb"]
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div
              className={`${classes["score-block"]} col-sm-5`}
              id={classes["rottentomatoes-block"]}
            >
              <div
                className="display-6"
                id="rottentomatoes-header"
                data-test="rottentomatoes-header"
              >
                Rotten Tomatoes
              </div>
              <div
                className={`${classes["score-block-content"]} justify-content-evenly`}
              >
                <div className={classes["score-block-unit"]}>
                  <div
                    className={`${classes["score-block-unit-header"]} display-6`}
                    id="tomatometer-header"
                    data-test="tomatometer-header"
                  >
                    Tomatometer
                  </div>
                  <div
                    className={classes["score-block-unit-score"]}
                    id={classes["tomatometer-value"]}
                    data-test="tomatometer-value"
                  >
                    {props.showLoadingIcons ? (
                      <div className="spinner-border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    ) : (
                      props.data["rt"]["tomatometer"]
                    )}
                  </div>
                </div>
                <div className={classes["score-block-unit"]}>
                  <div
                    className={`${classes["score-block-unit-header"]} display-6`}
                    id="audience_score-header"
                    data-test="audience_score-header"
                  >
                    Audience Score
                  </div>
                  <div
                    className={classes["score-block-unit-score"]}
                    id={classes["audience_score-value"]}
                    data-test="audience_score-value"
                  >
                    {props.showLoadingIcons ? (
                      <div className="spinner-border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    ) : (
                      props.data["rt"]["audience_score"]
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Scoreboard;
