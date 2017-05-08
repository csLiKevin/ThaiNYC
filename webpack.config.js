const path = require("path");

const jsDirectory = path.join(__dirname, "thai_nyc", "static", "js");
const entry = path.join(jsDirectory, "index.jsx");

module.exports = {
    entry: entry,
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                use: [
                    {
                        loader: "babel-loader",
                        query: {
                            plugins: [
                                [
                                    "import",
                                    {
                                        libraryName: "antd",
                                        style: "css"
                                    }
                                ],
                                "transform-object-rest-spread"
                            ],
                            presets: [
                                "es2015",
                                "react"
                            ]
                        }
                    }
                ]
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            }
        ]
    },
    output: {
        path: jsDirectory,
        filename: "bundle.js",
        publicPath: "/"
    },
    resolve: {
        extensions: [".js", ".jsx"]
    }
};
