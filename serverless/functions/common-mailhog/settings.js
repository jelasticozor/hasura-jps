// cf. https://github.com/blueimp/mailhog-node for documentation
exports.function = require('mailhog')({
  host: process.env.MAIL_SERVER_HOST,
  port: process.env.MAIL_SERVER_API_PORT
})
