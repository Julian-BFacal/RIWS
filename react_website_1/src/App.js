import React, { useState } from "react";
import styles from "./App.css";
import Modal from "./components/modal.jsx";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import {
  PagingInfo,
  ResultsPerPage,
  Paging,
  Facet,
  SearchProvider,
  Results,
  SearchBox,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import "./App.css";
import moment from "moment";





const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "book"
});

const configurationOptions = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  autocompleteQuery: {
    results:{
      search_fields: {
        "name.suggest": {
          weight: 3
        }
    },
    result_fields: {
      name: {
          snippet:{
            size: 100,
            fallback: true
          }
      },
    }
  },
    suggestions: {
      types: {
        results: {fields: ["name_completion"]}
      },
      // How many suggestions appear.
      size: 5
    }
  },
  searchQuery: {
    // 2. Results: name of the video game, its genre, publisher, scores, and platform.
    result_fields: {
      name: { raw: {} },
      author: { raw: {}},
      editorial: { raw: {}},
      tags: { raw: {}},
      year: {raw:{}},
      pages: {raw:{}},
      language: {raw:{}},
      sinopsis: {
        snippet: {
          size: 1000,
        }
      },
      portada: {raw: {}},
    },
    search_fields: {
     // 1. Search by name of video game.
     name: {},
     author: {}
    },
    // 3. Facet by scores, genre, publisher, and platform, which we'll use to build filters later.
    disjunctiveFacets: [
      "pages",
      "year",
      "language"
   ],
    facets: {
      tags: { type: "value", size: 15 },
      language: { type: "value", size: 10 },
      year: {
        type: "range",
        ranges: [
          { from: moment().year(), to:  moment().year(),
            name: "2023"
          },
          { from: moment().subtract(1,"years").year(), to: moment().subtract(1,"years").year(),
            name: "2022"
          },
          { from: moment().subtract(2,"years").year(), to: moment().subtract(2,"years").year(),
            name: "2021"
          },
          { from: moment().subtract(3,"years").year(), to: moment().subtract(3,"years").year(),
            name: "2020"
          },
          { from: moment().subtract(8,"years").year(), to: moment().subtract(4,"years").year(),
            name: "2015-2019"
          },
          { from: moment().subtract(13,"years").year(), to: moment().subtract(9,"years").year(),
            name: "2010-2014"
          },
          { from: moment().subtract(23,"years").year(), to: moment().subtract(14,"years").year(),
            name: "2000-2009"
          },
          { from: moment().subtract(33,"years").year(), to: moment().subtract(24,"years").year(),
            name: "1990"
          },
          { from: moment().subtract(43,"years").year(), to: moment().subtract(34,"years").year(),
            name: "1980-"
          },
        ]

      },
      pages: {
        type: "range",
        ranges: [
          { from: 0, to: 50, name: "0 - 50" },
          { from: 50, to: 100, name: "50 - 100" },
          { from: 100, to: 200, name: "100 - 200" },
          { from: 200, to: 300, name: "200 - 300" },
          { from: 300, to: 350, name: "300 - 400" },
          { from: 400, name: "400+" }
        ]
      }
    }
  }
};

function disable(){
document.body.style.overflow = 'hidden';}

export function enable(){
document.body.style.overflow = 'scroll';}

function MyModal( {result} ) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <main>
      <button className="primaryBtn" onClick={() => {setIsOpen(true); disable()}}>
       Ver Mas
      </button>
      {isOpen && <Modal result={result} setIsOpen={setIsOpen}  />}
    </main>
  )
}

const CustomResultView = ({ result }) =>(
  <li className="sui-result">
    <div className="sui-result__header">
      <div>
      <h3 className="card-title">{result.name.raw}</h3>
      </div>
    </div>
    <div className="sui-result__body">
      {/* use 'raw' values of fields to access values without snippets */}
      <div className="sui-result__image">
        <img src={result.portada.raw} alt={result.portada.raw}/>
        <h4 className="card-author">{result.author.raw}</h4>
        <MyModal result={result}/>
      </div>
        {/* Use the 'snippet' property of fields with dangerouslySetInnerHtml to render snippets */}

    </div>
  </li>
);


export default function App() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <SearchProvider config={configurationOptions}>
      <div className="App">
        <Layout
          header={
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between"
                }}
              >
                <div
                style={{
                  fontSize: "40px"
                }}>
                📚 Biblioteca Online
                </div >
                <div>
                <SearchBox searchAsYouType={true} debounceLength={300} autocompleteSuggestions={true}  autocompleteMinimumCharacters={3} inputProps={{ placeholder: "Buscar autor o libro" }}   />
                </div>
              </div>
            </div>
          }
          bodyContent={
            <Results
              resultView={CustomResultView}
              titleField="name"
              urlField="portada"
              thumbnailField="portada"/>}
          sideContent={
            <div>
              <Sorting
                label={"Ordenar por"}
                sortOptions={[
                  {
                    name: "Relevancia",
                    value: "",
                    direction: ""
                  },
                  {
                    name: "Autor",
                    value: [
                      {
                        field: "author.keyword",
                        direction: "asc"
                      }
                    ]
                  },
                  {
                    name: "Título",
                    value: [
                      {
                        field: "name.keyword",
                        direction: "asc"
                      }
                    ]
                  }
                ]}
              />
              <Facet field="tags" label="Tags" isFilterable={true} />
              <Facet field="language" label="Idioma" isFilterable={false} />
              <Facet field="year" label="Año" isFilterable={false} />
              <Facet field="pages" label="Páginas" isFilterable={false} />
            </div>
          }
          bodyHeader={
            <>
              <PagingInfo />
              <ResultsPerPage />
            </>
          }
          bodyFooter={<Paging />}
        />
      </div>
    </SearchProvider>
  );
}
