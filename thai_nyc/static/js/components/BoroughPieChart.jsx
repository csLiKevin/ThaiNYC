import PropTypes from "prop-types";
import React from "react";
import {Cell, Pie, PieChart, ResponsiveContainer} from "recharts";


export class BoroughPieChart extends React.Component {
    static get propTypes() {
        return {
            restaurantData: PropTypes.array.isRequired
        }
    }
    static get colors() {
        return ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#292B2C"];
    }
    getBoroughData() {
        const boroughCounts = this.props.restaurantData.reduce((accumulator, restaurant) => {
            accumulator[restaurant.borough] += 1;
            return accumulator;
        }, {
            BROOKLYN: 0,
            BRONX: 0,
            MANHATTAN: 0,
            QUEENS: 0,
            "STATEN ISLAND": 0
        });
        return Object.keys(boroughCounts).map((borough) => {
            return {
                name: borough,
                value: boroughCounts[borough]
            };
        });
    }
    render() {
        const boroughData = this.getBoroughData();
        const colors = BoroughPieChart.colors;
        return (
            <ResponsiveContainer width="100%" height={225}>
                <PieChart>
                    <Pie
                        data={boroughData}
                        label={({name, value}) => `${name} ${value}`}
                        cx={120}
                        cy={120}
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                    >
                        {
                            boroughData.map((entry, index) => <Cell fill={colors[index % colors.length]} key={index}/>)
                        }
                    </Pie>
                </PieChart>
            </ResponsiveContainer>
        );
    }
}
export default BoroughPieChart;
