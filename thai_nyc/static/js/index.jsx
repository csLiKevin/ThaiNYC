import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";
import {createStore} from "redux";



function reducer(state={}, action) {
    switch(action.type) {
    }
    return state;
}

const store = createStore(reducer);

const App = () => {
    return (
        <Provider store={store}>
            <div>Hello World</div>
        </Provider>
    );
};


ReactDOM.render(
    <App />,
    document.getElementById("viewport")
);
