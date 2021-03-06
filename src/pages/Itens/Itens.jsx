import React, { Component } from "react";

// Bootstrap imports
import { Col, Container, Row } from "react-bootstrap";

// Services
import {
  getItens,
  getItensByTitle,
  getRecommendation,
} from "../../services/recommender";

// Redux
import { connect } from "react-redux";
import {
  ADD_ITENS,
  ADD_RECOMMENDATION,
} from "../../store/actions/actionsConst";

// Components
import SearchBar from "../../components/SearchBar/SearchBar";
import FloatButton from "../../components/FloatButton/FloatButton";
import ModalItens from "../../components/ModalItens/ModalItens";
import CardItem from "../../components/CardItem/CardItem";

class Itens extends Component {
  state = {
    itens: [],
    profileItens: {},
    modalShow: false,
  };

  constructor(props) {
    super(props);
    this.onInit();
  }

  onInit = () => {
    this.props.loader(
      getItens().then((response) => {
        this.setState({ itens: response.data });
      })
    );
  };

  componentDidMount() {
    window.scrollTo(0, 0);
  }

  handleNext = () => {
    let profileItens = this.state.profileItens;

    let itens = [];

    for (let [key, value] of Object.entries(profileItens)) {
      itens.push({ movie_id: key, rating: value.rate });
    }

    let requestBody = {
      user_id: this.props.user.user.user_id,
      rates: itens,
    };

    this.props.loader(
      getRecommendation(requestBody).then((response) => {
        let recommendations = response.data;
        this.props.onSubmitItens(itens);
        this.props.onSubmitRecommendation(recommendations);

        this.props.history.push("/recommendation");
      })
    );
  };

  onSearch = (title, year) => {
    this.props.loader(
      getItensByTitle(title, year).then((response) => {
        let profileItens = this.state.profileItens;
        let profileItensKeys = Object.keys(this.state.profileItens).map(Number);
        let itens = response.data;
        console.log(itens)
        itens.forEach((element) => {
          if (profileItensKeys.includes(element.movie_id))
            element.rate = profileItens[element.movie_id].rate;
          else element.rate = 0;
        });
        this.setState({ itens: itens });
      })
    );
  };

  onRate = (id, rate) => {
    let itens = this.state.itens;

    itens[id].rate = rate;
    let item = itens[id];

    let profileItens = this.state.profileItens;
    profileItens[item.movie_id] = { ...item, ...{ rate: rate } };

    this.setState({ profileItens: profileItens, itens: itens });
  };

  onDelete = (key) => {
    let profileItens = this.state.profileItens;
    delete profileItens[key];

    let profileItensKeys = Object.keys(this.state.profileItens).map(Number);
    let itens = this.state.itens;
    itens.forEach((element) => {
      if (profileItensKeys.includes(element.movie_id))
        element.rate = profileItens[element.movie_id].rate;
      else element.rate = 0;
    });

    this.setState({ profileItens: profileItens, itens: itens });
  };

  onModalChange = () => {
    this.setState({ modalShow: !this.state.modalShow });
  };

  profileItensLen = () => Object.keys(this.state.profileItens).length;

  render() {
    return (
      <Container>
        <h4 className="d-flex justify-content-center">
          Rate at least 10 movies.
        </h4>
        <Row>
          <SearchBar onSearch={this.onSearch} />
        </Row>

        {this.state.itens.length === 0 && (
          <h4 className="d-flex justify-content-center">
            Unfortunatly, we can't find movies.
          </h4>
        )}
        <Row>
          {this.state.itens.map((item, index) => {
            return (
              <Col md={4} key={index}>
                <CardItem
                  item={item}
                  index={index}
                  onRate={this.onRate}
                  value={this.state.value}
                />
              </Col>
            );
          })}
        </Row>
        <FloatButton
          buttonFunction={this.handleNext}
          title="Next"
          num={1}
          disabled={this.profileItensLen() < 10}
        />
        <FloatButton
          buttonFunction={this.onModalChange}
          title={`Itens ${this.profileItensLen()}/10`}
          num={2}
          disabled={this.profileItensLen() === 0}
        />
        <ModalItens
          show={this.state.modalShow}
          onHide={this.onModalChange}
          itens={this.state.profileItens}
          onDelete={this.onDelete}
        />
      </Container>
    );
  }
}

const mapStateToProps = (state) => ({
  recommendations: state.recommendations,
  itens: state.itens,
  user: state.user,
});

const mapDispatchToProps = (dispatch) => ({
  onSubmitRecommendation: (value) =>
    dispatch({ type: ADD_RECOMMENDATION, payload: value }),
  onSubmitItens: (value) => dispatch({ type: ADD_ITENS, payload: value }),
});

export default connect(mapStateToProps, mapDispatchToProps)(Itens);
