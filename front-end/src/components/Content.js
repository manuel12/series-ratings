import classes from "../css/Content.module.css";

const Content = ({ children }) => {
  return <div className={classes["content-container"]}>{children}</div>;
};

export default Content;
