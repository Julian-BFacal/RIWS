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
import Slider from '@mui/material/Slider';
import Typography from '@mui/material/Typography';


const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "book"
});

const configurationOptions = {
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true,
  autocompleteQuery: {
    suggestions: {
      types: {
        documents: {
          // Which fields to search for suggestions.
           fields: ["name"]
        }
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
    facets: {
      tags: { type: "value", size: 100 },
      language: { type: "value", size: 5 },
      year: { type: "value", size: 15 },
      pages: { type: "value", size: 15 },
    }
  }
};

function MyModal( {result} ) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <main>
      <button className={styles.primaryBtn} onClick={() => setIsOpen(true)}>
       Ver Mas
      </button>
      {isOpen && <Modal result={result} setIsOpen={setIsOpen}  />}
    </main>
  )
}

const CustomResultView = ({ result }) =>(
  <li className="sui-result" style={{width:'50%'}}>
    <div className="sui-result__header">
      <h3 className="card-title">
        {result.name.raw}
      </h3>
      <h4 className="card-author">
        {result.author.raw}
      </h4>
    </div>
    <div className="sui-result__body">
      {/* use 'raw' values of fields to access values without snippets */}
      <div className="sui-result__image">
        <img src={result.portada.raw} alt={result.portada.raw} style={{align:'center'}}/>
        <MyModal style={{padding:'50px'}} result={result}/>
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
          header={<SearchBox autocompleteSuggestions={false} inputProps={{ placeholder: "Buscar autor o libro" }} />}
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
                    name: "Relevance",
                    value: "",
                    direction: ""
                  },
                  {
                    name: "Name",
                    value: "name",
                    direction: "asc"
                  },
                ]}
              />
              <Facet field="tags" label="Tags" isFilterable={true} />
              <Facet field="language" label="Idioma" isFilterable={false} />
              <Facet field="year" label="Año" isFilterable={false} />
              <Facet field="pages" label="Páginas" isFilterable={false} />
              <Typography  gutterBottom> PÁGINAS </Typography>
              <Slider defaultValue={50} aria-label="Default" valueLabelDisplay="auto" />
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
