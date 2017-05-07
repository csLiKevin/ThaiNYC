import PropTypes from "prop-types";
import React from "react";
import {Cell, Pie, PieChart, ResponsiveContainer} from "recharts";


export class GradePieChart extends React.Component {
    static get propTypes() {
        return {
            restaurantData: PropTypes.array.isRequired
        }
    }
    static get colors() {
        return ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];
    }
    gradeData() {
        const gradeCounts = this.props.restaurantData.reduce((accumulator, restaurant) => {
            const grade = restaurant.grades[0].score;
            accumulator[grade] += 1;
            return accumulator;
        }, {
            "1": 0,
            "2": 0,
            "3": 0,
            "26": 0
        });
        return Object.keys(gradeCounts).map((grade) => {
            return {
                name: grade,
                value: gradeCounts[grade]
            };
        });
    }
    render() {
        const gradeData = this.gradeData();
        const colors = GradePieChart.colors;
        return (
            <ResponsiveContainer width="100%" height={225}>
                <PieChart>
                    <Pie
                        data={gradeData}
                        label={({name, value}) => `${String.fromCharCode(parseInt(name) + 64)} ${value}`}
                        cx={120}
                        cy={120}
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                    >
                        {
                            gradeData.map((entry, index) => <Cell fill={colors[index % colors.length]} key={index}/>)
                        }
                    </Pie>
                </PieChart>
            </ResponsiveContainer>
        );
    }
}
export default GradePieChart;
