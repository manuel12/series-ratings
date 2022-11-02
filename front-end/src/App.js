import "./App.css";
import Header from "./components/Header";
import Content from "./components/Content";
import Search from "./components/Search";
import Scoreboard from "./components/Scoreboard";
import Footer from "./components/Footer";

import "bootstrap/dist/css/bootstrap.min.css";
import { useEffect, useState } from "react";

function App() {
  const [searchTermSubmitted, setSearchTermSubmitted] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [scoreData, setScoreData] = useState(null);
  const [showLoadingIcons, setShowLoadingIcons] = useState(true);

  useEffect(() => {
    if (searchTermSubmitted) {
      const url = `/api/?media=${searchTerm}`;

      fetch(url, {
        method: "GET",
      })
        .then((fetchedData) => {
          return fetchedData.json();
        })
        .then((data) => {
          console.log(`Fetched from url: ${url}`);
          console.table(data);
          setScoreData(data);
          setShowLoadingIcons(false);
          return data;
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [searchTermSubmitted]);

  return (
    <div className="container h-100" data-test="container">
      <Header />
      <Content>
        {searchTermSubmitted ? (
          <Scoreboard
            title={"The Sopranos"}
            data={scoreData}
            showLoadingIcons={showLoadingIcons}
          />
        ) : (
          <Search
            setSearchTerm={setSearchTerm}
            setSearchTermSubmitted={setSearchTermSubmitted}
          />
        )}
      </Content>
      <Footer />
    </div>
  );
}

export default App;
