import { useState } from "react";

const Search = (props) => {
  const [searchTerm, setSearchTerm] = useState("");

  const onlyWhiteSpace = (s) => {
    return s.match(/^\s*$/);
  };

  const validateForm = () => {
    const inputElem = document.getElementById("id_search");
    return onlyWhiteSpace(inputElem.value) ? false : true;
  };

  const submitHandler = (e) => {
    e.preventDefault();

    if (validateForm()) {
      setSearchTerm(e.target.value);
      props.setSearchTerm(searchTerm);
      props.setSearchTermSubmitted(true);
    }
  };

  return (
    <div className="container" data-test="search-container">
      <div className="row justify-content-center align-items-center h-100">
        <div className="col-9">
          <form
            action="scoreboard/"
            className="input-group"
            method="POST"
            data-test="search-form"
            onSubmit={submitHandler}
          >
            <input
              type="text"
              name="search"
              className="form-control"
              placeholder="Stranger Things..."
              maxLength="100"
              required
              id="id_search"
              onChange={(e) => {
                setSearchTerm(e.target.value);
              }}
            ></input>
            <div className="input-group-append input-group-lg">
              <button type="submit" className="btn btn-danger" data-test="search-button">
                Search
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Search;
