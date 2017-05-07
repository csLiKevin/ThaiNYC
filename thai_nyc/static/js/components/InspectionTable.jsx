import PropTypes from "prop-types";
import React from "react";
import {Table as AntTable} from "antd";


export class InspectionTable extends React.Component {
    static get propTypes() {
        return {
            inspectionData: PropTypes.array.isRequired
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
                title: "Type",
                dataIndex: "check_type",
                key: "type"
            },
            {
                title: "Critical",
                dataIndex: "critical",
                key: "critical",
                render: (boolean) => <div style={{backgroundColor: boolean ? "#FF8042" : "#00C49F", height: "16px", width: "16px"}}/>
            },
            {
                title: "Violation Code",
                dataIndex: "violation_code",
                key: "violationCode"
            },
            {
                title: "Number of Violations",
                dataIndex: "score",
                key: "violationNumber"
            },
            {
                title: "Description",
                dataIndex: "violation_description",
                key: "violationDescription",
                render: (description) => description.length > 150 ? description.substring(0, 150) + "..." : description
            }
        ];
    }
    render() {
        return (
            <AntTable
                columns={this.columns}
                dataSource={this.props.inspectionData}
                pagination={false}
                rowKey="id"
            />
        );
    }
}
export default InspectionTable;
