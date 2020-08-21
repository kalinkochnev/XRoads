import React from 'react';
import './Search.scss';

class SearchBar extends React.Component {
    render() {
      return (
        <div>
          <form class="default-searchbar">
            <input type="text" id="search-box" placeholder="Search for clubs..."></input>
            <input id="search-submit" type="submit" value=""></input>
          </form>
        </div>
  
      );
    }
  }

  export default SearchBar;