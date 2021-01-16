import React from 'react';
import './Search.scss';
import Sticky from '../StickyCard/StickyCard.jsx';
import lunr from 'lunr';

class SearchBar extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      searchQuery: "",
      searchRes: null
    }

    this.handleChange = this.handleChange.bind(this);
    this.searchClubs = this.searchClubs.bind(this);

    this.clubs = props.clubs;
    console.log("Received clubs for searching", this.props.clubs);

    this.lunrIndex = lunr(function () {
      this.field("name", {
        boost: 10
      });
      this.field("description");

      this.ref("id");

      props.clubs.forEach(function (club) {
        this.add(club)
      }, this)
    });

  }

  handleChange(e) {
    console.log("input text changed", e);
    // setSearchQuery(e.target.value);
    let v = e.target.value
    this.setState(() => ({
      searchQuery: v
    }));
  }

  searchClubs(e) {
    console.log("Search clubs called with query", this.state.searchQuery);

    e.preventDefault();

    let searchRes = this.lunrIndex.search(this.state.searchQuery).map(function (result) {
      return result.ref;
    });
    console.log("Lunr index is", this.lunrIndex);

    console.log("Search result found", searchRes);

    this.props.filterClubs(searchRes)

    this.setState({
      searchRes: searchRes
    });


  }
  render() {
    const searchResNotFound = this.state.searchRes != null && this.state.searchRes.length == 0
    return (
      <div>
        <div className="search-center">
          <Sticky label="All Clubs">
            <form className="default-searchbar" onSubmit={this.searchClubs}>
              <input type="text" id="search-box" placeholder="Search for clubs..." value={this.searchQuery} onChange={this.handleChange}></input>
              <input id="search-submit" type="submit" value="" onClick={this.searchClubs}></input>
            </form>
          </Sticky>
        </div>
        { searchResNotFound ? <div>No results in search - womp, womp, womp :(  </div> : <div />}
      </div>);
  }
}


export default SearchBar;