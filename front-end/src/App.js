import "./App.css";
import Header from "./components/Header";
import Content from "./components/Content";
import Search from "./components/Search";
import Scoreboard from "./components/Scoreboard";

import "bootstrap/dist/css/bootstrap.min.css";
import { useEffect, useState } from "react";

function App() {
  const [searchTermSubmitted, setSearchTermSubmitted] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [seriesTitle, setSeriesTitle] = useState(searchTerm);
  const [scoreData, setScoreData] = useState(null);
  const [showLoadingIcons, setShowLoadingIcons] = useState(true);

  useEffect(() => {
    if (searchTermSubmitted) {
      const url = `/api/?media=${searchTerm}`;
      console.log(`Making request to url: ${url}...`);
      fetch(url, {
        method: "GET",
      })
        .then((fetchedData) => {
          return fetchedData.json();
        })
        .then((dataObj) => {
          console.log(dataObj);
          console.log(`Fetched from url: ${url}`);

          const scoreData = dataObj.data;
          const title = dataObj.title;

          setSeriesTitle(title);
          setScoreData(scoreData);
          setShowLoadingIcons(false);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, [searchTermSubmitted]);

  return (
    <div className='app-container container h-100' data-test='container'>
      <Header />
      <Content>
        {searchTermSubmitted ? (
          <Scoreboard
            title={seriesTitle}
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
    </div>
  );
}

export default App;
