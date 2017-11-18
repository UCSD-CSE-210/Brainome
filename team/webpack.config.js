var webpack = require('webpack');  
module.exports = {  
  devtool: 'inline-source-map',
  entry: [
    "./js/containers/ensembleTabularContainer.js"
  ],
  output: {
    path: __dirname + '/static',
    filename: "tabular_ensemble.js"
  },
   module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['react', 'es2015']
        }
      },
      { 
        test: /\.css$/,
        loader: 'style!css'
      },
      
       { test: /\.jpe?g$|\.gif$|\.png$|\.svg$|\.woff$|\.ttf$|\.wav$|\.mp3$/,
        loader: require.resolve("file-loader") + "?name=../[path][name].[ext]"
       },
      //{ test: /\.jpe?g$|\.gif$|\.png$|\.svg$|\.woff$|\.ttf$|\.eot$/, loader: "url" }
    ]
  },
  plugins: [
  ]
};
