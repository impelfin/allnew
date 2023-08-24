const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use(
        createProxyMiddleware("/api", {
            target: "http://3.37.236.215:8080/",
            changeOrigin: true,
        })
    )
}