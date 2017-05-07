import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";
import {createStore} from "redux";
import Page from "./components/Page";


function reducer(state={}, action) {
    switch(action.type) {
    }
    return state;
}

const initialState = {
    restaurantData: restaurantData // restaurantData is passed to the page from Django.
};
const store = createStore(reducer, initialState);

const App = () => {
    return (
        <Provider store={store}>
            <Page>Hello World</Page>
        </Provider>
    );
};

ReactDOM.render(
    <App />,
    document.getElementById("viewport")
);
