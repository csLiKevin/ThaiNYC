import React from "react";
import {connect} from "react-redux";
import {RestaurantTable} from "./RestaurantTable";


class PageBase extends React.Component {
    static get style () {
        return {
            paddingBottom: "10px",
            paddingLeft: "20px",
            paddingRight: "20px",
            paddingTop: "10px"
        };
    }
    render() {
        return (
            <div style={Page.style}>
                <h1>Thai NYC</h1>
                <RestaurantTable restaurantData={this.props.restaurantData}/>
            </div>
        );
    }
}
export const Page = connect((state) => {
    return {restaurantData: state.restaurantData};
})(PageBase);
export default Page;
