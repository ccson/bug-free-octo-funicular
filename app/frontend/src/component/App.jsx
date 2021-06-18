import React from "react";
import '../index.css';

export default class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {movies: []};
  }

  componentDidMount() {
    this.getMovieList();
  }

  getMovieList() {
    fetch(`http://${process.env.REACT_APP_BACKEND_URL}:8080/movie_details`)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            movies: result
          });
        }
      );
  }

  render() {
    const movies = this.state.movies.map((item, i) => (
      <tbody>
        <tr>
          <td> {item.title_name} </td>
          <td> {item.release_year} </td>
          <td> {item.film_rating} </td>
          <td> {item.runtime} </td>
          <td> {item.genres} </td>
          <td> <img src={item.poster_artwork}></img> </td>
          <td> {item.rating} </td>
          <td> {item.transcode_timestamp} </td>
          <td> {item.transcode_file_size} </td>
          <td> {item.original_file_size} </td>
        </tr>
      </tbody>
    ));

    return (
      <div>
        <table>
          <thead>
            <tr>
              <th>Title Name</th>
              <th>Release Year</th>
              <th>Film Rating</th>
              <th>Runtime (in Minutes)</th>
              <th>Genres</th>
              <th>Poster Artwork</th>
              <th>Rating</th>
              <th>Transcode Timestamp</th>
              <th>Transcoded File Size (in Bytes)</th>
              <th>Original File Size (in Bytes)</th>
            </tr>
          </thead>
          {movies}
        </table>
      </div>
    );
  }
}
