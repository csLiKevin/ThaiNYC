import PropTypes from "prop-types";
import React from "react";
import {Table as AntTable} from "antd";


export class GradeTable extends React.Component {
    static get propTypes() {
        return {
            gradeData: PropTypes.array.isRequired
        }
    }
    get columns() {
        return [
            {
                title: "Date",
                dataIndex: "date",
                key: "date"
            },
            {
                title: "Grade",
                dataIndex: "score",
                key: "grade",
                render: (grade) => String.fromCharCode(grade + 64)
            }
        ];
    }
    render() {
        return (
            <AntTable
                columns={this.columns}
                dataSource={this.props.gradeData}
                pagination={false}
                rowKey="id"
            />
        );
    }
}
export default GradeTable;
