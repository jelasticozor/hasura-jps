'use strict'

const bodyParser = require('body-parser')
const {
  deleteAllMessages
} = require('./functions')

module.exports = ({ app }, wrap) => {
  app.use(bodyParser.json())
  app.post('/', wrap(deleteAllMessages))
}
