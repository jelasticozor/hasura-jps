'use strict'

const bodyParser = require('body-parser')
const {
  deleteMessage,
} = require('./functions')

module.exports = ({ app }, wrap) => {
  app.use(bodyParser.json())
  app.post('/', wrap(deleteMessage))
}
