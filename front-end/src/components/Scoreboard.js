import classes from "../css/Scoreboard.module.css";

const Scoreboard = (props) => {
  return (
    <div
      className={`${classes["scoreboard-container"]} text-white`}
      data-test='scoreboard-container'
    >
      <div className={`${classes["scoreboard-header"]} h-25`}>
        <h2
          id='media-title'
          className={`${classes["h2"]} display-6`}
          data-test='media-title'
        >
          {props.showLoadingIcons ? (
            <div
              className={`spinner-border ${classes["media-title-spinner"]}`}
              role='status'
            ></div>
          ) : (
            props.title
          )}
        </h2>
      </div>

      <div
        className={`${classes["scoreboard-content"]} justify-content-evenly`}
      >
        <div className={`${classes["score-block"]} ${classes["imdb-block"]} `}>
          <div
            className={`${classes["imdb-header"]} display-6 text-dark`}
            id='imdb-header'
            data-test='imdb-header'
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
                className={`${classes["score-block-unit-score"]} ${classes["imdb-score"]}`}
                data-test='imdb-score-value'
              >
                {props.showLoadingIcons ? (
                  <div className='spinner-border' role='status'></div>
                ) : props.data && props.data.imdb ? (
                  `${props.data["imdb"]}/10`
                ) : (
                  "N/A"
                )}
              </div>
            </div>
          </div>
        </div>

        <div
          className={`${classes["score-block"]} ${classes["rottentomatoes-block"]}`}
        >
          <div
            className={`${classes["rottentomatoes-header"]} display-6`}
            id='rottentomatoes-header'
            data-test='rottentomatoes-header'
          >
            Rotten Tomatoes
          </div>
          <div
            className={`${classes["score-block-content"]} justify-content-evenly`}
          >
            <div className={classes["score-block-unit"]}>
              <div
                className={`${classes["score-block-unit-header"]} display-6`}
                id='tomatometer-header'
                data-test='tomatometer-header'
              >
                Tomatometer
              </div>
              <div
                className={`${classes["score-block-unit-score"]} ${classes["tomatometer-value"]}`}
                data-test='tomatometer-value'
              >
                {props.showLoadingIcons ? (
                  <div className='spinner-border' role='status'></div>
                ) : props.data &&
                  props.data["rt"] &&
                  props.data["rt"]["tomatometer"] ? (
                  `${props.data["rt"]["tomatometer"]}%`
                ) : (
                  "N/A"
                )}
              </div>
            </div>
            <div className={classes["score-block-unit"]}>
              <div
                className={`${classes["score-block-unit-header"]} display-6`}
                id='audience_score-header'
                data-test='audience_score-header'
              >
                Audience Score
              </div>
              <div
                className={`${classes["score-block-unit-score"]} ${classes["audience_score-value"]}`}
                data-test='audience_score-value'
              >
                {props.showLoadingIcons ? (
                  <div className='spinner-border' role='status'>
                    +
                  </div>
                ) : props.data &&
                  props.data["rt"] &&
                  props.data["rt"]["audience_score"] ? (
                  `${props.data["rt"]["audience_score"]}%`
                ) : (
                  "N/A"
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Scoreboard;
