import PropTypes from "prop-types";
import React from "react";
import {BarChart, Bar, Legend, ResponsiveContainer, XAxis} from "recharts";


export class BoroughGradeBarChart extends React.Component {
    static get propTypes() {
        return {
            restaurantData: PropTypes.array.isRequired
        }
    }
    boroughGradeData() {
        const boroughCounts = this.props.restaurantData.reduce((accumulator, restaurant) => {
            const grade = restaurant.grades[0].score;
            accumulator[restaurant.borough][grade] += 1;
            return accumulator;
        }, {
            BROOKLYN: {
                "1": 0,
                "2": 0,
                "3": 0,
                "26": 0
            },
            BRONX: {
                "1": 0,
                "2": 0,
                "3": 0,
                "26": 0
            },
            MANHATTAN: {
                "1": 0,
                "2": 0,
                "3": 0,
                "26": 0
            },
            QUEENS: {
                "1": 0,
                "2": 0,
                "3": 0,
                "26": 0
            },
            "STATEN ISLAND": {
                "1": 0,
                "2": 0,
                "3": 0,
                "26": 0
            }
        });
        return Object.keys(boroughCounts).map((borough) => {
            const boroughGrades = boroughCounts[borough];
            return {
                name: borough,
                A: boroughGrades["1"],
                B: boroughGrades["2"],
                C: boroughGrades["3"],
                Z: boroughGrades["26"]
            };
        });
    }
    render() {
        return (
            <ResponsiveContainer width="100%" height={225}>
                <BarChart data={this.boroughGradeData()}>
                    <XAxis dataKey="name"/>
                    <Bar dataKey="A" stackId="single" fill="#00C49F" />
                    <Bar dataKey="B" stackId="single" fill="#0088FE" />
                    <Bar dataKey="C" stackId="single" fill="#FFBB28" />
                    <Bar dataKey="Z" stackId="single" fill="#FF8042" />
                    <Legend />
                </BarChart>
            </ResponsiveContainer>
        );
    }
}
