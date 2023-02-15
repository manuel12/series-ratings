import classes from "../css/Header.module.css";

const Header = () => {
  return (
    <div className={classes["header-container"]} data-test="header">
      <a href="/" className="text-decoration-none" data-test="header-text">
        <h1 className="text-light text-center display-1">Series Ratings</h1>
      </a>
    </div>
  );
};

export default Header;
