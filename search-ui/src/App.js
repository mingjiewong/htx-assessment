import { SearchProvider, SearchBox, Results, Facet, Paging, Sorting } from "@elastic/react-search-ui";
import ElasticsearchAPIConnector from '@elastic/search-ui-elasticsearch-connector';
import '@elastic/react-search-ui-views/lib/styles/styles.css';

const connector = new ElasticsearchAPIConnector({
  host: process.env.REACT_APP_ELASTICSEARCH_HOST || 'http://localhost:9200',
  index: 'cv-transcriptions'
});

console.log('ElasticsearchAPIConnector initialized with host:', connector.host);

const configurationOptions = {
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      generated_text: { type: 'text' },
      // duration: { type: 'numeric' },
      // age: { type: 'exact' },
      // gender: { type: 'exact' },
      // accent: { type: 'exact' },
    },
    result_fields: {
      generated_text: { snippet: { size: 100, fallback: true } },
      duration: { raw: { fallback: 0 } }, // Provide a default value
      age: { raw: { fallback: "Unknown" } },
      gender: { raw: { fallback: "Unknown" } },
      accent: { raw: { fallback: "Unknown" } },
    },
    facets: {
      gender: { type: 'value'},
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
    <div className="App" style={styles.container}>

      {/* Search Box for Keyword Search */}
      <div style={styles.searchBox}>
        <SearchBox />
      </div>

      {/* Filters (Aligned in Grid) */}
      <div style={styles.filters}>
        <div style={styles.filterItem}><Facet field="gender" label="Gender" /></div>
        <div style={styles.filterItem}><Facet field="accent" label="Accent" /></div>
        <div style={styles.filterItem}><Facet field="age" label="Age Range" /></div>
        <div style={styles.filterItem}>
          <Facet 
            field="duration" 
            label="Duration Range" 
            type="range"
            ranges={[
              { from: 0, to: 10, name: "0 - 10 sec" },
              { from: 11, to: 20, name: "11 - 20 sec" },
              { from: 21, to: 30, name: "21 - 30 sec" },
              { from: 31, name: "31 sec and above" },
            ]}
          />
        </div>
      </div>

      {/* Sorting */}
      <div style={styles.sorting}>
        <Sorting
          label="Sort By"
          sortOptions={[
            { name: "Duration (Ascending)", value: [{ field: "duration", direction: "asc" }] },
            { name: "Duration (Descending)", value: [{ field: "duration", direction: "desc" }] }
          ]}
        />
      </div>

      {/* Results */}
      <div style={styles.results}>
        <Results />
      </div>

      {/* Pagination */}
      <div style={styles.paging}>
        <Paging />
      </div>

    </div>
  </SearchProvider>
);

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
    padding: "20px",
    maxWidth: "900px",
    margin: "auto"
  },
  sorting: {
    textAlign: "center",
    paddingBottom: "10px"
  },
  filters: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)", // Ensure 4 evenly spaced columns
    gap: "20px",
    borderBottom: "1px solid #ddd",
    paddingBottom: "10px"
  },
  filterItem: {
    minWidth: "200px", // Ensure all filters have equal width
    textAlign: "left",
  },
  results: {
    marginTop: "20px"
  },
  paging: {
    textAlign: "center",
    marginTop: "20px"
  }
};

export default App;