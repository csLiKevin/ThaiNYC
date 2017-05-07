import React from "react";
import {connect} from "react-redux";
import {Card, Col, Row} from "antd";
import {BoroughPieChart} from "./BoroughPieChart";
import {BoroughGradeBarChart} from "./BoroughGradeBarChart";
import {GradePieChart} from "./GradePieChart";
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
    static get rowStyle() {
        return {
            marginBottom: "10px"
        }
    }
    render() {
        return (
            <div style={Page.style}>
                <Row style={Page.rowStyle}>
                    <h1>Thai NYC</h1>
                </Row>
                <Row gutter={8} style={Page.rowStyle}>
                    <Col span={8}>
                        <Card title="Restaurants per Borough">
                            <BoroughPieChart restaurantData={this.props.restaurantData}/>
                        </Card>
                    </Col>
                    <Col span={8}>
                        <Card title="Restaurants by Health Grade">
                            <GradePieChart restaurantData={this.props.restaurantData}/>
                        </Card>
                    </Col>
                    <Col span={8}>
                        <Card title="Restaurants Health Grade by Borough">
                            <BoroughGradeBarChart restaurantData={this.props.restaurantData}/>
                        </Card>
                    </Col>
                </Row>
                <Row style={Page.rowStyle}>
                    <Card title="Restaurants ordered by Grade and Health Violations">
                        <RestaurantTable restaurantData={this.props.restaurantData}/>
                    </Card>
                </Row>
            </div>
        );
    }
}
export const Page = connect((state) => {
    return {restaurantData: state.restaurantData};
})(PageBase);
export default Page;
