const path = require('path')

module.exports = {
  devServer: {
    port: 8081,
    hot: true
  },
  configureWebpack: {
    resolve: {
      alias: {
        'vis-network$': path.resolve(__dirname, 'node_modules/vis-network/dist/vis-network.esm.js'),
        'vis-data$': path.resolve(__dirname, 'node_modules/vis-data/peer/umd/vis-data.js'),
        'vis-network/dist/vis-network.css$': path.resolve(
          __dirname,
          'node_modules/vis-network/dist/vis-network.min.css'
        )
      }
    },
    module: {
      rules: [
        {
          test: /vis-network\.min\.css$/,
          use: ['vue-style-loader', 'css-loader']
        }
      ]
    }
  },
  chainWebpack: config => {
    config.resolve.alias
      .set('vis-network', path.resolve(__dirname, 'node_modules/vis-network'))
      .set('vis-data', path.resolve(__dirname, 'node_modules/vis-data'))

    config.module
      .rule('vis-css')
      .test(/vis-network\.min\.css$/)
      .pre()
      .use('vue-style-loader')
        .loader('vue-style-loader')
        .end()
      .use('css-loader')
        .loader('css-loader')
        .end()
  },
  // 修正 transpileDependencies 配置
  transpileDependencies: [
    // 使用正则表达式匹配路径
    /[\\/]node_modules[\\/]vis-network/,
    /[\\/]node_modules[\\/]vis-data/
  ],
  outputDir: path.resolve(__dirname, '../kg_system/static'),
  indexPath: path.resolve(__dirname, '../kg_system/templates/index.html'),
  productionSourceMap: process.env.NODE_ENV !== 'production'
}