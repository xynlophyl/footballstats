import React, { Component } from 'react';
import axios from 'axios';

class FPLView extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      squad: [],
    };
  };

  componentDidMount = () => {
    axios
      .get(`${this.state.base_url}/fpl/squad/`)
      .then((res) => this.setState({squad: res.data}))
      .catch((e) => this.setState({errorFlag:true, errorMessage: 'this song and artist combination already exists'}))

    axios
      .get(`${this.state.base_url}/fpl/squad/`)
      .then((res) => {
        console.log(res.data)
      })
    return;
  }

  renderSquad = () => {
    var squad = this.state.squad
    console.log(squad)
  }

  render() {
    return (
      <main className="min-h-screen bg-red-900" id="fplsquad">
        <div className="border-red-400 border-2">
          test
        </div>
      </main>
    );
  };
}

export default FPLView;