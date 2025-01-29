// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

// SEPARATORRRRRRR

// import { SearchProvider, SearchBox, Results, Facet } from "@elastic/react-search-ui";
// import ElasticsearchAPIConnector from '@elastic/search-ui-elasticsearch-connector';
// import '@elastic/react-search-ui-views/lib/styles/styles.css';

// const connector = new ElasticsearchAPIConnector({
//   host: 'http://localhost:9200',
//   index: 'cv-transcriptions'
// });

// const configurationOptions = {
//   apiConnector: connector,
//   searchQuery: {
//     search_fields: {
//       generated_text: {},
//       duration: {},
//       age: {},
//       gender: {},
//       accent: {},
//     },
//     result_fields: {
//       generated_text: { snippet: { size: 100, fallback: true } },
//       duration: {},
//       age: {},
//       gender: {},
//       accent: {},
//     },
//     facets: {
//       gender: { type: 'value' },
//       accent: { type: 'value' },
//       age: {
//         type: 'range',
//         ranges: [
//           { from: 18, to: 30 },
//           { from: 31, to: 45 },
//           { from: 46, to: 60 },
//         ],
//       },
//       duration: {
//         type: 'range',
//         ranges: [
//           { from: 0, to: 3 },
//           { from: 4, to: 6 },
//           { from: 7, to: 10 },
//         ],
//       },
//     }
//   },
//   alwaysSearchOnInitialLoad: true
// };

// const App = () => (
//   <SearchProvider config={configurationOptions}>
//     <div className="App">
//       <SearchBox />
//       <Results />
//       <Facet field="gender" label="Gender" />
//       <Facet field="accent" label="Accent" />
//     </div>
//   </SearchProvider>
// );

// export default App;


// SEPARATORRRRRRR


// import { SearchProvider, SearchBox, Results, Facet, Paging, Sorting } from "@elastic/react-search-ui";
// import ElasticsearchAPIConnector from '@elastic/search-ui-elasticsearch-connector';
// import '@elastic/react-search-ui-views/lib/styles/styles.css';

// const connector = new ElasticsearchAPIConnector({
//   host: 'http://localhost:9200',
//   index: 'cv-transcriptions'
// });

// const configurationOptions = {
//   apiConnector: connector,
//   searchQuery: {
//     search_fields: {
//       generated_text: {},
//       duration: {},
//       age: {},
//       gender: {},
//       accent: {},
//     },
//     result_fields: {
//       generated_text: { snippet: { size: 100, fallback: true } },
//       duration: {},
//       age: {},
//       gender: {},
//       accent: {},
//     },
//     facets: {
//       gender: { type: 'value' },
//       accent: { type: 'value' },
//       age: {
//         type: 'range',
//         ranges: [
//           { from: 18, to: 30 },
//           { from: 31, to: 45 },
//           { from: 46, to: 60 },
//         ],
//       },
//       duration: {
//         type: 'range',
//         ranges: [
//           { from: 0, to: 3 },
//           { from: 4, to: 6 },
//           { from: 7, to: 10 },
//         ],
//       },
//     },
//   },
//   alwaysSearchOnInitialLoad: true
// };

// const App = () => (
//   <SearchProvider config={configurationOptions}>
//     <div className="App">
//       <SearchBox />
//       <Sorting
//         label="Sort By"
//         sortOptions={[
//           { name: "Relevance", value: "", direction: "" },
//           { name: "Age (Ascending)", value: "age", direction: "asc" },
//           { name: "Age (Descending)", value: "age", direction: "desc" }
//         ]}
//       />
//       <Results />
//       <Facet field="gender" label="Gender" />
//       <Facet field="accent" label="Accent" />
//       <Paging />
//     </div>
//   </SearchProvider>
// );

// export default App;


import { SearchProvider, Results, Facet, Paging, Sorting } from "@elastic/react-search-ui";
import ElasticsearchAPIConnector from '@elastic/search-ui-elasticsearch-connector';
import '@elastic/react-search-ui-views/lib/styles/styles.css';

const connector = new ElasticsearchAPIConnector({
  host: 'http://localhost:9200',
  index: 'cv-transcriptions'
});

const configurationOptions = {
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      generated_text: { type: 'text' },
      duration: { type: 'numeric' },
      age: { type: 'exact'},
      gender: { type: 'exact'},
      accent: { type: 'exact'},
    },
    result_fields: {
      generated_text: { snippet: { size: 100, fallback: true } },
      duration: {},
      age: {},
      gender: {},
      accent: {},
    },
    facets: {
      gender: { type: 'value' },
      accent: { type: 'value' },
      age: { type: 'value' },
      duration: {
        type: 'range',
        ranges: [
          { from: 0, to: 10, name: "0 - 10 sec" },
          { from: 11, to: 20, name: "11 - 20 sec" },
          { from: 21, to: 30, name: "21 - 30 sec" },
          { from: 31, name: "31 sec and above" },
        ],
      },
    },
  },
  alwaysSearchOnInitialLoad: true
};

const App = () => (
  <SearchProvider config={configurationOptions}>
    <div className="App">
      <Sorting
        label="Sort By"
        sortOptions={[
          { name: "Duration (Ascending)", value: [{ field: "duration", direction: "asc" }] },
          { name: "Duration (Descending)", value: [{ field: "duration", direction: "desc" }] }
        ]}
      />
      <Results />
      <Facet field="gender" label="Gender" />
      <Facet field="accent" label="Accent" />
      <Facet field="age" label="Age Range" />
      <Facet field="duration" label="Duration Range" type="range"
        ranges={[
          { from: 0, to: 10, name: "0 - 10 sec" },
          { from: 11, to: 20, name: "11 - 20 sec" },
          { from: 21, to: 30, name: "21 - 30 sec" },
          { from: 31, name: "31 sec and above" },
        ]}
      />
      <Paging />
    </div>
  </SearchProvider>
);

export default App;