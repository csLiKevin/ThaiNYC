import PropTypes from "prop-types";
import React from "react";
import {Table as AntTable} from "antd";
import {GradeTable} from "./GradeTable";
import {InspectionTable} from "./InspectionTable";


export class RestaurantTable extends React.Component {
    static get propTypes() {
        return {
            restaurantData: PropTypes.array.isRequired
        }
    }
    get columns() {
        return [
            {
                title: "Name",
                dataIndex: "name",
                key: "name"
            },
            {
                title: "Grade",
                dataIndex: "grades.0.score",
                key: "grade",
                render: (grade) => String.fromCharCode(grade + 64)
            },
            {
                title: "Address",
                key: "address",
                render: (record) => {
                    return (
                        <div>
                            <div>{record.street_address}</div>
                            <div>{record.borough} {record.zip_code}</div>
                        </div>
                    );
                }
            },
            {
                title: "Phone Number",
                dataIndex: "phone_number",
                key: "phoneNumber"
            }
        ];
    }
    expandedRowRender(record) {
        return (
            <div>
                <h2>Grade History</h2>
                <GradeTable gradeData={record.grades}/>
                <h2>Inspection History</h2>
                <InspectionTable inspectionData={record.inspections}/>
            </div>
        );
    }
    render() {
        return (
            <AntTable
                columns={this.columns}
                dataSource={this.props.restaurantData}
                expandedRowRender={this.expandedRowRender}
                rowKey="id"
            />
        );
    }
}
export default RestaurantTable;
