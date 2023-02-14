import { useState } from "react";
import classes from "../css/Search.module.css";

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
    <div className="container search-container" data-test="search-container">
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
        <div className="input-group-append">
          <button
            type="submit"
            className="btn btn-danger"
            data-test="search-button"
          >
            Search
          </button>
        </div>
      </form>
    </div>
  );
};

export default Search;
